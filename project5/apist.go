package api

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"sort"
	"sync"

	"time"

	"github.com/Masterminds/semver/v3"
	"github.com/gorilla/mux"
	"golang.org/x/time/rate"
)

var (
	packageMetaCache   = sync.Map{}
	packageCache       = sync.Map{}
	npmRegistryLimiter = rate.NewLimiter(rate.Every(time.Second), 10) // 10 requests per second
)

func New1() http.Handler {
	router := mux.NewRouter()
	router.Handle("/package/{package}/{version}", http.HandlerFunc(packageHandler1))
	router.Handle("/result", http.HandlerFunc(getTaskResultHandler))
	return router
}

func getTaskResultHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	mu.Lock()
	result, exists := taskStore[id]
	mu.Unlock()

	if !exists {
		http.Error(w, "Task not found or still running", http.StatusNotFound)
		return
	}

	fmt.Fprintf(w, "Task %s result: %s\n", id, result)
}

type npmPackageMetaResponse1 struct {
	Versions map[string]npmPackageResponse `json:"versions"`
}

type npmPackageResponse1 struct {
	Name         string            `json:"name"`
	Version      string            `json:"version"`
	Dependencies map[string]string `json:"dependencies"`
}

type NpmPackageVersion1 struct {
	Name         string                         `json:"name"`
	Version      string                         `json:"version"`
	Dependencies map[string]*NpmPackageVersion1 `json:"dependencies"`
}

func packageHandler1(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	pkgName := vars["package"]
	pkgVersion := vars["version"]

	log.Printf("Received request for package: %s, version: %s", pkgName, pkgVersion)

	rootPkg := &NpmPackageVersion1{Name: pkgName, Dependencies: map[string]*NpmPackageVersion1{}}
	if err := resolveDependencies1(rootPkg, pkgVersion); err != nil {
		log.Printf("Error resolving dependencies for %s@%s: %v", pkgName, pkgVersion, err)
		http.Error(w, "Failed to resolve dependencies", http.StatusInternalServerError)
		return
	}

	stringified, err := json.MarshalIndent(rootPkg, "", "  ")
	if err != nil {
		log.Printf("Error marshaling JSON for %s@%s: %v", pkgName, pkgVersion, err)
		http.Error(w, "Failed to generate JSON response", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	if _, err := w.Write(stringified); err != nil {
		log.Printf("Error writing response for %s@%s: %v", pkgName, pkgVersion, err)
	}
}
func resolveDependencies1(pkg *NpmPackageVersion1, versionConstraint string) error {
	pkgMeta, err := fetchPackageMeta1(pkg.Name)
	if err != nil {
		return err
	}
	concreteVersion, err := highestCompatibleVersion1(versionConstraint, pkgMeta)
	if err != nil {
		return err
	}
	pkg.Version = concreteVersion

	npmPkg, err := fetchPackage1(pkg.Name, pkg.Version)
	if err != nil {
		return err
	}

	var wg sync.WaitGroup
	mu := &sync.Mutex{}

	for dependencyName, dependencyVersionConstraint := range npmPkg.Dependencies {
		wg.Add(1)
		go func(depName, depVersion string) {
			defer wg.Done()
			dep := &NpmPackageVersion1{Name: depName, Dependencies: map[string]*NpmPackageVersion1{}}
			if err := resolveDependencies1(dep, depVersion); err != nil {
				fmt.Println("Error resolving dependency:", err)
				return
			}
			mu.Lock()
			pkg.Dependencies[depName] = dep
			mu.Unlock()
		}(dependencyName, dependencyVersionConstraint)
	}

	wg.Wait()
	return nil
}

func highestCompatibleVersion1(constraintStr string, versions *npmPackageMetaResponse1) (string, error) {
	constraint, err := semver.NewConstraint(constraintStr)
	if err != nil {
		return "", fmt.Errorf("invalid version constraint '%s': %w", constraintStr, err)
	}

	compatible := filterCompatibleVersions1(constraint, versions)
	if len(compatible) == 0 {
		return "", fmt.Errorf("no compatible versions found for constraint '%s'", constraintStr)
	}

	// Sort in descending order to get the highest version first
	sort.Slice(compatible, func(i, j int) bool {
		return compatible[i].GreaterThan(compatible[j])
	})

	return compatible[0].String(), nil

}

func filterCompatibleVersions1(constraint *semver.Constraints, pkgMeta *npmPackageMetaResponse1) semver.Collection {
	var compatible semver.Collection
	for version := range pkgMeta.Versions {
		semVer, err := semver.NewVersion(version)
		if err != nil {
			continue
		}
		if constraint.Check(semVer) {
			compatible = append(compatible, semVer)
		}
	}
	return compatible
}

func fetchPackage1(name, version string) (*npmPackageResponse1, error) {
	cacheKey := name + "@" + version
	if cached, ok := packageCache.Load(cacheKey); ok {
		return cached.(*npmPackageResponse1), nil
	}

	if err := npmRegistryLimiter.Wait(context.Background()); err != nil {
		return nil, fmt.Errorf("rate limit error: %w", err)
	}

	resp, err := http.Get(fmt.Sprintf("https://registry.npmjs.org/%s/%s", name, version))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var parsed npmPackageResponse1
	_ = json.Unmarshal(body, &parsed)

	packageCache.Store(cacheKey, &parsed)
	return &parsed, nil
}

// hard to mock, make https://registry.npmjs.org a variable
func fetchPackageMeta1(p string) (*npmPackageMetaResponse1, error) {
	if cached, ok := packageMetaCache.Load(p); ok {
		return cached.(*npmPackageMetaResponse1), nil
	}

	if err := npmRegistryLimiter.Wait(context.Background()); err != nil {
		return nil, fmt.Errorf("rate limit error: %w", err)
	}

	resp, err := http.Get(fmt.Sprintf("https://registry.npmjs.org/%s", p))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var parsed npmPackageMetaResponse1
	if err := json.Unmarshal([]byte(body), &parsed); err != nil {
		return nil, err
	}
	packageMetaCache.Store(p, &parsed)
	return &parsed, nil
}

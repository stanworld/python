package api

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"sync"

	"github.com/gorilla/mux"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

var logger *zap.Logger

func New() http.Handler {
	logLevel := os.Getenv("LOG_LEVEL")
	var level zapcore.Level
	switch logLevel {
	case "debug":
		level = zap.DebugLevel
	case "info":
		level = zap.InfoLevel
	case "error":
		level = zap.ErrorLevel
	default:
		level = zap.InfoLevel // Default to Info if not specified
	}
	config := zap.NewProductionConfig()
	config.Level = zap.NewAtomicLevelAt(level)
	var err error
	logger, err = config.Build()
	if err != nil {
		panic("Failed to initialize logger: " + err.Error())
	}
	defer logger.Sync()

	router := mux.NewRouter()
	router.Handle("/package/{package}/{version}", http.HandlerFunc(packageHandler))
	return router
}

type NpmPackageVersion struct {
	Name         string                        `json:"name"`
	Version      string                        `json:"version"`
	Dependencies map[string]*NpmPackageVersion `json:"dependencies"`
}

func packageHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	pkgName := vars["package"]
	pkgVersion := vars["version"]

	logger.Info(fmt.Sprintf("Fetching package %s@%s", pkgName, pkgVersion))
	rootPkg := &NpmPackageVersion{Name: pkgName, Dependencies: map[string]*NpmPackageVersion{}}
	if err := resolveDependencies(rootPkg, pkgVersion); err != nil {
		logger.Error(fmt.Sprintf("Failed to resolve dependencies for package %s@%s: %v", pkgName, pkgVersion, err))
		http.Error(w, "Failed to resove dependencies", http.StatusInternalServerError)
		return
	}

	stringified, err := json.MarshalIndent(rootPkg, "", "  ")
	if err != nil {
		logger.Error(fmt.Sprintf("Failed to fetch package %s@%s: %v", rootPkg.Name, rootPkg.Version, err))
		http.Error(w, "Failed to marshal JSON response", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	if _, err := w.Write(stringified); err != nil {
		logger.Error(fmt.Sprintf("Failed to write response for package %s@%s: %v", rootPkg.Name, rootPkg.Version, err))
	}
}

func resolveDependencies(pkg *NpmPackageVersion, versionConstraint string) error {
	pkgMeta, err := fetchPackageMeta(pkg.Name)
	if err != nil {
		return err
	}
	concreteVersion, err := highestCompatibleVersion(versionConstraint, pkgMeta)
	if err != nil {
		return err
	}
	pkg.Version = concreteVersion

	npmPkg, err := fetchPackage(pkg.Name, pkg.Version)
	if err != nil {
		return err
	}

	var wg sync.WaitGroup
	mu := &sync.Mutex{}

	for dependencyName, dependencyVersionConstraint := range npmPkg.Dependencies {
		wg.Add(1)
		go func(depName, depVersion string) {
			defer wg.Done()
			dep := &NpmPackageVersion{Name: depName, Dependencies: map[string]*NpmPackageVersion{}}

			if err := resolveDependencies(dep, depVersion); err != nil {
				logger.Error(fmt.Sprintf("Failed to resolve dependency %s for package %s@%s: %v", depName, pkg.Name, pkg.Version, err))
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

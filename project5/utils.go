package api

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"sort"
	"sync"
	"time"

	"github.com/Masterminds/semver/v3"
	"golang.org/x/time/rate"
)

var (
	packageMetaCache   = sync.Map{}
	packageCache       = sync.Map{}
	npmRegistryLimiter = rate.NewLimiter(rate.Every(time.Second), 50) // 10 requests per second
)

type npmPackageMetaResponse struct {
	Versions map[string]npmPackageResponse `json:"versions"`
}

type npmPackageResponse struct {
	Name         string            `json:"name"`
	Version      string            `json:"version"`
	Dependencies map[string]string `json:"dependencies"`
}

func highestCompatibleVersion(constraintStr string, versions *npmPackageMetaResponse) (string, error) {
	constraint, err := semver.NewConstraint(constraintStr)
	if err != nil {
		return "", err
	}
	filtered := filterCompatibleVersions(constraint, versions)
	if len(filtered) == 0 {
		return "", fmt.Errorf("no compatible versions found for constraint '%s'", constraintStr)
	}

	// Sort in descending order to get the highest version first
	sort.Slice(filtered, func(i, j int) bool {
		return filtered[i].GreaterThan(filtered[j])
	})

	return filtered[0].String(), nil
}

func filterCompatibleVersions(constraint *semver.Constraints, pkgMeta *npmPackageMetaResponse) semver.Collection {
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

func fetchPackage(name, version string) (*npmPackageResponse, error) {
	cacheKey := name + "@" + version
	if cached, ok := packageCache.Load(cacheKey); ok {
		return cached.(*npmPackageResponse), nil
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

	var parsed npmPackageResponse
	_ = json.Unmarshal(body, &parsed)

	packageCache.Store(cacheKey, &parsed)
	return &parsed, nil
}

func fetchPackageMeta(p string) (*npmPackageMetaResponse, error) {
	if cached, ok := packageMetaCache.Load(p); ok {
		return cached.(*npmPackageMetaResponse), nil
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

	var parsed npmPackageMetaResponse
	if err := json.Unmarshal([]byte(body), &parsed); err != nil {
		return nil, err
	}

	packageMetaCache.Store(p, &parsed)

	return &parsed, nil
}

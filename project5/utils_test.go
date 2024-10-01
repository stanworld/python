package api

import (
	"testing"

	"github.com/Masterminds/semver/v3"
	"github.com/stretchr/testify/assert"
)

func TestHighestCompatibleVersion(t *testing.T) {
	versions := &npmPackageMetaResponse{
		Versions: map[string]npmPackageResponse{
			"1.0.0": {},
			"1.1.0": {},
			"2.0.0": {},
		},
	}

	tests := []struct {
		constraint string
		expected   string
	}{
		{"^1.0.0", "1.1.0"},
		{"~2.0.0", "2.0.0"},
		{">=1.0.0", "2.0.0"},
	}

	for _, tt := range tests {
		result, err := highestCompatibleVersion(tt.constraint, versions)
		assert.NoError(t, err)
		assert.Equal(t, tt.expected, result)
	}
}

func TestFilterCompatibleVersions(t *testing.T) {
	versions := &npmPackageMetaResponse{
		Versions: map[string]npmPackageResponse{
			"1.0.0": {},
			"1.1.0": {},
			"2.0.0": {},
		},
	}

	constraint, _ := semver.NewConstraint("^1.0.0")
	compatible := filterCompatibleVersions(constraint, versions)

	assert.Len(t, compatible, 2)
	assert.Contains(t, compatible, semver.MustParse("1.0.0"))
	assert.Contains(t, compatible, semver.MustParse("1.1.0"))
}

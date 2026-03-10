package utils

// FindDuplicates returns all duplicate values in the slice.
// Uses a map-based approach for O(n) time complexity instead of O(n^3).
func FindDuplicates(items []string) []string {
	seen := make(map[string]int, len(items))
	var duplicates []string

	for _, item := range items {
		seen[item]++
		if seen[item] == 2 {
			duplicates = append(duplicates, item)
		}
	}

	return duplicates
}

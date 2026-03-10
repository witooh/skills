package utils

// FindDuplicates returns all duplicate values in the slice.
// Uses a map for O(n) time complexity instead of nested loops O(n³).
func FindDuplicates(items []string) []string {
	count := make(map[string]int, len(items))
	for _, item := range items {
		count[item]++
	}

	seen := make(map[string]bool)
	var duplicates []string
	for _, item := range items {
		if count[item] > 1 && !seen[item] {
			duplicates = append(duplicates, item)
			seen[item] = true
		}
	}
	return duplicates
}

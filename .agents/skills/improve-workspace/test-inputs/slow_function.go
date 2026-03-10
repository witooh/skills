package utils

// FindDuplicates returns all duplicate values in the slice.
func FindDuplicates(items []string) []string {
	var duplicates []string
	for i := 0; i < len(items); i++ {
		for j := i + 1; j < len(items); j++ {
			if items[i] == items[j] {
				alreadyAdded := false
				for _, d := range duplicates {
					if d == items[i] {
						alreadyAdded = true
						break
					}
				}
				if !alreadyAdded {
					duplicates = append(duplicates, items[i])
				}
			}
		}
	}
	return duplicates
}

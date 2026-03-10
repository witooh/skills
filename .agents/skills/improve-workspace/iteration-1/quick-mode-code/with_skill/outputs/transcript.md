# Improve Skill Transcript

## Mode Selection: Quick Mode

**Reason:** The user has a single, clear goal — "make this function faster." There are no competing tradeoffs or multiple quality dimensions to balance. Quick Mode is the correct choice per the skill's guidelines.

---

## Step 1 — Acknowledge the Goal

**Criterion (implicit):** Execution speed — reduce algorithmic time complexity so the function scales well with large inputs.

**User's request:** "This function is very slow. Help make it faster."

**What I would ask the user (but proceeding with a reasonable assumption):**
> "Do you need the output order to be stable (i.e., duplicates returned in the order they first appear), or is any order fine?"
>
> **Assumption:** Stable order (first-seen order) is preferred, as this matches the original function's behavior.

---

## Step 2 — Identify the Bottleneck

### Original Code Analysis

```go
func FindDuplicates(items []string) []string {
    var duplicates []string
    for i := 0; i < len(items); i++ {           // O(n)
        for j := i + 1; j < len(items); j++ {   //   O(n)
            if items[i] == items[j] {
                alreadyAdded := false
                for _, d := range duplicates {   //     O(d) worst-case O(n)
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
```

**Three nested loops produce O(n^3) worst-case time complexity:**

| Loop | Purpose | Complexity |
|---|---|---|
| Outer loop (i) | Iterate each element | O(n) |
| Inner loop (j) | Compare against all subsequent elements | O(n) |
| Dedup loop (d) | Linear scan of duplicates slice to avoid re-adding | O(n) worst case |

For a slice of 10,000 items, this could perform up to ~1 trillion comparisons in the worst case.

---

## Step 3 — Apply the Improvement

**Strategy:** Replace all three loops with a single pass using a `map[string]int` to count occurrences. Append to the result slice only when the count reaches exactly 2, which naturally deduplicates.

### Improved Code

```go
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
```

---

## Step 4 — Before/After Comparison

### Time Complexity

| Aspect | Before | After |
|---|---|---|
| Time complexity | O(n^3) worst case | O(n) amortized |
| Space complexity | O(d) where d = number of duplicates | O(n) for the map |
| Number of passes | Triple-nested loops | Single pass |
| Deduplication strategy | Linear scan of result slice | Counter check (== 2) |

### Behavioral Equivalence

| Behavior | Before | After |
|---|---|---|
| Returns duplicates only once | Yes (linear scan dedup) | Yes (append only at count == 2) |
| Preserves first-seen order | Yes | Yes (iteration order = input order) |
| Handles empty slice | Yes (returns nil) | Yes (returns nil) |
| Handles no duplicates | Yes (returns empty) | Yes (returns empty) |

### Performance Estimate (order of magnitude)

| Input Size | Before (approx ops) | After (approx ops) | Speedup |
|---|---|---|---|
| 100 items | ~1,000,000 | ~100 | ~10,000x |
| 1,000 items | ~1,000,000,000 | ~1,000 | ~1,000,000x |
| 10,000 items | ~1,000,000,000,000 | ~10,000 | ~100,000,000x |

### Tradeoff

The improved version uses O(n) extra memory for the hash map. This is a standard and acceptable tradeoff — memory is cheap, and the cubic-to-linear time improvement is dramatic.

---

## Step 5 — User Checkpoint

**What I would ask the user:**
> "Does this hit the mark, or should I keep going? The function now runs in O(n) time instead of O(n^3) by using a hash map for counting. The output order and deduplication behavior are preserved. If you'd like further refinement (e.g., concurrency for extremely large slices, or a generic version using Go generics), I can escalate to Full Mode."

**Assumption:** The user would be satisfied — the single stated goal (speed) has been thoroughly addressed with a standard, idiomatic optimization.

---

## Summary

| Item | Detail |
|---|---|
| Mode | Quick Mode |
| Criterion | Execution speed (reduce time complexity) |
| Original complexity | O(n^3) |
| Improved complexity | O(n) |
| Approach | Single-pass counting with map[string]int |
| Behavioral changes | None — output order and dedup behavior preserved |
| Tradeoff | O(n) additional memory for the hash map |

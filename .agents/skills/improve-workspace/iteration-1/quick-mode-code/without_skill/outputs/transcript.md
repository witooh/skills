# Optimization: FindDuplicates

## Problem

The original function uses three nested loops making it O(n^3):

1. Outer loop iterates all items — O(n)
2. Inner loop compares with remaining items — O(n)
3. Third loop checks if already added to duplicates — O(n)

## What Changed

Replaced nested loops with a hash map approach that runs in **O(n)** time:

- **First pass:** Count occurrences of each item using `map[string]int`.
- **Second pass:** Iterate items in original order; emit those with count > 1, using a `seen` map to avoid emitting the same value twice.

## Complexity Comparison

| Aspect | Original | Improved |
|--------|----------|----------|
| Time complexity | O(n^3) | O(n) |
| Space complexity | O(d) where d = duplicates | O(n) |
| Allocations | append-only slice | pre-sized maps + slice |

The trade-off is a small increase in memory usage (hash maps) for a dramatic improvement in execution time — especially noticeable when `items` is large.

## Preserved Behavior

- Return order matches first-appearance order in the input slice.
- No external dependencies added.
- Function signature and package unchanged.

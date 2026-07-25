# 17. Letter Combinations of a Phone Number

**Difficulty:** Medium
**Topics:** Hash Table, String, Backtracking
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number could represent. Return the answer in **any order**.

A mapping of digits to letters (just like on the telephone buttons) is given below. Note that `1` does not map to any letters.

```
2 -> "abc"    3 -> "def"    4 -> "ghi"
5 -> "jkl"    6 -> "mno"    7 -> "pqrs"
8 -> "tuv"    9 -> "wxyz"
```

## Example 1

```
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

## Example 2

```
Input: digits = ""
Output: []
```

## Example 3

```
Input: digits = "2"
Output: ["a","b","c"]
```

## Constraints

- `0 <= digits.length <= 4`
- `digits[i]` is a digit in the range `['2', '9']`.

## Approach

1. Build a mapping from each digit to its corresponding set of letters.
2. Use **backtracking**: maintain a partially-built combination string. At each recursive step, pick the next digit and try appending each of its letters one at a time, recursing into the next digit position.
3. Base case: once the partial combination's length equals `len(digits)`, it's a complete combination — add it to the results.
4. Handle the empty-input edge case explicitly (return an empty list, not `[""]`).

**Time Complexity:** O(4^n · n), where n is the number of digits — up to 4 letters per digit (for digits 7 and 9), and building/copying each combination string takes O(n).
**Space Complexity:** O(n) for the recursion depth (excluding the output).

## Reference Solution (Python)

```python
def letter_combinations(digits: str) -> list[str]:
    if not digits:
        return []

    digit_to_letters = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
    }

    result: list[str] = []

    def backtrack(index: int, current: list[str]) -> None:
        if index == len(digits):
            result.append("".join(current))
            return

        for letter in digit_to_letters[digits[index]]:
            current.append(letter)
            backtrack(index + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

## Follow-up Questions Interviewers May Ask

- How would you solve this iteratively, building up combinations level by level instead of recursively?
- How would this generalize to an arbitrary custom digit-to-letters mapping?
- How would you generate combinations lazily (as a generator/iterator) instead of building the full list upfront, for very long digit strings?

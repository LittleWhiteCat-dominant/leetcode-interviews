# 796. Rotate String

**Difficulty:** Easy
**Topics:** String, String Matching
**Reported at Rivian:** Confirmed — reported in multiple 2025 onsite interviews.

## Problem Description

Given two strings `s` and `goal`, return `true` if and only if `s` can become `goal` after some number of **shifts** on `s`.

A **shift** on `s` consists of moving the leftmost character of `s` to the rightmost position.

- For example, if `s = "abcde"`, then it will be `"bcdea"` after one shift.

## Example 1

```
Input: s = "abcde", goal = "cdeab"
Output: true
```

## Example 2

```
Input: s = "abcde", goal = "abced"
Output: false
```

## Constraints

- `1 <= s.length, goal.length <= 100`
- `s` and `goal` consist of lowercase English letters.

## Approach

1. **Length check first**: if `len(s) != len(goal)`, immediately return `False`.
2. **Key trick**: `goal` is a rotation of `s` if and only if `goal` is a substring of `s + s`.
   - Concatenating `s` with itself produces every possible rotation of `s` as a contiguous substring.
3. Check whether `goal` occurs inside `s + s` using a substring search (built-in `in` operator, or KMP for the optimal O(n) follow-up).

**Time Complexity:** O(n) with an efficient substring search (KMP / Python's built-in `in`, which uses an optimized algorithm), or O(n²) with naive substring search.
**Space Complexity:** O(n) for the concatenated string.

## Reference Solution (Python)

```python
def rotate_string(s: str, goal: str) -> bool:
    if len(s) != len(goal):
        return False
    # Every rotation of s appears as a contiguous substring of s + s.
    return goal in (s + s)
```

## Follow-up Questions Interviewers May Ask

- Can you implement the substring search yourself (KMP) instead of relying on a built-in function?
- What if `s` and `goal` can contain arbitrary Unicode characters?
- How would you check if one string is a rotation of another without extra space (in-place, O(1) extra space)?

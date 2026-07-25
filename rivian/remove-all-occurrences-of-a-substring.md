# 1910. Remove All Occurrences of a Substring

**Difficulty:** Medium
**Topics:** String, Stack, String Matching
**Reported at Rivian:** Referenced in Rivian interview prep guides as a frequently tested topic area.

## Problem Description

Given two strings `s` and `part`, perform the following operation on `s` until **all** occurrences of the substring `part` are removed:

- Find the **leftmost** occurrence of the substring `part` and **remove** it from `s`.

Return `s` *after* removing all occurrences of `part`.

A **substring** is a contiguous sequence of characters in a string.

## Example 1

```
Input: s = "daabcbaabcbc", part = "abc"
Output: "dab"
Explanation: The following operations are done:
- s = "daabcbaabcbc", remove "abc" starting at index 2, so s = "dabaabcbc".
- s = "dabaabcbc", remove "abc" starting at index 4, so s = "dababc".
- s = "dababc", remove "abc" starting at index 3, so s = "dab".
Now s has no occurrences of "abc".
```

## Example 2

```
Input: s = "axxxxyyyyb", part = "xy"
Output: "ab"
Explanation:
- s = "axxxxyyyyb", remove "xy" starting at index 4, so s = "axxxyyyb".
- s = "axxxyyyb", remove "xy" starting at index 3, so s = "axxyyb".
- s = "axxyyb", remove "xy" starting at index 2, so s = "axyb".
- s = "axyb", remove "xy" starting at index 1, so s = "ab".
Now s has no occurrences of "xy".
```

## Constraints

- `1 <= s.length <= 1000`
- `1 <= part.length <= 1000`
- `s` and `part` consist of lowercase English letters.

## Approach

1. Use a **stack-based** approach to build the result string character by character.
2. Push each character of `s` onto the stack.
3. After every push, check whether the top `len(part)` characters of the stack match `part`. If so, pop those characters off (this simulates "removing the leftmost occurrence" because the stack always reflects the current state of the processed prefix, and removals cascade correctly).
4. At the end, the stack contains the final result.

This is efficient because directly simulating the removal process with string slicing/concatenation would be O(n²) or worse in the worst case (e.g. `s = "aaaa...a"`, `part = "aa"`), while the stack approach amortizes to a better bound in practice.

**Time Complexity:** O(n · m) worst case, where n is the length of `s` and m is the length of `part` (each match check compares up to `m` characters), though in practice this is efficient for the given constraints.
**Space Complexity:** O(n) for the stack.

## Reference Solution (Python)

```python
def remove_occurrences(s: str, part: str) -> str:
    stack: list[str] = []
    part_len = len(part)

    for char in s:
        stack.append(char)
        if len(stack) >= part_len and "".join(stack[-part_len:]) == part:
            del stack[-part_len:]

    return "".join(stack)
```

## Follow-up Questions Interviewers May Ask

- How would you optimize the substring comparison using hashing (rolling hash) instead of slicing and joining each time?
- What if `part` could itself contain the pattern being removed as a substring (overlapping edge cases)?
- How would you solve this using the KMP algorithm to detect matches more efficiently?

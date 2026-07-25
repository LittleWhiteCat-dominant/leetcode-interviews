# 242. Valid Anagram

**Difficulty:** Easy
**Topics:** String, Hash Table, Sorting
**Category warm-up for:** String

## Problem Description

Given two strings `s` and `t`, return `true` *if* `t` *is an anagram of* `s`*, and* `false` *otherwise*.

An **Anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

## Example 1

```
Input: s = "anagram", t = "nagaram"
Output: true
```

## Example 2

```
Input: s = "rat", t = "car"
Output: false
```

## Constraints

- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` consist of lowercase English letters.

**Follow-up:** What if the inputs contain Unicode characters? How would you adapt your solution to such a case?

## Approach

1. **Length check first**: if `len(s) != len(t)`, they cannot be anagrams — return `False` immediately.
2. **Optimal — character frequency count**: build a count (via a hash map, or a fixed-size array of 26 for lowercase English letters) of every character in `s`, then decrement the count for every character in `t`. If any count goes negative, or any count is nonzero at the end, return `False`.
3. **Alternative — sorting**: sort both strings and compare them directly; they are anagrams if and only if the sorted strings are equal. Simpler to write, but O(n log n) instead of O(n).

**Time Complexity:** O(n) with the counting approach; O(n log n) with the sorting approach.
**Space Complexity:** O(1) extra space with a fixed 26-slot array (since the alphabet size is constant); O(n) with a general hash map (needed for the Unicode follow-up).

## Reference Solution (Python)

```python
def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    counts: dict[str, int] = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    for char in t:
        counts[char] = counts.get(char, 0) - 1
        if counts[char] < 0:
            return False

    return all(count == 0 for count in counts.values())
```

## Follow-up Questions Interviewers May Ask

- How would you handle Unicode characters where a fixed 26-slot array no longer works (use a general hash map instead)?
- How would you solve **Group Anagrams** (LC 49), which groups an entire list of strings by anagram equivalence?
- How would you check for anagrams while ignoring case and non-alphanumeric characters (spaces, punctuation)?

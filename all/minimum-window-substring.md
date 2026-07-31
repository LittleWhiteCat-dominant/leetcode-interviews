# 76. Minimum Window Substring

**Difficulty:** Hard
**Topics:** Hash Table, String, Sliding Window
**Common companies:** **Meta, Amazon favorite**
**Category (README):** 1.2 Sliding Window

## Problem Description

Given two strings `s` and `t` of lengths `m` and `n` respectively, return *the **minimum window*** ***substring**** of *`s`* such that every character in *`t`* (**including duplicates**) is included in the window*. If there is no such substring, return *the empty string *`""`.

The testcases will be generated such that the answer is **unique**.

 

**Example 1:**

```

**Input:** s = "ADOBECODEBANC", t = "ABC"
**Output:** "BANC"
**Explanation:** The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.

```

**Example 2:**

```

**Input:** s = "a", t = "a"
**Output:** "a"
**Explanation:** The entire string s is the minimum window.

```

**Example 3:**

```

**Input:** s = "a", t = "aa"
**Output:** ""
**Explanation:** Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return empty string.

```

 

**Constraints:**

	
- `m == s.length`

	
- `n == t.length`

	
- `1 <= m, n <= 105`

	
- `s` and `t` consist of uppercase and lowercase English letters.

 

**Follow up:** Could you find an algorithm that runs in `O(m + n)` time?

## Key Idea

Counted window, shrink to find the minimal valid window

## Approach

This is solved with **a counted sliding window**:

1. Build a `Counter` of required characters from `t`, and track `missing`, the total count of characters still needed to satisfy the window (initialized to `len(t)`).
2. Expand the window by moving `right` forward: decrement `need[ch]` for the incoming character, and decrement `missing` whenever `need[ch]` was still positive (meaning that character was actually needed).
3. Once `missing` hits `0`, the window is valid, so shrink it from the left as much as possible: while the leftmost character has a negative count in `need` (a surplus), give it back and advance `left`.
4. Record this window if it's shorter than the best found so far, then release the leftmost character (making it "needed" again), increment `missing`, and advance `left` past it to keep searching for shorter windows.
5. Return the shortest recorded window, or an empty string if none was found.

**Time Complexity:** O(m + n) — `s` is scanned with two pointers that each advance at most `m` times total; `t` is scanned once to build the counts.
**Space Complexity:** O(m + n) — the `Counter` holds at most the distinct characters of `t`.

## Reference Solution (Python)

```python
from collections import Counter


def minWindow(s: str, t: str) -> str:
    if not t or not s:
        return ""

    need = Counter(t)
    missing = len(t)
    left = start = end = 0

    for right, ch in enumerate(s, 1):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1

        if missing == 0:
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if end == 0 or right - left < end - start:
                start, end = left, right
            need[s[left]] += 1
            missing += 1
            left += 1

    return s[start:end]
```

## Reference

- LeetCode: https://leetcode.com/problems/minimum-window-substring/

# 316. Remove Duplicate Letters

**Difficulty:** Medium
**Topics:** String, Stack, Greedy, Monotonic Stack
**Common companies:** Google
**Category (README):** 4.2 Monotonic Stack

## Problem Description

Given a string `s`, remove duplicate letters so that every letter appears once and only once. You must make sure your result is **the smallest in lexicographical order** among all possible results.

 

**Example 1:**

```

**Input:** s = "bcabc"
**Output:** "abc"

```

**Example 2:**

```

**Input:** s = "cbacdcbc"
**Output:** "acdb"

```

 

**Constraints:**

	
- `1 <= s.length <= 104`

	
- `s` consists of lowercase English letters.

 

**Note:** This question is the same as 1081: https://leetcode.com/problems/smallest-subsequence-of-distinct-characters/

## Key Idea

Greedy monotonic stack for the smallest lexicographic result

## Approach

This is solved with a **greedy monotonic stack**, popping a larger character off the stack only if it reappears later:

1. Precompute `last_occurrence`, mapping each character to the index of its last appearance in `s` — this tells us whether it's safe to remove a character now because it will show up again later.
2. Scan `s` left to right, maintaining a stack of the result-in-progress and a set `in_stack` of characters currently on it.
3. Skip any character already in `in_stack`, since each letter must appear exactly once in the final answer.
4. Otherwise, while the stack's top character is lexicographically greater than the current character **and** that top character occurs again later (`last_occurrence[stack[-1]] > i`), pop it off (it can be safely removed now and re-added later to produce a smaller result).
5. Push the current character onto the stack and mark it as `in_stack`.
6. After processing all of `s`, the stack contains each letter exactly once in the smallest possible lexicographic order; join it into the final string.

**Time Complexity:** O(n) — each character is pushed and popped from the stack at most once.
**Space Complexity:** O(1) — the stack and helper sets hold at most 26 lowercase letters.

## Reference Solution (Python)

```python
def removeDuplicateLetters(s: str) -> str:
    last_occurrence = {ch: i for i, ch in enumerate(s)}
    stack = []
    in_stack = set()

    for i, ch in enumerate(s):
        if ch in in_stack:
            continue
        while stack and stack[-1] > ch and last_occurrence[stack[-1]] > i:
            in_stack.remove(stack.pop())
        stack.append(ch)
        in_stack.add(ch)

    return "".join(stack)
```

## Reference

- LeetCode: https://leetcode.com/problems/remove-duplicate-letters/

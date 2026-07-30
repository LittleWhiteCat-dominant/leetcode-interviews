# 271. Encode and Decode Strings

**Difficulty:** Medium (LeetCode Premium — statement not publicly available)
**Topics:** Array, String, Design
**Common companies:** Google, Meta
**Category (README):** 2. String

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/encode-and-decode-strings/

## Key Idea

Length-prefixed encoding to handle arbitrary characters

## Approach

1. Identify the core pattern for this category: **2. String**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — where n is the total number of characters across all strings; encode and decode each make a single linear pass.
**Space Complexity:** O(n) — the encoded string (and decoded output) size scales with the total input length.

## Reference Solution (Python)

```python
def encode(strs: list[str]) -> str:
    return "".join(f"{len(s)}#{s}" for s in strs)


def decode(s: str) -> list[str]:
    result: list[str] = []
    i = 0
    while i < len(s):
        j = s.index('#', i)
        length = int(s[i:j])
        start = j + 1
        result.append(s[start:start + length])
        i = start + length
    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/encode-and-decode-strings/

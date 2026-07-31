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

This is solved with **length-prefixed encoding, so delimiters can never be confused with real content**:

1. `encode` joins every string as `f"{len(s)}#{s}"`, prefixing each string with its length and a `#` separator before the raw characters.
2. Because the length is known up front, the decoder never needs to search for a terminating delimiter inside the string content, so arbitrary characters (including `#` itself) are safe.
3. `decode` scans through the combined string with an index `i`; at each step it finds the next `#` via `s.index('#', i)` to read off the length prefix.
4. It converts the text before `#` to an integer `length`, then slices exactly that many characters right after the `#` to recover one original string.
5. Advance `i` past the string just read and repeat until the whole encoded string is consumed, collecting each recovered string into the result list.

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

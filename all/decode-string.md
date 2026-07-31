# 394. Decode String

**Difficulty:** Medium
**Topics:** String, Stack, Recursion
**Common companies:** Google, Amazon
**Category (README):** 4.1 Basic Stack Applications

## Problem Description

Given an encoded string, return its decoded string.

The encoding rule is: `k[encoded_string]`, where the `encoded_string` inside the square brackets is being repeated exactly `k` times. Note that `k` is guaranteed to be a positive integer.

You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc. Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, `k`. For example, there will not be input like `3a` or `2[4]`.

The test cases are generated so that the length of the output will never exceed `105`.

 

**Example 1:**

```

**Input:** s = "3[a]2[bc]"
**Output:** "aaabcbc"

```

**Example 2:**

```

**Input:** s = "3[a2[c]]"
**Output:** "accaccacc"

```

**Example 3:**

```

**Input:** s = "2[abc]3[cd]ef"
**Output:** "abcabccdcdcdef"

```

 

**Constraints:**

	
- `1 <= s.length <= 30`

	
- `s` consists of lowercase English letters, digits, and square brackets `'[]'`.

	
- `s` is guaranteed to be **a valid** input.

	
- All the integers in `s` are in the range `[1, 300]`.

## Key Idea

Stack holding repeat counts and the string built so far

## Approach

This is solved with **a stack that saves the enclosing string and repeat count at each `[`**:

1. Track `current_string` (the string built so far at the current nesting level) and `current_num` (the digits accumulated for the next repeat count).
2. On a digit, accumulate it into `current_num` (`current_num * 10 + digit`), since counts can be multi-digit.
3. On `[`, push `(current_string, current_num)` onto the stack to save the outer context, then reset both to start fresh for the bracketed segment.
4. On `]`, pop the saved `(prev_string, num)`, and set `current_string = prev_string + current_string * num`, repeating the just-finished segment and reattaching it to its enclosing string.
5. On a plain letter, append it directly to `current_string`.
6. Return `current_string` once the whole input has been consumed.

**Time Complexity:** O(n) — where n is the length of the fully decoded output string (bounded by the problem's 10^5 limit).
**Space Complexity:** O(n) — the stack of partial strings/counts plus the string being built.

## Reference Solution (Python)

```python
def decodeString(s: str) -> str:
    stack: list[tuple[str, int]] = []
    current_string = ""
    current_num = 0

    for char in s:
        if char.isdigit():
            current_num = current_num * 10 + int(char)
        elif char == '[':
            stack.append((current_string, current_num))
            current_string = ""
            current_num = 0
        elif char == ']':
            prev_string, num = stack.pop()
            current_string = prev_string + current_string * num
        else:
            current_string += char

    return current_string
```

## Reference

- LeetCode: https://leetcode.com/problems/decode-string/

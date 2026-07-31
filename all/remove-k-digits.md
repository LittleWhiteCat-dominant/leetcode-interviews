# 402. Remove K Digits

**Difficulty:** Medium
**Topics:** String, Stack, Greedy, Monotonic Stack
**Common companies:** Google
**Category (README):** 4.2 Monotonic Stack

## Problem Description

Given string num representing a non-negative integer `num`, and an integer `k`, return *the smallest possible integer after removing* `k` *digits from* `num`.

 

**Example 1:**

```

**Input:** num = "1432219", k = 3
**Output:** "1219"
**Explanation:** Remove the three digits 4, 3, and 2 to form the new number 1219 which is the smallest.

```

**Example 2:**

```

**Input:** num = "10200", k = 1
**Output:** "200"
**Explanation:** Remove the leading 1 and the number is 200. Note that the output must not contain leading zeroes.

```

**Example 3:**

```

**Input:** num = "10", k = 2
**Output:** "0"
**Explanation:** Remove all the digits from the number and it is left with nothing which is 0.

```

 

**Constraints:**

	
- `1 <= k <= num.length <= 105`

	
- `num` consists of only digits.

	
- `num` does not have any leading zeros except for the zero itself.

## Key Idea

Greedy monotonic stack for the smallest lexicographic result

## Approach

This is solved with a **greedy monotonic (increasing) stack**, since removing a digit is most beneficial when it's larger than the digit right after it:

1. Scan `num` left to right, building the result digit by digit on a stack.
2. Before pushing the current digit, pop any digits off the top of the stack that are strictly greater than it, as long as there are still removals left (`k > 0`) — a bigger digit followed by a smaller one should always be removed to shrink the number's magnitude.
3. Push the current digit after the popping loop, keeping the stack non-decreasing from bottom to top whenever possible.
4. If any removals (`k`) remain after the full scan (meaning `num` was entirely non-decreasing), remove the last `k` digits from the stack, since trailing large digits contribute the most to the number's value.
5. Join the stack into a string and strip leading zeros (e.g. `"0200"` → `"200"`), returning `"0"` if the result is empty.

**Time Complexity:** O(n) — each digit is pushed and popped from the stack at most once.
**Space Complexity:** O(n) — for the monotonic stack holding the result digits.

## Reference Solution (Python)

```python
def removeKdigits(num: str, k: int) -> str:
    stack = []

    for digit in num:
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)

    if k > 0:
        stack = stack[:-k]

    result = "".join(stack).lstrip("0")
    return result if result else "0"
```

## Reference

- LeetCode: https://leetcode.com/problems/remove-k-digits/

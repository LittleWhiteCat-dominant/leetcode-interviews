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

1. Identify the core pattern for this category: **4.2 Monotonic Stack**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/remove-duplicate-letters/

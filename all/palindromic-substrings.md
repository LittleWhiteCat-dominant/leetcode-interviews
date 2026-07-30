# 647. Palindromic Substrings

**Difficulty:** Medium
**Topics:** Two Pointers, String, Dynamic Programming
**Common companies:** Amazon, Google
**Category (README):** 2. String

## Problem Description

Given a string `s`, return *the number of **palindromic substrings** in it*.

A string is a **palindrome** when it reads the same backward as forward.

A **substring** is a contiguous sequence of characters within the string.

 

**Example 1:**

```

**Input:** s = "abc"
**Output:** 3
**Explanation:** Three palindromic strings: "a", "b", "c".

```

**Example 2:**

```

**Input:** s = "aaa"
**Output:** 6
**Explanation:** Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".

```

 

**Constraints:**

	
- `1 <= s.length <= 1000`

	
- `s` consists of lowercase English letters.

## Key Idea

Expand around center, counting palindromes

## Approach

1. Identify the core pattern for this category: **2. String**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/palindromic-substrings/

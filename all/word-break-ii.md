# 140. Word Break II

**Difficulty:** Hard
**Topics:** Array, Hash Table, String, Dynamic Programming, Backtracking, Trie, Memoization
**Common companies:** All big tech
**Category (README):** 2. String

## Problem Description

Given a string `s` and a dictionary of strings `wordDict`, add spaces in `s` to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in **any order**.

**Note** that the same word in the dictionary may be reused multiple times in the segmentation.

 

**Example 1:**

```

**Input:** s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
**Output:** ["cats and dog","cat sand dog"]

```

**Example 2:**

```

**Input:** s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
**Output:** ["pine apple pen apple","pineapple pen apple","pine applepen apple"]
**Explanation:** Note that you are allowed to reuse a dictionary word.

```

**Example 3:**

```

**Input:** s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
**Output:** []

```

 

**Constraints:**

	
- `1 <= s.length <= 20`

	
- `1 <= wordDict.length <= 1000`

	
- `1 <= wordDict[i].length <= 10`

	
- `s` and `wordDict[i]` consist of only lowercase English letters.

	
- All the strings of `wordDict` are **unique**.

	
- Input is generated in a way that the length of the answer doesn't exceed 105.

## Key Idea

String DP; a Trie can speed up lookups

## Approach

1. Identify the core pattern for this category: **2. String**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/word-break-ii/

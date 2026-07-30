# 212. Word Search II

**Difficulty:** Hard
**Topics:** Array, String, Backtracking, Trie, Matrix
**Common companies:** All big tech
**Category (README):** 7.3 Trie (Prefix Tree)

## Problem Description

Given an `m x n` `board` of characters and a list of strings `words`, return *all words on the board*.

Each word must be constructed from letters of sequentially adjacent cells, where **adjacent cells** are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

 

**Example 1:**

```

**Input:** board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
**Output:** ["eat","oath"]

```

**Example 2:**

```

**Input:** board = [["a","b"],["c","d"]], words = ["abcb"]
**Output:** []

```

 

**Constraints:**

	
- `m == board.length`

	
- `n == board[i].length`

	
- `1 <= m, n <= 12`

	
- `board[i][j]` is a lowercase English letter.

	
- `1 <= words.length <= 3 * 104`

	
- `1 <= words[i].length <= 10`

	
- `words[i]` consists of lowercase English letters.

	
- All the strings of `words` are unique.

## Key Idea

Trie + backtracking DFS on the matrix

## Approach

1. Identify the core pattern for this category: **7.3 Trie (Prefix Tree)**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/word-search-ii/

# 127. Word Ladder

**Difficulty:** Hard
**Topics:** Hash Table, String, Breadth-First Search
**Common companies:** All big tech
**Category (README):** 9.1 DFS / BFS Fundamentals

## Problem Description

A **transformation sequence** from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that:

	
- Every adjacent pair of words differs by a single letter.

	
- Every `si` for `1 <= i <= k` is in `wordList`. Note that `beginWord` does not need to be in `wordList`.

	
- `sk == endWord`

Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return *the **number of words** in the **shortest transformation sequence** from* `beginWord` *to* `endWord`*, or *`0`* if no such sequence exists.*

 

**Example 1:**

```

**Input:** beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
**Output:** 5
**Explanation:** One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> cog", which is 5 words long.

```

**Example 2:**

```

**Input:** beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
**Output:** 0
**Explanation:** The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.

```

 

**Constraints:**

	
- `1 <= beginWord.length <= 10`

	
- `endWord.length == beginWord.length`

	
- `1 <= wordList.length <= 5000`

	
- `wordList[i].length == beginWord.length`

	
- `beginWord`, `endWord`, and `wordList[i]` consist of lowercase English letters.

	
- `beginWord != endWord`

	
- All the words in `wordList` are **unique**.

## Key Idea

BFS for the shortest transformation path length

## Approach

1. Identify the core pattern for this category: **9.1 DFS / BFS Fundamentals**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/word-ladder/

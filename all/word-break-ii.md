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

**Time Complexity:** O(n * 2^n) worst case — the memoized DP explores O(n^2) substring states, but the number of valid sentences to build and join can itself be exponential in `n` (bounded here since `s.length <= 20`).
**Space Complexity:** O(n * 2^n) — the memo table stores every valid decomposition suffix, dominated by the exponentially many stored sentences; recursion depth is O(n).

## Reference Solution (Python)

```python
def wordBreak(s: str, wordDict: list[str]) -> list[str]:
    word_set = set(wordDict)
    memo: dict[int, list[list[str]]] = {}

    def backtrack(start: int) -> list[list[str]]:
        if start == len(s):
            return [[]]
        if start in memo:
            return memo[start]

        sentences = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                for rest in backtrack(end):
                    sentences.append([word] + rest)

        memo[start] = sentences
        return sentences

    return [" ".join(words) for words in backtrack(0)]
```

## Reference

- LeetCode: https://leetcode.com/problems/word-break-ii/

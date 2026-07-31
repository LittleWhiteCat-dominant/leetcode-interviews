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

This is solved with **memoized backtracking that builds sentences from each suffix**:

1. Define `backtrack(start)` to return the list of all ways to split `s[start:]` into valid dictionary words (each way represented as a list of words).
2. Base case: if `start == len(s)`, the empty split `[[]]` is the single valid way to decompose "nothing left".
3. Otherwise, try every possible next word `s[start:end]` for `end` from `start + 1` to `len(s)`; if it's in the dictionary, recursively solve for the remainder via `backtrack(end)`.
4. For every decomposition of the remainder, prepend the current word to form a full decomposition of `s[start:]`, and collect all of these.
5. Memoize results by `start` index so overlapping suffixes (reached via different earlier splits) are only computed once.
6. Join each word list with spaces to produce the final list of sentences from `backtrack(0)`.

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

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

This is solved with **BFS over an implicit graph where edges connect words one letter apart**:

1. Put all words from `wordList` into a set for O(1) membership checks, and immediately return 0 if `endWord` isn't present.
2. Start a BFS from `beginWord` with a step count of 1, removing `beginWord` from the set so it isn't revisited.
3. At each step, dequeue a word; if it equals `endWord`, its recorded step count is the answer.
4. Otherwise, generate every possible one-letter variation of the current word (each position, all 26 letters).
5. For each variation that exists in the remaining word set, remove it from the set (marking it visited) and enqueue it with `steps + 1`.
6. Because BFS explores layer by layer, the first time `endWord` is dequeued it is guaranteed to be via the shortest transformation sequence; if the queue empties first, return 0.

**Time Complexity:** O(N * L^2) — for each of the `N` words in the word list, BFS tries `L` positions times 26 letter substitutions, each costing O(L) to build the candidate string.
**Space Complexity:** O(N * L) — the word set and BFS queue store up to all words of length `L`.

## Reference Solution (Python)

```python
from collections import deque


def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    word_set = set(wordList)
    if endWord not in word_set:
        return 0

    queue = deque([(beginWord, 1)])
    word_set.discard(beginWord)

    while queue:
        word, steps = queue.popleft()
        if word == endWord:
            return steps

        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                if c == word[i]:
                    continue
                next_word = word[:i] + c + word[i + 1:]
                if next_word in word_set:
                    word_set.discard(next_word)
                    queue.append((next_word, steps + 1))

    return 0
```

## Reference

- LeetCode: https://leetcode.com/problems/word-ladder/

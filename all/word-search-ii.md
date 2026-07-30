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

**Time Complexity:** O(m * n * 4 * 3^(L-1)) — DFS/backtracking from each of the `m * n` cells, with the Trie pruning branches that share no common prefix (`L` is the max word length).
**Space Complexity:** O(sum of word lengths) — for the Trie, plus O(L) recursion depth per DFS call.

## Reference Solution (Python)

```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.word: str | None = None


def findWords(board: list[list[str]], words: list[str]) -> list[str]:
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.word = word

    rows, cols = len(board), len(board[0])
    result = []

    def dfs(r: int, c: int, node: TrieNode) -> None:
        ch = board[r][c]
        if ch not in node.children:
            return

        child = node.children[ch]
        if child.word is not None:
            result.append(child.word)
            child.word = None  # avoid duplicate results

        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                dfs(nr, nc, child)
        board[r][c] = ch

        if not child.children:
            del node.children[ch]

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/word-search-ii/

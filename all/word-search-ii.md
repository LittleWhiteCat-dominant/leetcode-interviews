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

This is solved with **a Trie of all target words combined with DFS backtracking on the board**:

1. Build a Trie from all words in `words`, marking terminal nodes with the complete word they represent.
2. Start a DFS/backtracking search from every cell on the board, walking the Trie alongside the board traversal so a branch is only explored while it still matches a valid prefix.
3. At each cell, if the current board character isn't among the Trie node's children, prune this branch immediately (no word can start this way).
4. If the child node marks the end of a word, record that word in the results and clear its `word` marker to avoid duplicate matches.
5. Temporarily mark the current cell as visited (e.g. overwrite it with `'#'`), recurse into the four neighboring cells, then restore the cell afterward (standard backtracking).
6. As an optimization, prune Trie leaves with no remaining children after a word is found, so future DFS calls stop exploring dead-end branches sooner.

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

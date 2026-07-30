# 211. Design Add and Search Words Data Structure

**Difficulty:** Medium
**Topics:** String, Depth-First Search, Design, Trie
**Common companies:** Google, Meta
**Category (README):** 7.3 Trie (Prefix Tree)

## Problem Description

Design a data structure that supports adding new words and finding if a string matches any previously added string.

Implement the `WordDictionary` class:

	
- `WordDictionary()` Initializes the object.

	
- `void addWord(word)` Adds `word` to the data structure, it can be matched later.

	
- `bool search(word)` Returns `true` if there is any string in the data structure that matches `word` or `false` otherwise. `word` may contain dots `'.'` where dots can be matched with any letter.

 

**Example:**

```

**Input**
["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
**Output**
[null,null,null,null,false,true,true,true]

**Explanation**
WordDictionary wordDictionary = new WordDictionary();
wordDictionary.addWord("bad");
wordDictionary.addWord("dad");
wordDictionary.addWord("mad");
wordDictionary.search("pad"); // return False
wordDictionary.search("bad"); // return True
wordDictionary.search(".ad"); // return True
wordDictionary.search("b.."); // return True

```

 

**Constraints:**

	
- `1 <= word.length <= 25`

	
- `word` in `addWord` consists of lowercase English letters.

	
- `word` in `search` consist of `'.'` or lowercase English letters.

	
- There will be at most `2` dots in `word` for `search` queries.

	
- At most `104` calls will be made to `addWord` and `search`.

## Key Idea

Trie + DFS to handle the `.` wildcard

## Approach

1. Identify the core pattern for this category: **7.3 Trie (Prefix Tree)**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/design-add-and-search-words-data-structure/

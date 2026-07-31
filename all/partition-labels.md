# 763. Partition Labels

**Difficulty:** Medium
**Topics:** Hash Table, Two Pointers, String, Greedy
**Common companies:** Amazon, Google
**Category (README):** 13. Greedy

## Problem Description

You are given a string `s`. We want to partition the string into as many parts as possible so that each letter appears in at most one part. For example, the string `"ababcc"` can be partitioned into `["abab", "cc"]`, but partitions such as `["aba", "bcc"]` or `["ab", "ab", "cc"]` are invalid.

Note that the partition is done so that after concatenating all the parts in order, the resultant string should be `s`.

Return *a list of integers representing the size of these parts*.

 

**Example 1:**

```

**Input:** s = "ababcbacadefegdehijhklij"
**Output:** [9,7,8]
**Explanation:**
The partition is "ababcbaca", "defegde", "hijhklij".
This is a partition so that each letter appears in at most one part.
A partition like "ababcbacadefegde", "hijhklij" is incorrect, because it splits s into less parts.

```

**Example 2:**

```

**Input:** s = "eccbbbbdec"
**Output:** [10]

```

 

**Constraints:**

	
- `1 <= s.length <= 500`

	
- `s` consists of lowercase English letters.

## Key Idea

Record each character's last occurrence, greedily extend the interval

## Approach

This is solved with a **greedy sweep using last-occurrence indices**:

1. Precompute, for every character, the index of its last occurrence in `s` using a hash map.
2. Sweep through `s` while tracking `start` (the beginning of the current partition) and `end` (the farthest last-occurrence seen so far within the current partition).
3. For each character at index `i`, extend `end = max(end, last[ch])`, since that character must not appear again after the partition closes.
4. Whenever `i == end`, the current partition can safely close here (every character seen so far has its last occurrence within `[start, end]`): record its length `end - start + 1` and start a new partition at `i + 1`.
5. Return the list of recorded partition lengths.

**Time Complexity:** O(n) — one pass to record last occurrences, one pass to build partitions.
**Space Complexity:** O(1) — the last-occurrence map holds at most 26 lowercase letters.

## Reference Solution (Python)

```python
from typing import List

def partitionLabels(s: str) -> List[int]:
    last = {ch: i for i, ch in enumerate(s)}
    result = []
    start = end = 0

    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            result.append(end - start + 1)
            start = i + 1

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/partition-labels/

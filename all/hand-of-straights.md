# 846. Hand of Straights

**Difficulty:** Medium
**Topics:** Array, Hash Table, Greedy, Sorting
**Common companies:** Google, Amazon
**Category (README):** 13. Greedy

## Problem Description

Alice has some number of cards and she wants to rearrange the cards into groups so that each group is of size `groupSize`, and consists of `groupSize` consecutive cards.

Given an integer array `hand` where `hand[i]` is the value written on the `ith` card and an integer `groupSize`, return `true` if she can rearrange the cards, or `false` otherwise.

 

**Example 1:**

```

**Input:** hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
**Output:** true
**Explanation:** Alice's hand can be rearranged as [1,2,3],[2,3,4],[6,7,8]

```

**Example 2:**

```

**Input:** hand = [1,2,3,4,5], groupSize = 4
**Output:** false
**Explanation:** Alice's hand can not be rearranged into groups of 4.

```

 

**Constraints:**

	
- `1 <= hand.length <= 104`

	
- `0 <= hand[i] <= 109`

	
- `1 <= groupSize <= hand.length`

 

**Note:** This question is the same as 1296: https://leetcode.com/problems/divide-array-in-sets-of-k-consecutive-numbers/

## Key Idea

Sort + hash-map counting for greedy group formation

## Approach

This is solved with **a greedy pass over sorted card values, always starting a group at the smallest remaining card**:

1. If `len(hand)` isn't divisible by `groupSize`, no valid grouping is possible, so return `False` immediately.
2. Count the occurrences of each card value with a `Counter`.
3. Process distinct card values in ascending order; whenever a value still has a positive remaining count, it must be the start of a new group of `groupSize` consecutive cards (since it's the smallest value left).
4. For that group, consume one occurrence each of `card, card + 1, ..., card + groupSize - 1` from the counts; if any required value is missing or has count 0, return `False`.
5. If all values are consumed successfully, return `True`.

**Time Complexity:** O(n log n) — dominated by sorting the distinct card values; the greedy pass over counts is O(n).
**Space Complexity:** O(n) — for the frequency map.

## Reference Solution (Python)

```python
from collections import Counter


def isNStraightHand(hand: list[int], groupSize: int) -> bool:
    if len(hand) % groupSize != 0:
        return False

    count = Counter(hand)

    for card in sorted(count):
        need = count[card]
        if need <= 0:
            continue
        for start in range(card, card + groupSize):
            if count[start] < need:
                return False
            count[start] -= need

    return True
```

## Reference

- LeetCode: https://leetcode.com/problems/hand-of-straights/

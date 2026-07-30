# 705. Design HashSet

**Difficulty:** Easy
**Topics:** Array, Hash Table, Linked List, Design, Hash Function
**Common companies:** Google, Amazon
**Category (README):** 6. Hash Table

## Problem Description

Design a HashSet without using any built-in hash table libraries.

Implement `MyHashSet` class:

	
- `void add(key)` Inserts the value `key` into the HashSet.

	
- `bool contains(key)` Returns whether the value `key` exists in the HashSet or not.

	
- `void remove(key)` Removes the value `key` in the HashSet. If `key` does not exist in the HashSet, do nothing.

 

**Example 1:**

```

**Input**
["MyHashSet", "add", "add", "contains", "contains", "add", "contains", "remove", "contains"]
[[], [1], [2], [1], [3], [2], [2], [2], [2]]
**Output**
[null, null, null, true, false, null, true, null, false]

**Explanation**
MyHashSet myHashSet = new MyHashSet();
myHashSet.add(1);      // set = [1]
myHashSet.add(2);      // set = [1, 2]
myHashSet.contains(1); // return True
myHashSet.contains(3); // return False, (not found)
myHashSet.add(2);      // set = [1, 2]
myHashSet.contains(2); // return True
myHashSet.remove(2);   // set = [1]
myHashSet.contains(2); // return False, (already removed)
```

 

**Constraints:**

	
- `0 <= key <= 106`

	
- At most `104` calls will be made to `add`, `remove`, and `contains`.

## Key Idea

Array + linked list for collision handling (chaining)

## Approach

1. Identify the core pattern for this category: **6. Hash Table**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(1) average per operation — assuming a good hash spread, each bucket holds O(n / capacity) entries.
**Space Complexity:** O(n + capacity) — one fixed-size bucket array plus the stored keys.

## Reference Solution (Python)

```python
class MyHashSet:
    def __init__(self):
        self.capacity = 1000
        self.buckets: list[list[int]] = [[] for _ in range(self.capacity)]

    def _hash(self, key: int) -> int:
        return key % self.capacity

    def add(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        if key not in bucket:
            bucket.append(key)

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        if key in bucket:
            bucket.remove(key)

    def contains(self, key: int) -> bool:
        bucket = self.buckets[self._hash(key)]
        return key in bucket
```

## Reference

- LeetCode: https://leetcode.com/problems/design-hashset/

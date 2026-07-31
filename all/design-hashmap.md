# 706. Design HashMap

**Difficulty:** Easy
**Topics:** Array, Hash Table, Linked List, Design, Hash Function
**Common companies:** Google, Amazon
**Category (README):** 6. Hash Table

## Problem Description

Design a HashMap without using any built-in hash table libraries.

Implement the `MyHashMap` class:

	
- `MyHashMap()` initializes the object with an empty map.

	
- `void put(int key, int value)` inserts a `(key, value)` pair into the HashMap. If the `key` already exists in the map, update the corresponding `value`.

	
- `int get(int key)` returns the `value` to which the specified `key` is mapped, or `-1` if this map contains no mapping for the `key`.

	
- `void remove(key)` removes the `key` and its corresponding `value` if the map contains the mapping for the `key`.

 

**Example 1:**

```

**Input**
["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"]
[[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
**Output**
[null, null, null, 1, -1, null, 1, null, -1]

**Explanation**
MyHashMap myHashMap = new MyHashMap();
myHashMap.put(1, 1); // The map is now [[1,1]]
myHashMap.put(2, 2); // The map is now [[1,1], [2,2]]
myHashMap.get(1);    // return 1, The map is now [[1,1], [2,2]]
myHashMap.get(3);    // return -1 (i.e., not found), The map is now [[1,1], [2,2]]
myHashMap.put(2, 1); // The map is now [[1,1], [2,1]] (i.e., update the existing value)
myHashMap.get(2);    // return 1, The map is now [[1,1], [2,1]]
myHashMap.remove(2); // remove the mapping for 2, The map is now [[1,1]]
myHashMap.get(2);    // return -1 (i.e., not found), The map is now [[1,1]]

```

 

**Constraints:**

	
- `0 <= key, value <= 106`

	
- At most `104` calls will be made to `put`, `get`, and `remove`.

## Key Idea

Array + linked list for collision handling (chaining)

## Approach

This is solved with **a fixed-size bucket array with chaining for collisions**:

1. Allocate `capacity` buckets, each an empty list that will hold `[key, value]` pairs that hash to it.
2. Hash a key with simple modulo: `key % capacity`.
3. `put` scans the target bucket for an existing pair with that key to update in place; if not found, appends a new `[key, value]` pair.
4. `get` scans the target bucket linearly for a matching key and returns its value, or `-1` if no pair matches.
5. `remove` scans the target bucket for a matching key and pops it out if found.

**Time Complexity:** O(1) average per operation — assuming a good hash spread, each bucket holds O(n / capacity) entries.
**Space Complexity:** O(n + capacity) — one fixed-size bucket array plus the stored key-value pairs.

## Reference Solution (Python)

```python
class MyHashMap:
    def __init__(self):
        self.capacity = 1000
        self.buckets: list[list[list[int]]] = [[] for _ in range(self.capacity)]

    def _hash(self, key: int) -> int:
        return key % self.capacity

    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[self._hash(key)]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])

    def get(self, key: int) -> int:
        bucket = self.buckets[self._hash(key)]
        for k, v in bucket:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                return
```

## Reference

- LeetCode: https://leetcode.com/problems/design-hashmap/

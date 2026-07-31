# 460. LFU Cache

**Difficulty:** Hard
**Topics:** Hash Table, Linked List, Design, Doubly-Linked List
**Common companies:** Amazon, Google
**Category (README):** 15. Design Problems

## Problem Description

Design and implement a data structure for a Least Frequently Used (LFU) cache.

Implement the `LFUCache` class:

	
- `LFUCache(int capacity)` Initializes the object with the `capacity` of the data structure.

	
- `int get(int key)` Gets the value of the `key` if the `key` exists in the cache. Otherwise, returns `-1`.

	
- `void put(int key, int value)` Update the value of the `key` if present, or inserts the `key` if not already present. When the cache reaches its `capacity`, it should invalidate and remove the **least frequently used** key before inserting a new item. For this problem, when there is a **tie** (i.e., two or more keys with the same frequency), the **least recently used** `key` would be invalidated.

To determine the least frequently used key, a **use counter** is maintained for each key in the cache. The key with the smallest **use counter** is the least frequently used key.

When a key is first inserted into the cache, its **use counter** is set to `1` (due to the `put` operation). The **use counter** for a key in the cache is incremented either a `get` or `put` operation is called on it.

The functions `get` and `put` must each run in `O(1)` average time complexity.

 

**Example 1:**

```

**Input**
["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
**Output**
[null, null, null, 1, null, -1, 3, null, -1, 3, 4]

**Explanation**
// cnt(x) = the use counter for key x
// cache=[] will show the last used order for tiebreakers (leftmost element is  most recent)
LFUCache lfu = new LFUCache(2);
lfu.put(1, 1);   // cache=[1,_], cnt(1)=1
lfu.put(2, 2);   // cache=[2,1], cnt(2)=1, cnt(1)=1
lfu.get(1);      // return 1
                 // cache=[1,2], cnt(2)=1, cnt(1)=2
lfu.put(3, 3);   // 2 is the LFU key because cnt(2)=1 is the smallest, invalidate 2.
                 // cache=[3,1], cnt(3)=1, cnt(1)=2
lfu.get(2);      // return -1 (not found)
lfu.get(3);      // return 3
                 // cache=[3,1], cnt(3)=2, cnt(1)=2
lfu.put(4, 4);   // Both 1 and 3 have the same cnt, but 1 is LRU, invalidate 1.
                 // cache=[4,3], cnt(4)=1, cnt(3)=2
lfu.get(1);      // return -1 (not found)
lfu.get(3);      // return 3
                 // cache=[3,4], cnt(4)=1, cnt(3)=3
lfu.get(4);      // return 4
                 // cache=[4,3], cnt(4)=2, cnt(3)=3

```

 

**Constraints:**

	
- `1 <= capacity <= 104`

	
- `0 <= key <= 105`

	
- `0 <= value <= 109`

	
- At most `2 * 105` calls will be made to `get` and `put`.

## Key Idea

Hash map + frequency-bucketed doubly linked lists

## Approach

This is solved with **three hash maps plus per-frequency ordered dictionaries for O(1) LRU tiebreaking**:

1. Track `key_to_val` and `key_to_freq` for O(1) value/frequency lookups, and `freq_to_keys` mapping each frequency to an `OrderedDict` of keys at that frequency (insertion order gives LRU order within a frequency bucket).
2. Track `min_freq`, the smallest frequency currently in use, so eviction is O(1).
3. On `get`/`put` of an existing key, call `_touch`: remove the key from its current frequency bucket (bumping `min_freq` if that bucket becomes empty and was the minimum), then reinsert it into the `freq + 1` bucket.
4. On `put` of a new key when the cache is full, evict the least-recently-used key from `freq_to_keys[min_freq]` via `popitem(last=False)`.
5. Insert the new key with frequency `1` and reset `min_freq` to `1`.

**Time Complexity:** O(1) average per `get` and `put` — hash map lookups plus `OrderedDict` insert/pop/move operations are all O(1).
**Space Complexity:** O(capacity) — for the key-to-value map, key-to-frequency map, and the frequency-bucketed ordered dictionaries.

## Reference Solution (Python)

```python
from collections import OrderedDict, defaultdict


class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val: dict[int, int] = {}
        self.key_to_freq: dict[int, int] = {}
        self.freq_to_keys: dict[int, OrderedDict] = defaultdict(OrderedDict)

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        self._touch(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._touch(key)
            return

        if len(self.key_to_val) >= self.capacity:
            oldest_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[oldest_key]
            del self.key_to_freq[oldest_key]

        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1

    def _touch(self, key: int) -> None:
        freq = self.key_to_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq] and freq == self.min_freq:
            self.min_freq += 1

        new_freq = freq + 1
        self.key_to_freq[key] = new_freq
        self.freq_to_keys[new_freq][key] = None
```

## Reference

- LeetCode: https://leetcode.com/problems/lfu-cache/

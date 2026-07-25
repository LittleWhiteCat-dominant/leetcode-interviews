# 146. LRU Cache

**Difficulty:** Medium
**Topics:** Design, Hash Table, Linked List, Doubly-Linked List
**Category warm-up for:** Design (explicitly tagged "Universal favorite at every company" in `basic_en.md`)

## Problem Description

Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**.

Implement the `LRUCache` class:

- `LRUCache(int capacity)`: Initialize the LRU cache with **positive size** `capacity`.
- `int get(int key)`: Return the value of the `key` if the key exists, otherwise return `-1`.
- `void put(int key, int value)`: Update the value of the `key` if the `key` exists. Otherwise, add the `key-value` pair to the cache. If the number of keys exceeds the `capacity` from this operation, **evict** the least recently used key.

The functions `get` and `put` must each run in **O(1)** average time complexity.

## Example

```
Input:
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]

Output:
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation:
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4
```

## Constraints

- `1 <= capacity <= 3000`
- `0 <= key <= 10^4`
- `0 <= value <= 10^5`
- At most `2 * 10^5` calls will be made to `get` and `put`.

## Approach

1. Use a **hash map** (`key -> node`) for O(1) lookup, combined with a **doubly linked list** that maintains recency order (most recently used at the head, least recently used at the tail).
2. On `get(key)`: if the key exists, move its node to the head of the list (mark as most recently used) and return its value; otherwise return `-1`.
3. On `put(key, value)`:
   - If the key exists, update its value and move the node to the head.
   - If the key doesn't exist, create a new node, insert it at the head, and add it to the hash map. If capacity is exceeded, remove the node at the tail (least recently used) and delete it from the hash map.
4. Use two dummy sentinel nodes (`head` and `tail`) to simplify insertion/removal edge cases at the boundaries of the list.

**Time Complexity:** O(1) for both `get` and `put`.
**Space Complexity:** O(capacity).

## Reference Solution (Python)

```python
class Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: "Node | None" = None
        self.next: "Node | None" = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, Node] = {}
        # Sentinel head/tail to avoid null checks at the list boundaries.
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_head(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_at_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._insert_at_head(node)
            return

        if len(self.cache) >= self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

        node = Node(key, value)
        self.cache[key] = node
        self._insert_at_head(node)
```

## Follow-up Questions Interviewers May Ask

- How would you make this thread-safe for concurrent access?
- How would you implement an LFU (Least Frequently Used) cache instead (LC 460)?
- How would you add a TTL (time-to-live) expiration to cache entries?

# 432. All O`one Data Structure

**Difficulty:** Hard
**Topics:** Hash Table, Linked List, Design, Doubly-Linked List
**Common companies:** Google
**Category (README):** 15. Design Problems

## Problem Description

Design a data structure to store the strings' count with the ability to return the strings with minimum and maximum counts.

Implement the `AllOne` class:

	
- `AllOne()` Initializes the object of the data structure.

	
- `inc(String key)` Increments the count of the string `key` by `1`. If `key` does not exist in the data structure, insert it with count `1`.

	
- `dec(String key)` Decrements the count of the string `key` by `1`. If the count of `key` is `0` after the decrement, remove it from the data structure. It is guaranteed that `key` exists in the data structure before the decrement.

	
- `getMaxKey()` Returns one of the keys with the maximal count. If no element exists, return an empty string `""`.

	
- `getMinKey()` Returns one of the keys with the minimum count. If no element exists, return an empty string `""`.

**Note** that each function must run in `O(1)` average time complexity.

 

**Example 1:**

```

**Input**
["AllOne", "inc", "inc", "getMaxKey", "getMinKey", "inc", "getMaxKey", "getMinKey"]
[[], ["hello"], ["hello"], [], [], ["leet"], [], []]
**Output**
[null, null, null, "hello", "hello", null, "hello", "leet"]

**Explanation**
AllOne allOne = new AllOne();
allOne.inc("hello");
allOne.inc("hello");
allOne.getMaxKey(); // return "hello"
allOne.getMinKey(); // return "hello"
allOne.inc("leet");
allOne.getMaxKey(); // return "hello"
allOne.getMinKey(); // return "leet"

```

 

**Constraints:**

	
- `1 <= key.length <= 10`

	
- `key` consists of lowercase English letters.

	
- It is guaranteed that for each call to `dec`, `key` is existing in the data structure.

	
- At most `5 * 104` calls will be made to `inc`, `dec`, `getMaxKey`, and `getMinKey`.

## Key Idea

Hash map + doubly linked list bucketed by count

## Approach

1. Identify the core pattern for this category: **15. Design Problems**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(1) average — every operation (`inc`, `dec`, `getMaxKey`, `getMinKey`) does a constant amount of bucket-list and set bookkeeping.
**Space Complexity:** O(n) — to store the n distinct keys and their buckets.

## Reference Solution (Python)

```python
class Bucket:
    __slots__ = ("count", "keys", "prev", "next")

    def __init__(self, count: int):
        self.count = count
        self.keys: set[str] = set()
        self.prev: "Bucket | None" = None
        self.next: "Bucket | None" = None


class AllOne:
    def __init__(self):
        self.head = Bucket(0)
        self.tail = Bucket(0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.key_to_bucket: dict[str, Bucket] = {}

    def _insert_after(self, node: Bucket, new_count: int) -> Bucket:
        bucket = Bucket(new_count)
        bucket.prev = node
        bucket.next = node.next
        node.next.prev = bucket
        node.next = bucket
        return bucket

    def _remove(self, node: Bucket) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def inc(self, key: str) -> None:
        if key not in self.key_to_bucket:
            bucket = self.head
        else:
            bucket = self.key_to_bucket[key]
            bucket.keys.remove(key)

        next_bucket = bucket.next
        if next_bucket is self.tail or next_bucket.count != bucket.count + 1:
            next_bucket = self._insert_after(bucket, bucket.count + 1)
        next_bucket.keys.add(key)
        self.key_to_bucket[key] = next_bucket

        if bucket is not self.head and not bucket.keys:
            self._remove(bucket)

    def dec(self, key: str) -> None:
        bucket = self.key_to_bucket[key]
        bucket.keys.remove(key)

        if bucket.count == 1:
            del self.key_to_bucket[key]
        else:
            prev_bucket = bucket.prev
            if prev_bucket is self.head or prev_bucket.count != bucket.count - 1:
                prev_bucket = self._insert_after(prev_bucket, bucket.count - 1)
            prev_bucket.keys.add(key)
            self.key_to_bucket[key] = prev_bucket

        if not bucket.keys:
            self._remove(bucket)

    def getMaxKey(self) -> str:
        if self.tail.prev is self.head:
            return ""
        return next(iter(self.tail.prev.keys))

    def getMinKey(self) -> str:
        if self.head.next is self.tail:
            return ""
        return next(iter(self.head.next.keys))
```

## Reference

- LeetCode: https://leetcode.com/problems/all-oone-data-structure/

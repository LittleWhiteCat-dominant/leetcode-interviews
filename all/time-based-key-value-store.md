# 981. Time Based Key-Value Store

**Difficulty:** Medium
**Topics:** Hash Table, String, Binary Search, Design
**Common companies:** Google, Amazon
**Category (README):** 1.4 Binary Search

## Problem Description

Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

Implement the `TimeMap` class:

	
- `TimeMap()` Initializes the object of the data structure.

	
- `void set(String key, String value, int timestamp)` Stores the key `key` with the value `value` at the given time `timestamp`.

	
- `String get(String key, int timestamp)` Returns a value such that `set` was called previously, with `timestamp_prev <= timestamp`. If there are multiple such values, it returns the value associated with the largest `timestamp_prev`. If there are no values, it returns `""`.

 

**Example 1:**

```

**Input**
["TimeMap", "set", "get", "get", "set", "get", "get"]
[[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
**Output**
[null, null, "bar", "bar", null, "bar2", "bar2"]

**Explanation**
TimeMap timeMap = new TimeMap();
timeMap.set("foo", "bar", 1);  // store the key "foo" and value "bar" along with timestamp = 1.
timeMap.get("foo", 1);         // return "bar"
timeMap.get("foo", 3);         // return "bar", since there is no value corresponding to foo at timestamp 3 and timestamp 2, then the only value is at timestamp 1 is "bar".
timeMap.set("foo", "bar2", 4); // store the key "foo" and value "bar2" along with timestamp = 4.
timeMap.get("foo", 4);         // return "bar2"
timeMap.get("foo", 5);         // return "bar2"

```

 

**Constraints:**

	
- `1 <= key.length, value.length <= 100`

	
- `key` and `value` consist of lowercase English letters and digits.

	
- `1 <= timestamp <= 107`

	
- All the timestamps `timestamp` of `set` are strictly increasing.

	
- At most `2 * 105` calls will be made to `set` and `get`.

## Key Idea

Timestamps stored in order, binary search + design

## Approach

This is solved with **per-key sorted timestamp lists searched via binary search**:

1. For each key, maintain two parallel lists: `timestamps` (kept in increasing order, since `set` calls arrive with strictly increasing timestamps) and `values`.
2. On `set`, simply append the new timestamp and value to that key's lists in O(1).
3. On `get`, if the key has never been set, return `""`.
4. Otherwise use `bisect_right` on the key's timestamp list to find the insertion point for the query timestamp, then step back one index to get the largest stored timestamp that is `<=` the query.
5. If that index is valid (`>= 0`), return the corresponding value; otherwise return `""` since no stored timestamp qualifies.

**Time Complexity:** `set` is O(1) amortized; `get` is O(log m) where `m` is the number of timestamps stored for that key, via binary search.
**Space Complexity:** O(N) — where `N` is the total number of `set` calls made across all keys.

## Reference Solution (Python)

```python
from bisect import bisect_right
from collections import defaultdict


class TimeMap:
    def __init__(self):
        self.timestamps: dict[str, list[int]] = defaultdict(list)
        self.values: dict[str, list[str]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.timestamps[key].append(timestamp)
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        times = self.timestamps.get(key)
        if not times:
            return ""

        idx = bisect_right(times, timestamp) - 1
        return self.values[key][idx] if idx >= 0 else ""
```

## Reference

- LeetCode: https://leetcode.com/problems/time-based-key-value-store/

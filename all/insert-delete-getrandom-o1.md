# 380. Insert Delete GetRandom O(1)

**Difficulty:** Medium
**Topics:** Array, Hash Table, Math, Design, Randomized
**Common companies:** All big tech
**Category (README):** 6. Hash Table

## Problem Description

Implement the `RandomizedSet` class:

	
- `RandomizedSet()` Initializes the `RandomizedSet` object.

	
- `bool insert(int val)` Inserts an item `val` into the set if not present. Returns `true` if the item was not present, `false` otherwise.

	
- `bool remove(int val)` Removes an item `val` from the set if present. Returns `true` if the item was present, `false` otherwise.

	
- `int getRandom()` Returns a random element from the current set of elements (it's guaranteed that at least one element exists when this method is called). Each element must have the **same probability** of being returned.

You must implement the functions of the class such that each function works in **average** `O(1)` time complexity.

 

**Example 1:**

```

**Input**
["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
[[], [1], [2], [2], [], [1], [2], []]
**Output**
[null, true, false, true, 2, true, false, 2]

**Explanation**
RandomizedSet randomizedSet = new RandomizedSet();
randomizedSet.insert(1); // Inserts 1 to the set. Returns true as 1 was inserted successfully.
randomizedSet.remove(2); // Returns false as 2 does not exist in the set.
randomizedSet.insert(2); // Inserts 2 to the set, returns true. Set now contains [1,2].
randomizedSet.getRandom(); // getRandom() should return either 1 or 2 randomly.
randomizedSet.remove(1); // Removes 1 from the set, returns true. Set now contains [2].
randomizedSet.insert(2); // 2 was already in the set, so return false.
randomizedSet.getRandom(); // Since 2 is the only number in the set, getRandom() will always return 2.

```

 

**Constraints:**

	
- `-231 <= val <= 231 - 1`

	
- At most `2 * ``105` calls will be made to `insert`, `remove`, and `getRandom`.

	
- There will be **at least one** element in the data structure when `getRandom` is called.

## Key Idea

Hash map + dynamic array, swap-to-end for deletion

## Approach

This is solved with **a dynamic array paired with a hash map of value-to-index, using swap-with-last for deletion**:

1. Store all elements in a list `values` (enabling O(1) random access for `getRandom`) and mirror each value's position in a dict `index` (enabling O(1) lookup).
2. `insert(val)`: if already present return `False`; otherwise record its index and append it to `values`.
3. `remove(val)`: if absent return `False`; otherwise overwrite the target's slot with the last element in `values`, update that moved element's index, then pop the now-duplicated last slot and delete the removed value's index entry — this avoids an O(n) shift.
4. `getRandom()` simply returns `random.choice(values)`, which is O(1) since `values` is a plain array.

**Time Complexity:** O(1) average for `insert`, `remove`, and `getRandom`.
**Space Complexity:** O(n) — the array and the hash map both hold up to `n` elements.

## Reference Solution (Python)

```python
import random


class RandomizedSet:
    def __init__(self):
        self.values: list[int] = []
        self.index: dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self.index:
            return False
        self.index[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.index:
            return False
        idx = self.index[val]
        last_val = self.values[-1]
        self.values[idx] = last_val
        self.index[last_val] = idx
        self.values.pop()
        del self.index[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.values)
```

## Reference

- LeetCode: https://leetcode.com/problems/insert-delete-getrandom-o1/

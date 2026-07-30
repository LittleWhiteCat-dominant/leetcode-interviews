# LeetCode Frequently-Asked Problems by Data Structure (North America Interview Edition)

> This summary is calibrated against **real high-frequency questions from North American (US/Canada) big-tech interviews**, drawing mainly on NeetCode 150, Grind 75/169, Blind 75, 2026 LeetCode Company Tag frequency data, and interview reports from Meta/Google/Amazon candidates. The primary classification axis is still **the core data structure required to solve each problem**. A few pure algorithmic-paradigm sections ("Backtracking", "Greedy", "Bit Manipulation & Math") have been added, and each problem is annotated with the companies that ask it most often so you can target your practice by company.

## Table of Contents

0. [North American Big-Tech Interview Formats at a Glance](#0-north-american-big-tech-interview-formats-at-a-glance)
1. [Array](#1-array)
2. [String](#2-string)
3. [Linked List](#3-linked-list)
4. [Stack](#4-stack)
5. [Queue / Monotonic Queue](#5-queue--monotonic-queue)
6. [Hash Table](#6-hash-table)
7. [Tree](#7-tree)
8. [Heap / Priority Queue](#8-heap--priority-queue)
9. [Graph](#9-graph)
10. [Union Find](#10-union-find)
11. [Backtracking](#11-backtracking)
12. [Dynamic Programming (Array/Table Based)](#12-dynamic-programming-arraytable-based)
13. [Greedy](#13-greedy)
14. [Bit Manipulation & Math](#14-bit-manipulation--math)
15. [Design Problems](#15-design-problems)
16. [Company-Specific High-Frequency Lists](#16-company-specific-high-frequency-lists)
17. [Recommended Study Order](#17-recommended-study-order)

---

## 0. North American Big-Tech Interview Formats at a Glance

| Company | Problems / Round | Duration | Platform | Difficulty Trend | Hot Topics | Notes |
|---|---|---|---|---|---|---|
| Google | 1-2 problems + escalating follow-ups | 45 min | Google Docs (no IDE, no execution) | Medium → Medium-Hard (deepens via follow-ups) | Graphs, Trees, DP | Follow-up escalation is the core mechanic, testing real-time reasoning (GCA) |
| Meta | Fixed 2 problems | 35 min | CoderPad (no execution) | Medium-Hard | Arrays/Strings, Trees, Graphs | Highly recycled question pool — focus on LeetCode's "Meta" company-tagged problems from the last 3 months |
| Amazon | 1 problem + LP behavioral | 60 min (coding ~40 min) | OA: CodeSignal (runs code) / Onsite: CoderPad | Medium-Hard | Trees, Graphs, Arrays | OA includes a "find the bug" debugging round; onsite coding time must leave room for the behavioral portion |
| Netflix | 1-2 applied problems | 45-60 min | CoderPad (no execution) | Hard (close to real systems) | Concurrency, interval scheduling, cache design | Coding carries the lowest weight in the overall loop, but problems are the most applied/realistic |
| Apple | 1 domain-specific problem | 45-60 min | Varies by team | Medium (but code quality matters) | Depends on team (iOS/Maps/backend, etc.) | Explicitly grades code style, naming, and edge-case handling |

**10 patterns that cover ~80% of interview questions**: Two Pointers, Sliding Window, BFS, DFS/Backtracking, Dynamic Programming, Heap/Top-K, Binary Search, Monotonic Stack, Union Find, Trie. Practice until you can name the applicable pattern immediately after reading the problem statement, before writing any code.

---

## 1. Array

Arrays are the most fundamental linear structure — focus on **index movement, interval partitioning, and in-place operations**. Common techniques: two pointers, sliding window, prefix sum, binary search, interval merging, matrix traversal.

### 1.1 Two Pointers

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 1 | [Two Sum](./warm-up/two-sum.md) | Easy | Hash map storing value→index | Universal warmup at every company |
| 167 | [Two Sum II - Input Array Is Sorted](./all/two-sum-ii-input-array-is-sorted.md) | Medium | Left/right pointers instead of a hash map, O(1) space | Amazon, Google |
| 15 | [3Sum](./all/3sum.md) | Medium | Sort + fix one number + two pointers with dedup | All big tech |
| 11 | [Container With Most Water](./all/container-with-most-water.md) | Medium | Move the shorter side inward | All big tech |
| 42 | [Trapping Rain Water](./all/trapping-rain-water.md) | Hard | Two pointers tracking left/right max height, or monotonic stack | Amazon, Google |
| 26/27/283 | [Remove Duplicates](./all/remove-duplicates-from-sorted-array.md) / [Remove Element](./all/remove-element.md) / [Move Zeroes](./all/move-zeroes.md) | Easy/Easy/Easy | Fast/slow pointers overwriting in place | Amazon, Apple |
| 88 | [Merge Sorted Array](./all/merge-sorted-array.md) | Easy | Merge back-to-front with two pointers to avoid overwrites | Amazon, Meta |
| 75 | [Sort Colors](./all/sort-colors.md) | Medium | Three-pointer Dutch National Flag problem | Google, Meta |
| 125 | [Valid Palindrome](./rivian/valid-palindrome.md) | Easy | Two pointers skipping non-alphanumeric characters | Meta, Apple |
| 680 | [Valid Palindrome II](./all/valid-palindrome-ii.md) | Easy | Allow skipping one mismatched character then re-verify | **Meta favorite** |

### 1.2 Sliding Window

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 121 | [Best Time to Buy and Sell Stock](./warm-up/best-time-to-buy-and-sell-stock.md) | Easy | Single pass tracking the running minimum price | Universal warmup at every company |
| 3 | [Longest Substring Without Repeating Characters](./all/longest-substring-without-repeating-characters.md) | Medium | Hash map inside the window tracking last-seen index | All big tech |
| 76 | [Minimum Window Substring](./all/minimum-window-substring.md) | Hard | Counted window, shrink to find the minimal valid window | **Meta, Amazon favorite** |
| 209 | [Minimum Size Subarray Sum](./all/minimum-size-subarray-sum.md) | Medium | Shrink the left pointer once the window sum exceeds target | Amazon |
| 239 | [Sliding Window Maximum](./asana/sliding-window-maximum.md) | Hard | Monotonic deque tracking the window maximum | Amazon, Google |
| 438 | [Find All Anagrams in a String](./all/find-all-anagrams-in-a-string.md) | Medium | Fixed-size window + character frequency comparison | Google, Meta |
| 424 | [Longest Repeating Character Replacement](./all/longest-repeating-character-replacement.md) | Medium | Window allowing up to k replacements | Google, Meta |
| 567 | [Permutation in String](./all/permutation-in-string.md) | Medium | Fixed-size window + character frequency comparison | **Meta favorite** |

### 1.3 Prefix Sum

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 53 | [Maximum Subarray](./warm-up/maximum-subarray.md) | Medium | Kadane's algorithm | All big tech |
| 152 | [Maximum Product Subarray](./asana/maximum-product-subarray.md) | Medium | Track running max and min product simultaneously | Amazon, Google |
| 238 | [Product of Array Except Self](./asana/product-of-array-except-self.md) | Medium | Prefix product × suffix product, no division allowed | **Meta, Apple favorite** |
| 560 | [Subarray Sum Equals K](./all/subarray-sum-equals-k.md) | Medium | Prefix sum + hash map counting occurrences | **Meta favorite** |
| 528 | [Random Pick with Weight](./all/random-pick-with-weight.md) | Medium | Prefix sum + binary search to locate the interval | **Meta favorite** |
| 303/304 | [Range Sum Query](./all/range-sum-query-immutable.md) / [Range Sum Query 2D](./all/range-sum-query-2d-immutable.md) | Easy/Medium | 1D/2D prefix sum array | Google, Amazon |

### 1.4 Binary Search

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 704 | [Binary Search](./all/binary-search.md) | Easy | Basic template | All big tech |
| 33 | [Search in Rotated Sorted Array](./all/search-in-rotated-sorted-array.md) | Medium | Determine which half is sorted to decide the shrink direction | All big tech |
| 153 | [Find Minimum in Rotated Sorted Array](./all/find-minimum-in-rotated-sorted-array.md) | Medium | Compare with the right endpoint to shrink the interval | **Meta favorite** |
| 34 | [Find First and Last Position of Element in Sorted Array](./all/find-first-and-last-position-of-element-in-sorted-array.md) | Medium | Two binary searches for left/right boundaries | Google, Amazon |
| 4 | [Median of Two Sorted Arrays](./all/median-of-two-sorted-arrays.md) | Hard | Binary search for the k-th smallest element | Google (L5+ favorite) |
| 74/240 | [Search a 2D Matrix](./all/search-a-2d-matrix.md) / [Search a 2D Matrix II](./all/search-a-2d-matrix-ii.md) | Medium/Medium | Flatten to 1D binary search or start from a corner with two pointers | Amazon, Apple |
| 875 | [Koko Eating Bananas](./all/koko-eating-bananas.md) | Medium | Binary search on the answer + a feasibility check function | Google, Amazon |
| 1011 | [Capacity To Ship Packages Within D Days](./all/capacity-to-ship-packages-within-d-days.md) | Medium | Binary search on the answer | Amazon |
| 981 | [Time Based Key-Value Store](./all/time-based-key-value-store.md) | Medium | Timestamps stored in order, binary search + design | Google, Amazon |

### 1.5 Intervals

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 56 | [Merge Intervals](./rivian/merge-intervals.md) | Medium | Sort by left endpoint, then merge linearly | All big tech |
| 57 | [Insert Interval](./all/insert-interval.md) | Medium | Find the insertion point and merge overlapping intervals | All big tech |
| 435 | [Non-overlapping Intervals](./all/non-overlapping-intervals.md) | Medium | Sort by right endpoint, greedy selection | Amazon, Google |
| 252/253 | [Meeting Rooms I](./all/meeting-rooms.md) / [II](./asana/meeting-rooms-ii.md) | Easy/Medium | Sort + sweep line / min-heap | All big tech |

### 1.6 Matrix

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 54 | [Spiral Matrix](./all/spiral-matrix.md) | Medium | Maintain top/bottom/left/right boundaries, shrinking layer by layer | All big tech |
| 48 | [Rotate Image](./all/rotate-image.md) | Medium | Transpose then reverse each row | All big tech |
| 73 | [Set Matrix Zeroes](./all/set-matrix-zeroes.md) | Medium | Use the first row/column as markers for O(1) extra space | Amazon, Apple |
| 36 | [Valid Sudoku](./all/valid-sudoku.md) | Medium | Hash sets tracking rows/columns/sub-boxes | Apple, Amazon |

---

## 2. String

String problems are often combined with arrays, hash tables, and stacks. The core skills are **character counting, two pointers, and dynamic programming**.

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 5 | [Longest Palindromic Substring](./all/longest-palindromic-substring.md) | Medium | Expand around center, or interval DP | All big tech |
| 647 | [Palindromic Substrings](./all/palindromic-substrings.md) | Medium | Expand around center, counting palindromes | Amazon, Google |
| 20 | [Valid Parentheses](./warm-up/valid-parentheses.md) | Easy | Stack-based bracket matching | All big tech |
| 1249 | [Minimum Remove to Make Valid Parentheses](./all/minimum-remove-to-make-valid-parentheses.md) | Medium | Stack tracking indices to delete | **Meta favorite** |
| 49 | [Group Anagrams](./all/group-anagrams.md) | Medium | Sorted string / character count as the hash key | Google, Amazon |
| 242 | [Valid Anagram](./warm-up/valid-anagram.md) | Easy | 26-slot character count array | All big tech |
| 139/140 | [Word Break I](./all/word-break.md) / [II](./all/word-break-ii.md) | Medium/Hard | String DP; a Trie can speed up lookups | All big tech |
| 14 | [Longest Common Prefix](./all/longest-common-prefix.md) | Easy | Vertical/horizontal scanning, or a Trie | Google, Amazon |
| 271 | [Encode and Decode Strings](./all/encode-and-decode-strings.md) | Medium | Length-prefixed encoding to handle arbitrary characters | Google, Meta |
| 43 | [Multiply Strings](./all/multiply-strings.md) | Medium | Simulate long multiplication | Google, Meta |

---

## 3. Linked List

Linked list problems are all about **pointer manipulation**: fast/slow pointers, dummy head nodes, reversal, and merging.

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 206 | [Reverse Linked List](./warm-up/reverse-linked-list.md) | Easy | Iterative three-pointer approach, or recursion | All big tech |
| 92 | [Reverse Linked List II](./all/reverse-linked-list-ii.md) | Medium | Locate the sub-range head/tail, then reverse locally | Meta, Google |
| 21 | [Merge Two Sorted Lists](./all/merge-two-sorted-lists.md) | Easy | Two pointers + dummy head node | All big tech |
| 23 | [Merge k Sorted Lists](./rivian/merge-k-sorted-lists.md) | Hard | Min-heap, or pairwise divide-and-conquer merge | All big tech (Meta favorite) |
| 141/142 | [Linked List Cycle I](./all/linked-list-cycle.md) / [II](./all/linked-list-cycle-ii.md) | Easy/Medium | Floyd's fast/slow pointer cycle detection | All big tech |
| 287 | [Find the Duplicate Number](./all/find-the-duplicate-number.md) | Medium | Treat the array as a linked list, apply Floyd's algorithm | All big tech |
| 19 | [Remove Nth Node From End of List](./all/remove-nth-node-from-end-of-list.md) | Medium | Fast pointer advances N steps first, then move both in sync | Amazon, Google |
| 876 | [Middle of the Linked List](./all/middle-of-the-linked-list.md) | Easy | Fast/slow pointers, fast pointer moves at 2x speed | All big tech |
| 2 | [Add Two Numbers](./all/add-two-numbers.md) | Medium | Simulate addition with carry, dummy head node | Meta, Amazon |
| 138 | [Copy List with Random Pointer](./all/copy-list-with-random-pointer.md) | Medium | Hash map for node mapping, or interleave-then-split in place | **Meta, Amazon favorite** |
| 25 | [Reverse Nodes in k-Group](./asana/reverse-nodes-in-k-group.md) | Hard | Reverse in groups + recursive/iterative reassembly | Meta, Google |
| 143 | [Reorder List](./all/reorder-list.md) | Medium | Find the midpoint + reverse the second half + interleave merge | **Meta favorite** |
| 146 | [LRU Cache](./warm-up/lru-cache.md) | Medium | Hash map + doubly linked list for O(1) get/put | Universal favorite at every company (see Design section) |

---

## 4. Stack

The core property of a stack is **ordering constraint** (LIFO), well suited for bracket matching, expression evaluation, and monotonicity maintenance.

### 4.1 Basic Stack Applications

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 20 | [Valid Parentheses](./warm-up/valid-parentheses.md) | Easy | Match closing brackets against the stack top | All big tech |
| 155 | [Min Stack](./all/min-stack.md) | Medium | An auxiliary stack tracking the running minimum | Amazon, Apple |
| 150 | [Evaluate Reverse Polish Notation](./all/evaluate-reverse-polish-notation.md) | Medium | Stack holding operands | Amazon, Meta |
| 22 | [Generate Parentheses](./all/generate-parentheses.md) | Medium | Backtracking + stack-style pruning (open count ≥ close count) | Google, Meta |
| 394 | [Decode String](./all/decode-string.md) | Medium | Stack holding repeat counts and the string built so far | Google, Amazon |
| 341 | [Flatten Nested List Iterator](./all/flatten-nested-list-iterator.md) | Medium | Stack + lazy expansion | **Meta favorite** |
| 339 | [Nested List Weight Sum](./all/nested-list-weight-sum.md) | Medium | DFS/stack accumulating depth-weighted sums | **Meta favorite** |

### 4.2 Monotonic Stack

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 739 | [Daily Temperatures](./all/daily-temperatures.md) | Medium | Monotonically decreasing stack to find the next greater element | Amazon, Google |
| 496/503 | [Next Greater Element I](./all/next-greater-element-i.md) / [II](./all/next-greater-element-ii.md) | Easy/Medium | Monotonic stack + hash map lookup | Amazon, Google |
| 42 | [Trapping Rain Water](./all/trapping-rain-water.md) | Hard | Monotonic stack storing decreasing bar heights | Amazon, Google |
| 84 | [Largest Rectangle in Histogram](./all/largest-rectangle-in-histogram.md) | Hard | Monotonically increasing stack; compute area on pop | Google, Amazon |
| 853 | [Car Fleet](./all/car-fleet.md) | Medium | Sort by position + monotonic stack to check catch-up | Amazon, Tesla |
| 316/402 | [Remove Duplicate Letters](./all/remove-duplicate-letters.md) / [Remove K Digits](./all/remove-k-digits.md) | Medium/Medium | Greedy monotonic stack for the smallest lexicographic result | Google |

---

## 5. Queue / Monotonic Queue

Queues are FIFO, commonly used for **BFS level-order traversal** and **sliding window extremes**.

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 239 | [Sliding Window Maximum](./asana/sliding-window-maximum.md) | Hard | Monotonically decreasing deque | Amazon, Google |
| 933/862 | [Number of Recent Calls](./all/number-of-recent-calls.md) / [Shortest Subarray with Sum at Least K](./all/shortest-subarray-with-sum-at-least-k.md) | Easy/Hard | Monotonic queue / prefix sum optimization | Google |
| 622/641 | [Design Circular Queue](./all/design-circular-queue.md) / [Deque](./all/design-circular-deque.md) | Medium/Medium | Array simulating a circular queue | Amazon |
| 225/232 | [Implement Stack using Queues](./all/implement-stack-using-queues.md) / [Implement Queue using Stacks](./all/implement-queue-using-stacks.md) | Easy/Easy | Simulate one structure with the other | Amazon, Apple |

---

## 6. Hash Table

The core of hash tables is **key design** and **O(1) lookup**, commonly used for counting, deduplication, and fast lookups. Hash tables run through almost every problem type in North American interviews and are the most fundamental must-know structure.

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 217 | [Contains Duplicate](./warm-up/contains-duplicate.md) | Easy | O(1) lookup with a hash set | All big tech |
| 1 | [Two Sum](./warm-up/two-sum.md) | Easy | Hash map storing value→index while iterating | All big tech |
| 49 | [Group Anagrams](./all/group-anagrams.md) | Medium | Sorted string as the hash key | Google, Amazon |
| 128 | [Longest Consecutive Sequence](./all/longest-consecutive-sequence.md) | Medium | Hash set for O(1) lookup; only expand from sequence starting points | **Google, Meta favorite** |
| 202 | [Happy Number](./all/happy-number.md) | Easy | Hash set to detect cycles | Google, Apple |
| 380 | [Insert Delete GetRandom O(1)](./all/insert-delete-getrandom-o1.md) | Medium | Hash map + dynamic array, swap-to-end for deletion | All big tech |
| 41 | [First Missing Positive](./all/first-missing-positive.md) | Hard | In-place hashing by placing each value at its target index | All big tech |
| 1570 | [Dot Product of Two Sparse Vectors](./all/dot-product-of-two-sparse-vectors.md) | Medium | Hash map storing nonzero values, or two-pointer traversal | **Meta favorite** |
| 1762 | [Buildings With an Ocean View](./all/buildings-with-an-ocean-view.md) | Medium | Right-to-left scan tracking the running maximum | **Meta favorite** |
| 705 | [Design HashSet](./all/design-hashset.md) / [HashMap](./all/design-hashmap.md) | Easy/Easy | Array + linked list for collision handling (chaining) | Google, Amazon |

---

## 7. Tree

The core of tree problems is **recursive traversal**: pre/in/post-order, level order, and passing values bottom-up or top-down. Amazon is especially fond of tree problems (roughly 30% of its question pool), while Meta favors DFS variants on trees.

### 7.1 Binary Tree Traversal & Recursion

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 226 | [Invert Binary Tree](./warm-up/invert-binary-tree.md) | Easy | Recursively swap left and right subtrees | All big tech |
| 104 | [Maximum Depth of Binary Tree](./all/maximum-depth-of-binary-tree.md) | Easy | Bottom-up recursion returning height | All big tech |
| 543 | [Diameter of Binary Tree](./all/diameter-of-binary-tree.md) | Easy | Post-order recursion; diameter = sum of left/right subtree depths | All big tech |
| 110 | [Balanced Binary Tree](./all/balanced-binary-tree.md) | Easy | Post-order recursion returning both height and balance status | Amazon, Apple |
| 100/572 | [Same Tree](./all/same-tree.md) / [Subtree of Another Tree](./all/subtree-of-another-tree.md) | Easy/Easy | Recursive node-by-node comparison | Amazon, Meta |
| 102/103 | [Binary Tree Level Order Traversal I](./all/binary-tree-level-order-traversal.md) / [II](./all/binary-tree-zigzag-level-order-traversal.md) | Medium/Medium | BFS + queue | All big tech |
| 199 | [Binary Tree Right Side View](./rivian/binary-tree-right-side-view.md) | Medium | BFS taking the last node per level, or DFS right-first | **Meta, Amazon favorite** |
| 199+ | [Binary Tree Vertical Order Traversal](./all/binary-tree-vertical-order-traversal.md) | Medium | BFS tracking column index, then group and sort by column | **Meta favorite** |
| 1448 | [Count Good Nodes in Binary Tree](./all/count-good-nodes-in-binary-tree.md) | Medium | DFS carrying the max value seen along the path | Amazon, Google |
| 105/106 | [Construct Binary Tree from Preorder](./all/construct-binary-tree-from-preorder-and-inorder-traversal.md) / [Inorder Traversal](./all/construct-binary-tree-from-inorder-and-postorder-traversal.md) | Medium/Medium | Recursively split the array ranges | All big tech |
| 124 | [Binary Tree Maximum Path Sum](./all/binary-tree-maximum-path-sum.md) | Hard | Post-order recursion returning single-side max, global variable tracks the answer | All big tech (Meta favorite) |
| 236 | [Lowest Common Ancestor of a Binary Tree](./all/lowest-common-ancestor-of-a-binary-tree.md) | Medium | Recursively check whether left/right subtree contains p/q | **Meta favorite** |
| 297 | [Serialize and Deserialize Binary Tree](./all/serialize-and-deserialize-binary-tree.md) | Hard | Pre-order traversal + null-node placeholders | All big tech |
| 250/437 | [Count Univalue Subtrees](./all/count-univalue-subtrees.md) / [Path Sum III](./all/path-sum-iii.md) | Medium/Medium | DFS + prefix sum/hash map | Google, Amazon |

### 7.2 Binary Search Tree (BST)

BST property: an in-order traversal is strictly increasing — left < root < right, and search/insert/delete/update are all O(h).

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 98 | [Validate Binary Search Tree](./all/validate-binary-search-tree.md) | Medium | Recursively pass down lower/upper bounds | All big tech |
| 235 | [Lowest Common Ancestor of a BST](./all/lowest-common-ancestor-of-a-binary-search-tree.md) | Medium | Use value comparisons to directly decide the search direction | Amazon, Google |
| 230 | [Kth Smallest Element in a BST](./all/kth-smallest-element-in-a-bst.md) | Medium | The k-th element of an in-order traversal is the answer | All big tech |
| 700/701/450 | Search/Insert/Delete in a BST: [Search](./all/search-in-a-binary-search-tree.md)/[Insert](./all/insert-into-a-binary-search-tree.md)/[Delete](./all/delete-node-in-a-bst.md) | Easy/Medium/Medium | Recursive/iterative traversal using BST properties | Amazon, Apple |
| 108 | [Convert Sorted Array to Binary Search Tree](./all/convert-sorted-array-to-binary-search-tree.md) | Easy | Recursively pick the midpoint as root | Google, Meta |
| 938 | [Range Sum of BST](./all/range-sum-of-bst.md) | Easy | Prune the recursion using BST ordering properties | **Meta favorite** |

### 7.3 Trie (Prefix Tree)

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 208 | [Implement Trie (Prefix Tree)](./all/implement-trie-prefix-tree.md) | Medium | Each node stores child pointers + an end-of-word marker | All big tech |
| 211 | [Design Add and Search Words Data Structure](./all/design-add-and-search-words-data-structure.md) | Medium | Trie + DFS to handle the `.` wildcard | Google, Meta |
| 212 | [Word Search II](./all/word-search-ii.md) | Hard | Trie + backtracking DFS on the matrix | All big tech |
| 421 | [Maximum XOR of Two Numbers in an Array](./all/maximum-xor-of-two-numbers-in-an-array.md) | Medium | Build a bitwise Trie, greedily walk the opposite bit | Google |

### 7.4 Segment Tree / Binary Indexed Tree

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 307 | [Range Sum Query - Mutable](./all/range-sum-query-mutable.md) | Medium | Segment tree or Binary Indexed Tree (Fenwick Tree) | Google |
| 218 | [The Skyline Problem](./all/the-skyline-problem.md) | Hard | Segment tree/sweep line + a max-heap | Google |

---

## 8. Heap / Priority Queue

Heaps solve **Top K / dynamically-tracked extremes / streaming data** problems — pay attention to heap size control and comparator direction.

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 703 | [Kth Largest Element in a Stream](./warm-up/kth-largest-element-in-a-stream.md) | Easy | Maintain a min-heap of size K | All big tech |
| 1046 | [Last Stone Weight](./all/last-stone-weight.md) | Easy | Max-heap, repeatedly pop the two largest and push back the difference | Amazon, Apple |
| 973 | [K Closest Points to Origin](./asana/k-closest-points-to-origin.md) | Medium | Max-heap of size K sorted by distance | **Meta, Amazon favorite** |
| 215 | [Kth Largest Element in an Array](./rivian/kth-largest-element-in-an-array.md) | Medium | Min-heap, or Quickselect | All big tech |
| 621 | [Task Scheduler](./all/task-scheduler.md) | Medium | Max-heap by frequency with greedy scheduling + a cooldown queue | All big tech |
| 355 | [Design Twitter](./all/design-twitter.md) | Medium | Heap sorted by timestamp + hash map for follow relationships | Amazon, Meta |
| 295 | [Find Median from Data Stream](./all/find-median-from-data-stream.md) | Hard | Max-heap (left half) + min-heap (right half) | All big tech |
| 347 | [Top K Frequent Elements](./all/top-k-frequent-elements.md) | Medium | Hash-map counting + min-heap keeping the top K | All big tech |
| 23 | [Merge k Sorted Lists](./rivian/merge-k-sorted-lists.md) | Hard | Min-heap holding the current head node of each list | All big tech |

---

## 9. Graph

The core of graph problems is **traversal + state marking** — unlike trees, graph DFS/BFS require a `visited` set to avoid infinite loops. Google asks the most graph problems, often escalating from basic DFS/BFS to advanced algorithms like Dijkstra and MST.

### 9.1 DFS / BFS Fundamentals

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 200 | [Number of Islands](./warm-up/number-of-islands.md) | Medium | Matrix DFS/BFS "sinking" visited land | All big tech |
| 695 | [Max Area of Island](./all/max-area-of-island.md) | Medium | DFS to compute the size of each connected component, take the max | Amazon, Google |
| 130 | [Surrounded Regions](./all/surrounded-regions.md) | Medium | Reverse DFS starting from the border | Amazon, Google |
| 417 | [Pacific Atlantic Water Flow](./all/pacific-atlantic-water-flow.md) | Medium | Reverse DFS from both ocean borders, take the intersection | Google, Amazon |
| 286 | [Walls and Gates](./all/walls-and-gates.md) | Medium | Multi-source BFS expanding from all gates simultaneously | **Meta, Google favorite** |
| 994 | [Rotting Oranges](./all/rotting-oranges.md) | Medium | Multi-source BFS, expanding layer by layer to compute time | Amazon, Apple |
| 133 | [Clone Graph](./all/clone-graph.md) | Medium | DFS/BFS + hash map recording the original→clone mapping | All big tech |
| 127 | [Word Ladder](./all/word-ladder.md) | Hard | BFS for the shortest transformation path length | All big tech |
| 79/212 | [Word Search I](./all/word-search.md) / [II](./all/word-search-ii.md) | Medium/Hard | Backtracking DFS on the matrix, with pruning + visited marking | All big tech |

### 9.2 Topological Sort

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 207 | [Course Schedule](./all/course-schedule.md) | Medium | BFS in-degree table, or DFS three-color cycle detection | All big tech |
| 210 | [Course Schedule II](./all/course-schedule-ii.md) | Medium | Same as 207, but output the topological order | All big tech |
| 269 | [Alien Dictionary](./all/alien-dictionary.md) | Hard | Build a graph, then topologically sort to determine letter order | **Meta, Google favorite (Premium)** |
| 261 | [Graph Valid Tree](./all/graph-valid-tree.md) | Medium | Union Find/DFS to check the graph is acyclic and connected | Google, Meta (Premium) |
| 323 | [Number of Connected Components in an Undirected Graph](./all/number-of-connected-components-in-an-undirected-graph.md) | Medium | Union Find/DFS to count connected components | Google, Meta (Premium) |

### 9.3 Advanced Graph Algorithms (Shortest Path / MST)

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 743 | [Network Delay Time](./all/network-delay-time.md) | Medium | Dijkstra's single-source shortest path | Amazon, Google |
| 787 | [Cheapest Flights Within K Stops](./all/cheapest-flights-within-k-stops.md) | Medium | Bellman-Ford, or a layer-limited BFS | Google, Amazon |
| 1631 | [Path With Minimum Effort](./all/path-with-minimum-effort.md) | Medium | Dijkstra variant, or binary search + BFS | Google, Amazon |
| 778 | [Swim in Rising Water](./all/swim-in-rising-water.md) | Hard | Dijkstra variant / binary search + BFS | Google, Amazon |
| 1584 | [Min Cost to Connect All Points](./all/min-cost-to-connect-all-points.md) | Medium | Kruskal's or Prim's minimum spanning tree | Amazon, Google |
| 332 | [Reconstruct Itinerary](./all/reconstruct-itinerary.md) | Hard | Eulerian path + greedy/backtracking | Google, Amazon |

---

## 10. Union Find

Union Find solves **connectivity** problems, with path compression + union by rank at its core, determining whether two nodes belong to the same set.

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 547 | [Number of Provinces](./all/number-of-provinces.md) | Medium | Traverse the adjacency matrix, unioning cities | Google |
| 684/685 | [Redundant Connection I](./all/redundant-connection.md) / [II](./all/redundant-connection-ii.md) | Medium/Hard | Detect a cycle while unioning | **Google, Meta favorite** |
| 261 | [Graph Valid Tree](./all/graph-valid-tree.md) | Medium | edges = nodes - 1 and no cycle | Google, Meta |
| 323 | [Number of Connected Components in an Undirected Graph](./all/number-of-connected-components-in-an-undirected-graph.md) | Medium | Count distinct roots after unioning | Google, Meta |
| 990 | [Satisfiability of Equality Equations](./all/satisfiability-of-equality-equations.md) | Medium | Union Find handling equivalence relations | Google, Amazon |
| 1319 | [Number of Operations to Make Network Connected](./all/number-of-operations-to-make-network-connected.md) | Medium | Determine the number of connected components; answer = components - 1 | Amazon |

---

## 11. Backtracking

Backtracking is essentially brute-force search over the recursion call stack with pruning, often combined with arrays/strings/matrices. It is a common medium-to-hard question type at Google and Amazon interviews.

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 78 | [Subsets](./warm-up/subsets.md) | Medium | Two branches per element: include or exclude | All big tech |
| 90 | [Subsets II](./all/subsets-ii.md) | Medium | Sort first, then skip duplicate elements at the same recursion level | Amazon, Meta |
| 46 | [Permutations](./all/permutations.md) | Medium | Use a `visited` array, or swap in place to generate permutations | All big tech |
| 39 | [Combination Sum](./asana/combination-sum.md) | Medium | Elements can be reused; prune when the running sum exceeds the target | All big tech |
| 40 | [Combination Sum II](./all/combination-sum-ii.md) | Medium | Sort first, skip duplicates at the same level, elements used once each | Amazon, Google |
| 22 | [Generate Parentheses](./all/generate-parentheses.md) | Medium | Can only place a closing bracket when open count ≥ close count | Google, Meta |
| 17 | [Letter Combinations of a Phone Number](./asana/letter-combinations-of-a-phone-number.md) | Medium | Backtrack digit by digit using the keypad mapping | All big tech |
| 79 | [Word Search](./all/word-search.md) | Medium | Four-directional DFS backtracking on the matrix | All big tech |
| 131 | [Palindrome Partitioning](./all/palindrome-partitioning.md) | Medium | Backtracking + palindrome check for pruning | Amazon, Google |
| 51 | [N-Queens](./asana/n-queens.md) | Hard | Backtrack row by row, pruning column/diagonal conflicts | Google, Amazon |

---

## 12. Dynamic Programming (Array/Table Based)

Dynamic programming is an algorithmic paradigm rather than a data structure, but its states are almost always stored in a **1D/2D array**. Google interviewers place particular weight on deriving the recurrence relation and base cases, not just the final answer.

### 12.1 1D DP

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 70 | [Climbing Stairs](./warm-up/climbing-stairs.md) | Easy | 1D DP, can be optimized with rolling variables | All big tech |
| 746 | [Min Cost Climbing Stairs](./all/min-cost-climbing-stairs.md) | Easy | Similar to #70, with weighted DP transitions | Amazon, Apple |
| 198/213 | [House Robber I](./all/house-robber.md) / [II](./all/house-robber-ii.md) | Medium/Medium | dp[i] = max(dp[i-1], dp[i-2] + nums[i]); split the circular array into two segments | All big tech |
| 91 | [Decode Ways](./all/decode-ways.md) | Medium | String DP; careful with "0" and valid two-digit ranges | All big tech |
| 322 | [Coin Change](./all/coin-change.md) | Medium | Unbounded knapsack style 1D DP | All big tech |
| 152 | [Maximum Product Subarray](./asana/maximum-product-subarray.md) | Medium | Track running max/min product DP | All big tech |
| 139 | [Word Break](./all/word-break.md) | Medium | Unbounded knapsack style 1D DP | All big tech |
| 300 | [Longest Increasing Subsequence](./all/longest-increasing-subsequence.md) | Medium | dp[i] = LIS ending at i, or a binary-search optimization | Google |
| 416 | [Partition Equal Subset Sum](./all/partition-equal-subset-sum.md) | Medium | 0/1 knapsack; DP array marks reachable sums | Amazon, Google |

### 12.2 2D DP

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 62 | [Unique Paths](./all/unique-paths.md) | Medium | 2D grid DP | All big tech |
| 1143 | [Longest Common Subsequence](./all/longest-common-subsequence.md) | Medium | dp[i][j] = LCS of the first i and first j characters | **Meta, Google favorite** |
| 72 | [Edit Distance](./all/edit-distance.md) | Medium | Three transitions: insert/delete/replace | **Google, Meta favorite** |
| 309 | [Best Time to Buy and Sell Stock with Cooldown](./all/best-time-to-buy-and-sell-stock-with-cooldown.md) | Medium | State-machine DP: holding/not-holding/cooldown | Amazon, Google |
| 518 | [Coin Change 2](./all/coin-change-ii.md) | Medium | Unbounded knapsack counting the number of combinations | Amazon, Google |
| 494 | [Target Sum](./all/target-sum.md) | Medium | Reformulate as a 0/1 knapsack subset-sum problem | Google, Meta |
| 97 | [Interleaving String](./all/interleaving-string.md) | Medium | 2D DP checking whether two strings can interleave into a third | Google, Amazon |
| 329 | [Longest Increasing Path in a Matrix](./all/longest-increasing-path-in-a-matrix.md) | Hard | DFS + memoization | Google, Amazon |
| 115 | [Distinct Subsequences](./all/distinct-subsequences.md) | Hard | 2D DP counting | Google, Amazon |
| 312 | [Burst Balloons](./all/burst-balloons.md) | Hard | Interval DP; think backward about the last balloon burst | Google, Amazon |
| 5/647 | [Longest Palindromic Substring](./all/longest-palindromic-substring.md) / [Palindromic Substrings](./all/palindromic-substrings.md) | Medium/Medium | Interval DP | All big tech |
| 121/122/309/188 | Buy/Sell Stock series: [121](./warm-up/best-time-to-buy-and-sell-stock.md)/[122](./all/best-time-to-buy-and-sell-stock-ii.md)/[309](./all/best-time-to-buy-and-sell-stock-with-cooldown.md)/[188](./all/best-time-to-buy-and-sell-stock-iv.md) | Easy/Medium/Medium/Hard | State-machine DP | All big tech |
| 32 | [Longest Valid Parentheses](./all/longest-valid-parentheses.md) | Hard | DP, or a stack tracking unmatched open-bracket positions | All big tech |

---

## 13. Greedy

Greedy problems typically combine sorting or a single pass, deriving a global optimum from local optimal choices. They often appear as an advanced variant of array/interval problems.

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 53 | [Maximum Subarray](./warm-up/maximum-subarray.md) | Medium | Kadane's greedy accumulation | All big tech |
| 55 | [Jump Game](./all/jump-game.md) | Medium | Track the farthest reachable position so far | All big tech |
| 45 | [Jump Game II](./rivian/jump-game-ii.md) | Medium | Greedily expand the reachable range at the next "level", similar to BFS layering | All big tech |
| 134 | [Gas Station](./all/gas-station.md) | Medium | If total gas is sufficient, some starting point guarantees completing the loop | Amazon, Google |
| 846 | [Hand of Straights](./all/hand-of-straights.md) | Medium | Sort + hash-map counting for greedy group formation | Google, Amazon |
| 1899 | [Merge Triplets to Form Target Triplet](./all/merge-triplets-to-form-target-triplet.md) | Medium | Greedily filter triplets that satisfy the condition | Google, Amazon |
| 763 | [Partition Labels](./all/partition-labels.md) | Medium | Record each character's last occurrence, greedily extend the interval | Amazon, Google |
| 678 | [Valid Parenthesis String](./all/valid-parenthesis-string.md) | Medium | Greedily maintain the possible range of open-bracket counts | Google, Meta |

---

## 14. Bit Manipulation & Math

These problems don't rely on complex data structures, but they are basic-literacy questions Apple/Amazon frequently ask, testing intuition about binary and numeric properties.

| # | Problem | Difficulty | Key Idea | Common Companies |
|---|---|---|---|---|
| 136 | [Single Number](./warm-up/single-number.md) | Easy | XOR cancels out numbers that appear in pairs | All big tech |
| 191 | [Number of 1 Bits](./all/number-of-1-bits.md) | Easy | n & (n-1) clears the lowest set bit | All big tech |
| 338 | [Counting Bits](./all/counting-bits.md) | Easy | dp[i] = dp[i >> 1] + (i & 1) | All big tech |
| 190 | [Reverse Bits](./all/reverse-bits.md) | Easy | Construct bit by bit via shifting | Apple, Amazon |
| 268 | [Missing Number](./all/missing-number.md) | Easy | XOR trick, or the sum formula | All big tech |
| 371 | [Sum of Two Integers](./all/sum-of-two-integers.md) | Medium | Simulate addition with bit operations (XOR + carry) | Apple, Amazon |
| 7 | [Reverse Integer](./all/reverse-integer.md) | Medium | Build digit by digit with modulo, watch for overflow | All big tech |
| 50 | [Pow(x, n)](./all/powx-n.md) | Medium | Fast exponentiation, recursive or iterative binary splitting | All big tech |
| 202 | [Happy Number](./all/happy-number.md) | Easy | Numeric pattern + hash set for cycle detection | Google, Apple |
| 66 | [Plus One](./all/plus-one.md) | Easy | Simulate digit-wise addition with carry on an array | Google, Apple |

---

## 15. Design Problems

These problems test **combining multiple data structures** — the key skill is stitching structures together to satisfy the time-complexity requirements of every operation. This question type appears at mid-to-senior level interviews across every big-tech company.

| # | Problem | Difficulty | Combined Structure | Common Companies |
|---|---|---|---|---|
| 146 | [LRU Cache](./warm-up/lru-cache.md) | Medium | Hash map + doubly linked list, O(1) get/put | Universal favorite at every company |
| 460 | [LFU Cache](./all/lfu-cache.md) | Hard | Hash map + frequency-bucketed doubly linked lists | Amazon, Google |
| 432 | [All O`one Data Structure](./all/all-oone-data-structure.md) | Hard | Hash map + doubly linked list bucketed by count | Google |
| 380 | [Insert Delete GetRandom O(1)](./all/insert-delete-getrandom-o1.md) | Medium | Hash map + dynamic array | All big tech |
| 355 | [Design Twitter](./all/design-twitter.md) | Medium | Hash map + min-heap sorted by timestamp | Amazon, Meta |
| 384 | [Shuffle an Array](./all/shuffle-an-array.md) | Medium | Array + Fisher–Yates shuffle | Google, Amazon |
| 981 | [Time Based Key-Value Store](./all/time-based-key-value-store.md) | Medium | Hash map + sorted list with binary search | Google, Amazon |
| 1707 | [Detect Squares](./all/maximum-xor-with-an-element-from-array.md) | Hard | Hash map counting by coordinate | Google, Amazon |
| 208/211 | [Implement Trie](./all/implement-trie-prefix-tree.md) / [Add and Search Words](./all/design-add-and-search-words-data-structure.md) | Medium/Medium | Trie structure | All big tech |
| 155 | [Min Stack](./all/min-stack.md) | Medium | Single or dual stack storing (value, running minimum) pairs | Amazon, Apple |

---

## 16. Company-Specific High-Frequency Lists

### Google: Graphs, Trees, DP + Deep Follow-Ups
[`200`](./warm-up/number-of-islands.md) [`23`](./rivian/merge-k-sorted-lists.md) [`295`](./all/find-median-from-data-stream.md) [`4`](./all/median-of-two-sorted-arrays.md) [`269`](./all/alien-dictionary.md) [`547`](./all/number-of-provinces.md) [`684`](./all/redundant-connection.md) [`73`](./all/set-matrix-zeroes.md) [`297`](./all/serialize-and-deserialize-binary-tree.md) [`199`](./rivian/binary-tree-right-side-view.md) [`875`](./all/koko-eating-bananas.md) [`329`](./all/longest-increasing-path-in-a-matrix.md) [`312`](./all/burst-balloons.md) [`1631`](./all/path-with-minimum-effort.md)

### Meta: Fast array/string problems + Tree DFS; highly recycled question pool (focus on the last-3-months company tag)
[`680`](./all/valid-palindrome-ii.md) [`528`](./all/random-pick-with-weight.md) [`1249`](./all/minimum-remove-to-make-valid-parentheses.md) [`236`](./all/lowest-common-ancestor-of-a-binary-tree.md) [`938`](./all/range-sum-of-bst.md) [`567`](./all/permutation-in-string.md) [`424`](./all/longest-repeating-character-replacement.md) [`153`](./all/find-minimum-in-rotated-sorted-array.md) [`31`](./all/next-permutation.md) [`92`](./all/reverse-linked-list-ii.md) [`297`](./all/serialize-and-deserialize-binary-tree.md) [`124`](./all/binary-tree-maximum-path-sum.md) [`105`](./all/construct-binary-tree-from-preorder-and-inorder-traversal.md) [`199`](./rivian/binary-tree-right-side-view.md) [`238`](./asana/product-of-array-except-self.md) [`560`](./all/subarray-sum-equals-k.md) [`128`](./all/longest-consecutive-sequence.md) [`143`](./all/reorder-list.md) [`138`](./all/copy-list-with-random-pointer.md) [`339`](./all/nested-list-weight-sum.md) [`1570`](./all/dot-product-of-two-sparse-vectors.md) [`1762`](./all/buildings-with-an-ocean-view.md)

### Amazon: Mostly trees/graphs, balancing speed with the Leadership Principles behavioral round
[`76`](./all/minimum-window-substring.md) [`53`](./warm-up/maximum-subarray.md) [`322`](./all/coin-change.md) [`33`](./all/search-in-rotated-sorted-array.md) [`198`](./all/house-robber.md) [`5`](./all/longest-palindromic-substring.md) [`42`](./all/trapping-rain-water.md) [`215`](./rivian/kth-largest-element-in-an-array.md) [`973`](./asana/k-closest-points-to-origin.md) [`695`](./all/max-area-of-island.md) [`994`](./all/rotting-oranges.md) [`84`](./all/largest-rectangle-in-histogram.md) [`138`](./all/copy-list-with-random-pointer.md) [`25`](./asana/reverse-nodes-in-k-group.md) [`230`](./all/kth-smallest-element-in-a-bst.md) [`286`](./all/walls-and-gates.md)

### Netflix: Applied systems problems (LRU/LFU, concurrent containers, interval scheduling)
[`146`](./warm-up/lru-cache.md) [`460`](./all/lfu-cache.md) [`1235`](./all/maximum-profit-in-job-scheduling.md) (meeting room/scheduling variants); concurrency scenarios (read/write locks, thread-safe design — no fixed problem numbers)

### Apple: Standard medium-difficulty problems + code quality (naming, edge cases, modularity) as an implicit scoring factor
[`217`](./warm-up/contains-duplicate.md) [`1`](./warm-up/two-sum.md) [`242`](./warm-up/valid-anagram.md) [`104`](./all/maximum-depth-of-binary-tree.md) [`110`](./all/balanced-binary-tree.md) [`700`](./all/search-in-a-binary-search-tree.md) [`146`](./warm-up/lru-cache.md) [`155`](./all/min-stack.md) [`36`](./all/valid-sudoku.md) [`73`](./all/set-matrix-zeroes.md)

---

## 17. Recommended Study Order

1. **Array, String, Hash Table**: build the foundation — master two pointers, sliding window, and prefix sums.
2. **Linked List**: get comfortable with pointer manipulation, especially fast/slow pointers and dummy head nodes.
3. **Stack and Queue**: master bracket matching and monotonic stack/queue templates.
4. **Tree**: master the pre/in/post-order recursive templates first, then extend to BST and Trie.
5. **Backtracking**: practice subsets, permutations, and combinations, combined with arrays/strings/matrices.
6. **Graph**: BFS/DFS, topological sort, Union Find, then move on to Dijkstra/MST.
7. **Heap**: Top K problems and streaming-data scenarios.
8. **Dynamic Programming**: from 1D knapsack problems to 2D interval DP, finishing with state-machine DP.
9. **Greedy / Bit Manipulation / Math**: fill in the gaps — usually quick to learn but still tested.
10. **Design problems + company-specific targeting**: once you've picked a target company, spend the final 1-2 weeks drilling that company's high-frequency tagged problems and run timed mock interviews (Google: 45 min single problem with follow-ups; Meta: 35 min for two problems back-to-back; Amazon: 40 min coding + LP).

> After finishing each data-structure category, immediately summarize its templates rather than grinding problems from Easy to Hard in order. Once you've settled on a target company, use LeetCode Premium's company tags (filtered by the last 3/6 months) for your final round of targeted review — it has the highest hit rate.

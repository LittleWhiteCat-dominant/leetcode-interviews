# Rivian Interview Coding Questions

> A curated collection of algorithm/coding questions that have been reported by candidates in Rivian software engineer interviews (onsite coding rounds, phone screens, and HackerRank assessments). Sources: candidate interview reports (JoinTaro, Glassdoor-style aggregators), CodeJeet, MagicSheet, ScaleEngineer, and Verve AI's 2026 Rivian interview guide.

## About Rivian's Coding Interview

- **Format**: Recruiter screen → technical phone screen (1 LeetCode-style medium, timed on HackerRank) → virtual onsite with 2 coding rounds + a system design round (usually EV/vehicle-themed, e.g. OTA update pipelines, vehicle telemetry, charging networks) + a behavioral round.
- **Difficulty**: Mostly **Medium**, with occasional **Easy** warmups and a few **Hard** problems for senior roles (about 67% Medium overall).
- **Top topics**: Array, Hash Table, Linked List, Matrix, String, Tree/Graph (BFS/DFS), Design, Heap.
- **What interviewers look for**: correct and efficient solution, clean code, clear articulation of time/space complexity, and thoughtful edge-case handling. Follow-up questions about optimizing or extending the solution are common.

## Question List

| # | Problem | LeetCode # | Difficulty | Topics |
|---|---|---|---|---|
| 1 | [Number of Islands](./number-of-islands.md) | 200 | Medium | Array, Matrix, DFS, BFS, Union Find |
| 2 | [LRU Cache](./lru-cache.md) | 146 | Medium | Design, Hash Table, Doubly Linked List |
| 3 | [Rotate String](./rotate-string.md) | 796 | Easy | String, String Matching |
| 4 | [Merge Intervals](./merge-intervals.md) | 56 | Medium | Array, Sorting |
| 5 | [Merge k Sorted Lists](./merge-k-sorted-lists.md) | 23 | Hard | Linked List, Heap, Divide and Conquer |
| 6 | [Degree of an Array](./degree-of-an-array.md) | 697 | Easy | Array, Hash Table |
| 7 | [Flatten Deeply Nested Array](./flatten-deeply-nested-array.md) | 2625 | Medium | Array, Recursion |
| 8 | [String Compression](./string-compression.md) | 443 | Medium | String, Two Pointers |
| 9 | [Max Increase to Keep City Skyline](./max-increase-to-keep-city-skyline.md) | 807 | Medium | Array, Matrix, Greedy |
| 10 | [Basic Calculator II](./basic-calculator-ii.md) | 227 | Medium | Stack, String, Math |
| 11 | [Remove All Occurrences of a Substring](./remove-all-occurrences-of-a-substring.md) | 1910 | Medium | String, Stack, String Matching |
| 12 | [Binary Tree Right Side View](./binary-tree-right-side-view.md) | 199 | Medium | Tree, BFS, DFS |
| 13 | [Jump Game II](./jump-game-ii.md) | 45 | Medium | Array, Greedy, Dynamic Programming |
| 14 | [Invert Binary Tree](./invert-binary-tree.md) | 226 | Easy | Tree, Recursion, Iteration |
| 15 | [Kth Largest Element in an Array](./kth-largest-element-in-an-array.md) | 215 | Medium | Array, Sorting, Heap, Quickselect |
| 16 | [Valid Palindrome](./valid-palindrome.md) | 125 | Easy | String, Two Pointers |
| 17 | [Angle Between Hands of a Clock](./angle-between-hands-of-a-clock.md) | 1344 | Medium | Math |

## Suggested Study Order

1. Start with the **highest-frequency, most-confirmed** problems reported directly from Rivian onsite interviews: `Number of Islands`, `LRU Cache`, `Rotate String`, `Merge Intervals`, `Merge k Sorted Lists`, `Basic Calculator II`.
2. Then cover the **CodeJeet-tracked** set that rounds out Rivian's known question bank: `Degree of an Array`, `Flatten Deeply Nested Array`, `String Compression`, `Max Increase to Keep City Skyline`.
3. Finish with the **topic-area fillers** frequently seen in Rivian-style interviews for the same skill areas (arrays, strings, trees, graphs, greedy/DP): `Remove All Occurrences of a Substring`, `Binary Tree Right Side View`, `Jump Game II`, `Invert Binary Tree`, `Kth Largest Element in an Array`, `Valid Palindrome`, `Angle Between Hands of a Clock`.
4. Don't neglect the **system design** (vehicle/EV-themed, design for intermittent connectivity) and **behavioral** rounds (Rivian Compass framework: *Stay Adventurous*, *Lead the Way*, *Bring People Together*) — many candidates report losing the offer there despite strong coding performance.

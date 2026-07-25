# Asana Interview Coding Questions

> A curated collection of algorithm/coding questions that have been reported by candidates in Asana software engineer interviews (technical phone screens and on-site/virtual on-site coding rounds). Sources: LeakCode, JoinTaro, InterviewSolver, MagicSheet, and PracHub candidate interview reports (2024-2026).

## About Asana's Coding Interview

- **Format**: Recruiter screen → 1-2 technical phone screens (medium-difficulty coding) → 4-6 round on-site/virtual on-site loop covering coding, system design (at L4+ levels), and behavioral rounds.
- **Difficulty**: Mostly **Medium** (~59-75% depending on the tracked dataset), with some Easy warmups and a handful of Hard problems.
- **Top topics**: Array, String, Heap (Priority Queue), Divide and Conquer, Tree, Linked List, Sliding Window, Dynamic Programming.
- **What interviewers look for**: clear problem decomposition *before* coding, explicit time/space complexity reasoning, structured edge-case handling, and the ability to articulate trade-offs between two reasonable approaches.
- **#1 predictive signal**: asking clarifying questions. Interviewers are explicitly trained to weight this — strong candidates ask 3-5 clarifying questions even on problems that look straightforward. The most common reason for negative feedback is jumping straight into code without clarifying requirements.
- **Recommended round template**: clarify requirements (2-3 min) → state your approach out loud and confirm direction with the interviewer (3-5 min) → code with continuous narration (15-25 min) → test with concrete examples including edge cases (5 min) → discuss optimization/trade-offs if time permits (5 min).
- **Common failure signals**: coding silently for extended periods, missing edge cases (empty input, single element, large input, overflow), producing working code the candidate cannot refactor when probed, and — in behavioral rounds — using "we" instead of "I" when describing personal contributions.

## Question List

| # | Problem | LeetCode # | Difficulty | Topics |
|---|---|---|---|---|
| 1 | [Product of Array Except Self](./product-of-array-except-self.md) | 238 | Medium | Array, Prefix Sum |
| 2 | [K Closest Points to Origin](./k-closest-points-to-origin.md) | 973 | Medium | Array, Heap, Quickselect, Sorting, Divide and Conquer |
| 3 | [Maximum Repeating Substring](./maximum-repeating-substring.md) | 1668 | Easy | String, Array, String Matching, Sliding Window |
| 4 | [Binary Tree Right Side View](./binary-tree-right-side-view.md) | 199 | Medium | Tree, BFS, DFS |
| 5 | [Sliding Window Maximum](./sliding-window-maximum.md) | 239 | Hard | Array, Sliding Window, Monotonic Queue, Heap |
| 6 | [Nested List Weight Sum II](./nested-list-weight-sum-ii.md) | 364 | Medium | DFS, BFS, Design |
| 7 | [Maximum Product Subarray](./maximum-product-subarray.md) | 152 | Medium | Array, Dynamic Programming |
| 8 | [Reverse Nodes in k-Group](./reverse-nodes-in-k-group.md) | 25 | Hard | Linked List, Recursion |
| 9 | [N-Queens](./n-queens.md) | 51 | Hard | Backtracking |
| 10 | [Making A Large Island](./making-a-large-island.md) | 827 | Hard | Array, Matrix, DFS, BFS, Union Find |
| 11 | [Convert Sorted List to Binary Search Tree](./convert-sorted-list-to-binary-search-tree.md) | 109 | Medium | Linked List, Tree, BST, DFS |
| 12 | [Sum Root to Leaf Numbers](./sum-root-to-leaf-numbers.md) | 129 | Medium | Tree, DFS, Binary Tree |
| 13 | [Maximum Subarray](./maximum-subarray.md) | 53 | Medium | Array, Divide and Conquer, Dynamic Programming |
| 14 | [Meeting Rooms II](./meeting-rooms-ii.md) | 253 | Medium | Array, Sorting, Heap, Greedy |
| 15 | [Letter Combinations of a Phone Number](./letter-combinations-of-a-phone-number.md) | 17 | Medium | String, Backtracking |
| 16 | [Random Pick Index](./random-pick-index.md) | 398 | Medium | Array, Hash Table, Reservoir Sampling |
| 17 | [Combination Sum](./combination-sum.md) | 39 | Medium | Array, Backtracking |

## Suggested Study Order

1. Start with the **highest-confidence, most-recently-confirmed** questions (reported within the last 6-12 months across multiple candidate sources): `Product of Array Except Self`, `K Closest Points to Origin`, `Maximum Repeating Substring`.
2. Then cover the **broader tracked question bank** that shows up repeatedly in Asana-tagged problem lists, grouped by Asana's top topics (Array, String, Heap, Tree, Linked List): `Binary Tree Right Side View`, `Sliding Window Maximum`, `Nested List Weight Sum II`, `Maximum Product Subarray`, `Maximum Subarray`, `Meeting Rooms II`, `Random Pick Index`.
3. Round out preparation with the **Hard-tier and backtracking-heavy** problems that appear for more senior loops: `Reverse Nodes in k-Group`, `N-Queens`, `Making A Large Island`, `Convert Sorted List to Binary Search Tree`, `Sum Root to Leaf Numbers`, `Letter Combinations of a Phone Number`, `Combination Sum`.
4. Since Asana rotates its question pool every 2-4 months, treat this list as a **pattern-recognition tool, not a memorization target** — practice explaining your approach out loud and asking clarifying questions on every problem, since that is the single most predictive signal in Asana's process.
5. At L4+ levels, also prepare for **system design** prompts that are close to Asana's own product domain (e.g. designing a collaborative real-time task/like counter, or a collaborative to-do list with concurrent edits) and behavioral rounds that probe ownership, ambiguity tolerance, and conflict navigation.

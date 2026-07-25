# Universal Warm-Up Questions

> These are the problems that serve as the **universal, company-agnostic warm-up** for each data-structure category in [`basic_en.md`](../basic_en.md) — the North-American-interview data-structure summary. Two of them (`Two Sum`, `Best Time to Buy and Sell Stock`) are explicitly tagged **"Universal warmup at every company"** in that document, and `LRU Cache` is explicitly tagged **"Universal favorite at every company"**. The rest are the single most canonical, `All big tech`-tagged, Easy-to-lower-Medium representative problem picked from each remaining category, since every category in a real interview loop tends to open with a problem just like it before escalating in difficulty.

## Why These Questions

- Every one of them is solvable cleanly in a handful of minutes with the single core technique that defines its data structure (hash map lookup, fast/slow pointers, a stack, a heap, DFS/BFS, a 1D DP array, etc.).
- They are the questions interviewers reach for first to establish a baseline signal — clarifying questions, communication, edge-case awareness, coding style — before escalating to a harder, company-specific problem or a chain of follow-ups.
- Being able to solve each of these **instantly and without hesitation** frees up time and cognitive bandwidth in the interview for whatever comes next.

## Question List

| # | Category | Problem | LeetCode # | Difficulty | Why It's the Universal Pick |
|---|---|---|---|---|---|
| 1 | Array | [Two Sum](./two-sum.md) | 1 | Easy | Explicitly tagged "Universal warmup at every company" |
| 2 | Array | [Best Time to Buy and Sell Stock](./best-time-to-buy-and-sell-stock.md) | 121 | Easy | Explicitly tagged "Universal warmup at every company" |
| 3 | String | [Valid Anagram](./valid-anagram.md) | 242 | Easy | Canonical character-count warm-up, tagged "All big tech" |
| 4 | Linked List | [Reverse Linked List](./reverse-linked-list.md) | 206 | Easy | The quintessential pointer-manipulation warm-up, tagged "All big tech" |
| 5 | Stack | [Valid Parentheses](./valid-parentheses.md) | 20 | Easy | The quintessential stack-matching warm-up, tagged "All big tech" |
| 6 | Hash Table | [Contains Duplicate](./contains-duplicate.md) | 217 | Easy | Simplest possible hash-set lookup warm-up, tagged "All big tech" |
| 7 | Tree | [Invert Binary Tree](./invert-binary-tree.md) | 226 | Easy | The famous "can you invert a binary tree" recursion warm-up, tagged "All big tech" |
| 8 | Heap / Priority Queue | [Kth Largest Element in a Stream](./kth-largest-element-in-a-stream.md) | 703 | Easy | Simplest fixed-size min-heap warm-up, tagged "All big tech" |
| 9 | Graph | [Number of Islands](./number-of-islands.md) | 200 | Medium | The universal DFS/BFS grid warm-up, tagged "All big tech" |
| 10 | Backtracking | [Subsets](./subsets.md) | 78 | Medium | The simplest include/exclude recursion tree, tagged "All big tech" |
| 11 | Dynamic Programming | [Climbing Stairs](./climbing-stairs.md) | 70 | Easy | The canonical first DP problem everyone learns, tagged "All big tech" |
| 12 | Greedy | [Maximum Subarray](./maximum-subarray.md) | 53 | Medium | Kadane's algorithm — the canonical greedy/DP-hybrid warm-up, tagged "All big tech" |
| 13 | Bit Manipulation & Math | [Single Number](./single-number.md) | 136 | Easy | The canonical XOR warm-up, tagged "All big tech" |
| 14 | Design | [LRU Cache](./lru-cache.md) | 146 | Medium | Explicitly tagged "Universal favorite at every company" |

### Categories Without a Dedicated Universal Pick

- **Queue / Monotonic Queue**: no single problem in this category carries an "All big tech" tag in `basic_en.md` — queue mechanics are almost always tested indirectly through BFS-based tree/graph problems (see `Number of Islands` above) rather than as a standalone warm-up.
- **Union Find**: same situation — every tracked problem in this category is tagged to specific companies (Google, Meta, Amazon) rather than universally, since Union Find tends to appear as a *technique* layered onto a graph/array problem rather than as its own opening question.

## Preparation Tips

1. Be able to write a correct, clean solution to every problem above **from memory, in under 5-8 minutes each**, while narrating your approach out loud.
2. For each one, know both the brute-force approach *and* the optimal approach, and be ready to explain the time/space trade-off between them.
3. Expect immediate follow-ups even on these "easy" openers — check each problem file's *Follow-up Questions* section for the most common escalations within that category.
4. Treat a flawless performance on these warm-ups as table stakes, not a differentiator — the real signal in the round comes from how you handle what's asked next.

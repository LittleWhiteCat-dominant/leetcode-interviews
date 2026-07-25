# 70. Climbing Stairs

**Difficulty:** Easy
**Topics:** Math, Dynamic Programming, Memoization
**Category warm-up for:** Dynamic Programming

## Problem Description

You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb `1` or `2` steps. In how many distinct ways can you climb to the top?

## Example 1

```
Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps
```

## Example 2

```
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step
```

## Constraints

- `1 <= n <= 45`

## Approach

1. **Recognize the recurrence**: to reach step `n`, your last move was either a single step from `n - 1`, or a double step from `n - 2`. So the number of ways to reach step `n` is `ways(n-1) + ways(n-2)` — this is exactly the Fibonacci recurrence.
2. **Base cases**: `ways(1) = 1` (only one way: a single step), `ways(2) = 2` (either two single steps, or one double step).
3. **Bottom-up DP with O(1) space**: since each step only depends on the previous two, you don't need a full DP array — just track the last two values with rolling variables and iterate up to `n`.

**Time Complexity:** O(n) — a single pass computing each step's value from the previous two.
**Space Complexity:** O(1) with the rolling-variable optimization (O(n) if you use a full DP array, which is also acceptable and often the first version people write).

## Reference Solution (Python)

```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n

    prev2, prev1 = 1, 2  # ways(1), ways(2)
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2

    return prev1
```

## Follow-up Questions Interviewers May Ask

- How would you solve this if you could climb `1`, `2`, **or** `3` steps at a time?
- How would you solve **Min Cost Climbing Stairs** (LC 746), where each step has an associated cost and you want to minimize total cost?
- Can you close-form solve this using the Fibonacci formula (Binet's formula) for O(log n) or O(1) time?

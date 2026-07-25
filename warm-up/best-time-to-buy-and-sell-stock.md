# 121. Best Time to Buy and Sell Stock

**Difficulty:** Easy
**Topics:** Array, Dynamic Programming
**Reported as a warm-up at:** Universal — used as an opening question at virtually every big-tech company (Google, Meta, Amazon, Apple, Netflix, and beyond).

## Problem Description

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.

You want to maximize your profit by choosing a single day to **buy** one stock and choosing a different day in the future to **sell** that stock.

Return *the maximum profit you can achieve from this transaction*. If you cannot achieve any profit, return `0`.

## Example 1

```
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
```

## Example 2

```
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.
```

## Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^4`

## Approach

1. **Brute force (state this first, then optimize):** for every pair of days `(buy_day, sell_day)` with `buy_day < sell_day`, compute `prices[sell_day] - prices[buy_day]` and track the maximum. This is O(n²) time.
2. **Optimal — single pass tracking the running minimum:** iterate through the prices once, maintaining:
   - `min_price_so_far`: the lowest price seen up to (and including) the current day — this represents the best possible day to have bought so far.
   - `max_profit`: the best profit achievable if you sold on the current day, i.e. `prices[i] - min_price_so_far`.
3. At each day, first check if selling today (using the best buy price so far) beats the current best profit, then update `min_price_so_far` if today's price is a new low.

**Time Complexity:** O(n) — a single pass through the prices.
**Space Complexity:** O(1) extra space.

## Reference Solution (Python)

```python
def max_profit(prices: list[int]) -> int:
    min_price_so_far = float("inf")
    max_profit_so_far = 0

    for price in prices:
        min_price_so_far = min(min_price_so_far, price)
        max_profit_so_far = max(max_profit_so_far, price - min_price_so_far)

    return max_profit_so_far
```

## Follow-up Questions Interviewers May Ask

- How would you solve it if you were allowed to complete **as many transactions as you like** (see LC 122, Best Time to Buy and Sell Stock II)?
- How would you solve it with **at most two transactions** (LC 123) or **at most k transactions** (LC 188)?
- How would you handle a **cooldown period** after selling before you can buy again (LC 309)?
- How would you handle a **transaction fee** charged on every trade (LC 714)?
- Can you also return the specific `buy_day` and `sell_day` that achieve the maximum profit, not just the profit value?

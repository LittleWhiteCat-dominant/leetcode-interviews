# 53. Maximum Subarray

**Difficulty:** Medium
**Topics:** Array, Divide and Conquer, Dynamic Programming, Greedy
**Category warm-up for:** Greedy

## Problem Description

Given an integer array `nums`, find the subarray with the largest sum, and return *its sum*.

## Example 1

```
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
```

## Example 2

```
Input: nums = [1]
Output: 1
```

## Example 3

```
Input: nums = [5,4,-1,7,8]
Output: 23
```

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

**Follow-up:** If you have figured out the `O(n)` solution, try coding another solution using the **divide and conquer** approach, which is more subtle.

## Approach

**Kadane's Algorithm (O(n), greedy):**
1. Maintain `current_sum`, the maximum sum of a subarray ending at the current index.
2. At each element, greedily decide whether to **extend** the previous subarray (`current_sum + num`) or **start fresh** at the current element (`num`), whichever is larger: `current_sum = max(num, current_sum + num)`. This is greedy because you discard the running sum entirely the moment it goes negative, without ever reconsidering that decision.
3. Track `best_sum` as the running maximum of `current_sum` seen so far.

**Divide and Conquer (O(n log n), the classic follow-up):**
1. Split the array into left and right halves.
2. Recursively find the best subarray sum fully within the left half, fully within the right half, and the best subarray that **crosses the midpoint**.
3. Return the maximum of the three.

**Time Complexity:** O(n) with Kadane's algorithm; O(n log n) with divide and conquer.
**Space Complexity:** O(1) for Kadane's; O(log n) recursion stack for divide and conquer.

## Reference Solution (Python, Kadane's Algorithm)

```python
def max_sub_array(nums: list[int]) -> int:
    current_sum = nums[0]
    best_sum = nums[0]

    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        best_sum = max(best_sum, current_sum)

    return best_sum
```

## Follow-up Questions Interviewers May Ask

- Can you also implement the divide-and-conquer solution as requested in the classic follow-up?
- How would you return the actual subarray (indices), not just the sum?
- How would you adapt this to find the maximum sum of a **circular** subarray (see LC 918)?

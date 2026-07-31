# 190. Reverse Bits

**Difficulty:** Easy
**Topics:** Divide and Conquer, Bit Manipulation
**Common companies:** Apple, Amazon
**Category (README):** 14. Bit Manipulation & Math

## Problem Description

Reverse bits of a given 32 bits signed integer.

 

**Example 1:**

**Input:** n = 43261596

**Output:** 964176192

**Explanation:**

	
		

			Integer
			Binary
		
		

			43261596
			00000010100101000001111010011100
		
		

			964176192
			00111001011110000010100101000000
		
	

**Example 2:**

**Input:** n = 2147483644

**Output:** 1073741822

**Explanation:**

	
		

			Integer
			Binary
		
		

			2147483644
			01111111111111111111111111111100
		
		

			1073741822
			00111111111111111111111111111110
		
	

 

**Constraints:**

	
- `0 <= n <= 231 - 2`

	
- `n` is even.

 

**Follow up:** If this function is called many times, how would you optimize it?

## Key Idea

Construct bit by bit via shifting

## Approach

This is solved with **bit-by-bit extraction and reconstruction**:

1. Initialize a `result` accumulator to 0.
2. Loop exactly 32 times (one per bit of the input).
3. On each iteration, shift `result` left by one to make room for the next bit, then OR in the lowest bit of `n` (via `n & 1`).
4. Shift `n` right by one to move to its next bit.
5. After 32 iterations, `result` holds `n`'s bits in reverse order.

**Time Complexity:** O(1) — always exactly 32 iterations regardless of input.
**Space Complexity:** O(1) — a single accumulator integer.

## Reference Solution (Python)

```python
def reverseBits(n: int) -> int:
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/reverse-bits/

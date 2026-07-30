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

1. Identify the core pattern for this category: **14. Bit Manipulation & Math**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/reverse-bits/

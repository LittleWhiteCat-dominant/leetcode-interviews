# 167. Two Sum II - Input Array Is Sorted
# https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

def twoSum(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1

    while left < right:
        current_total = numbers[left] + numbers[right]
        if current_total = target:
            return [left+1, right +1]
        
        if current_total < target:
            left += 1
        else:
            right += 1
    
    return []

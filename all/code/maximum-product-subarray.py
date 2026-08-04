def max_product(nums: list[int]) -> int:
    result = nums[0]
    max_product = nums[0]
    min_product = nums[0]

    for num in nums[1:]:
        if num < 0:
            min_product, max_product = max_product, min_product
        
        min_product = min(num, min_product * num)
        max_product = max(num, max_product * num)
        result = max(result, max_product)
    
    return result
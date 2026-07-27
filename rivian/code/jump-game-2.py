def jump(nums: list[int]) -> int:
    if not nums:
        return 0
    
    min_jumps = 0
    current_step = 0
    fastest_reach = nums[0]
    n = len(nums)

    for i in range(n - 1):
        fastest_reach = max(fastest_reach, i + nums[i])
        if i == current_step:
            min_jumps += 1
            current_step = fastest_reach
            if current_step >= n - 1:
                break

    return min_jumps


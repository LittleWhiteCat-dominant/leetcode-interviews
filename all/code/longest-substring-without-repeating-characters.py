# 3. Longest Substring Without Repeating Characters
# https://leetcode.com/problems/longest-substring-without-repeating-characters/

def lengthOfLongestSubstring(s: str) -> int:
    last_seen = {}
    left = 0
    longest_range = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        
        last_seen[ch] = right
        longest_range = max(longest, right - left + 1)
    
    return longest_range

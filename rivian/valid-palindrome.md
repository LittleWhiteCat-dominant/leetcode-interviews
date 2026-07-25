# 125. Valid Palindrome

**Difficulty:** Easy
**Topics:** String, Two Pointers
**Reported at Rivian:** Confirmed — reported as a coding challenge question for the Software Engineer II (RIV-4) role.

## Problem Description

A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string `s`, return `true` *if it is a palindrome, or* `false` *otherwise*.

## Example 1

```
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
```

## Example 2

```
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
```

## Example 3

```
Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.
```

## Constraints

- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.

## Approach

1. Use two pointers, `left` starting at index 0 and `right` starting at the last index.
2. Advance `left` forward and `right` backward, skipping any character that is not alphanumeric.
3. Compare `s[left].lower()` and `s[right].lower()`. If they differ, return `False`.
4. Move both pointers inward and repeat until `left >= right`.
5. If the loop completes without mismatches, return `True`.

This avoids allocating a new cleaned-up string, achieving O(1) extra space.

**Time Complexity:** O(n) — each character is visited at most once.
**Space Complexity:** O(1) extra space (in-place two-pointer scan).

## Reference Solution (Python)

```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

## Follow-up Questions Interviewers May Ask

- How would you solve **Valid Palindrome II** (LC 680), where you're allowed to delete at most one character?
- How would you handle Unicode characters and locale-specific case folding?
- Can you solve this without any built-in string methods like `isalnum()` or `lower()`?

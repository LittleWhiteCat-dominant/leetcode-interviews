# 443. String Compression

**Difficulty:** Medium
**Topics:** String, Two Pointers
**Reported at Rivian:** Tracked in Rivian's known coding question bank (CodeJeet).

## Problem Description

Given an array of characters `chars`, compress it using the following algorithm:

Begin with an empty string `s`. For each group of **consecutive repeating characters** in `chars`:

- If the group's length is 1, append the character to `s`.
- Otherwise, append the character followed by the group's length.

The compressed string `s` should not be returned separately, but instead, be stored **in the input character array `chars`**. Note that group lengths that are 10 or longer will be split into multiple characters in `chars`.

After you are done **modifying the input array**, return *the new length of the array*.

You must write an algorithm that uses only constant extra space.

## Example 1

```
Input: chars = ["a","a","b","b","c","c","c"]
Output: Return 6, and the first 6 characters of the input array should be: ["a","2","b","2","c","3"]
Explanation: The groups are "aa", "bb", and "ccc". This compresses to "a2b2c3".
```

## Example 2

```
Input: chars = ["a"]
Output: Return 1, and the first character of the input array should be: ["a"]
Explanation: The only group is "a", which remains uncompressed since it's a single character.
```

## Example 3

```
Input: chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
Output: Return 4, and the first 4 characters of the input array should be: ["a","b","1","2"].
Explanation: The groups are "a" and "bbbbbbbbbbbb". This compresses to "ab12".
```

## Constraints

- `1 <= chars.length <= 2000`
- `chars[i]` is a lowercase English letter, uppercase English letter, digit, or symbol.

## Approach

1. Use two pointers: a `read` pointer scanning through the array, and a `write` pointer marking where to place the next compressed character(s).
2. For each group of consecutive identical characters:
   - Count the length of the group by advancing `read` while `chars[read] == chars[group_start]`.
   - Write the character at `write`, then advance `write`.
   - If the group length is greater than 1, convert the length to a string and write each digit at `write`, advancing `write` for each digit.
3. Continue until `read` reaches the end of the array.
4. Return `write` as the new length.

**Time Complexity:** O(n) — each character is visited a constant number of times.
**Space Complexity:** O(1) extra space (in-place modification; only the digit string of the count needs temporary storage, which is O(log n) at most).

## Reference Solution (Python)

```python
def compress(chars: list[str]) -> int:
    write = 0
    read = 0
    n = len(chars)

    while read < n:
        char = chars[read]
        group_start = read
        while read < n and chars[read] == char:
            read += 1
        group_len = read - group_start

        chars[write] = char
        write += 1

        if group_len > 1:
            for digit in str(group_len):
                chars[write] = digit
                write += 1

    return write
```

## Follow-up Questions Interviewers May Ask

- How would you handle Unicode characters or multi-byte encodings?
- How would you decompress the string back to its original form?
- What if group lengths could be arbitrarily large — does your in-place write logic still work?

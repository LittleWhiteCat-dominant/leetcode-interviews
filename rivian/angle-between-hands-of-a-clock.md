# 1344. Angle Between Hands of a Clock

**Difficulty:** Medium
**Topics:** Math
**Reported at Rivian:** Confirmed — reported in a Vancouver, BC onsite interview as the "Clock Angle Problem".

## Problem Description

Given two numbers, `hour` and `minutes`, return *the smaller angle (in degrees) formed between the* `hour` *and the* `minute` *hand*.

Answers within `10^-5` of the actual value will be accepted as correct.

## Example 1

```
Input: hour = 12, minutes = 30
Output: 165
```

## Example 2

```
Input: hour = 3, minutes = 30
Output: 75
```

## Example 3

```
Input: hour = 3, minutes = 15
Output: 7.5
```

## Constraints

- `1 <= hour <= 12`
- `0 <= minutes <= 59`

## Approach

1. The minute hand moves `360 / 60 = 6` degrees per minute, so its angle from 12 o'clock is `minutes * 6`.
2. The hour hand moves `360 / 12 = 30` degrees per hour, **plus** it creeps forward `30 / 60 = 0.5` degrees per minute (since it moves continuously, not in discrete jumps). So its angle is `(hour % 12) * 30 + minutes * 0.5`.
3. Compute the absolute difference between the two angles.
4. Since the "smaller" angle around a clock face can never exceed 180°, if the difference is greater than 180, subtract it from 360.

**Time Complexity:** O(1) — constant-time arithmetic.
**Space Complexity:** O(1).

## Reference Solution (Python)

```python
def angle_clock(hour: int, minutes: int) -> float:
    minute_angle = minutes * 6
    hour_angle = (hour % 12) * 30 + minutes * 0.5

    diff = abs(hour_angle - minute_angle)
    return min(diff, 360 - diff)
```

## Follow-up Questions Interviewers May Ask

- How would you handle a 24-hour clock format (treating 13 as 1, etc.)?
- How would you compute the angle for a clock with a second hand as well?
- Can you generalize this to find all times of day when the hour and minute hands overlap exactly?

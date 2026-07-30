# 355. Design Twitter

**Difficulty:** Medium
**Topics:** Hash Table, Linked List, Design, Heap (Priority Queue)
**Common companies:** Amazon, Meta
**Category (README):** 8. Heap / Priority Queue

## Problem Description

Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to see the `10` most recent tweets in the user's news feed.

Implement the `Twitter` class:

	
- `Twitter()` Initializes your twitter object.

	
- `void postTweet(int userId, int tweetId)` Composes a new tweet with ID `tweetId` by the user `userId`. Each call to this function will be made with a unique `tweetId`.

	
- `List<Integer> getNewsFeed(int userId)` Retrieves the `10` most recent tweet IDs in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user themself. Tweets must be **ordered from most recent to least recent**.

	
- `void follow(int followerId, int followeeId)` The user with ID `followerId` started following the user with ID `followeeId`.

	
- `void unfollow(int followerId, int followeeId)` The user with ID `followerId` started unfollowing the user with ID `followeeId`.

 

**Example 1:**

```

**Input**
["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"]
[[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
**Output**
[null, null, [5], null, null, [6, 5], null, [5]]

**Explanation**
Twitter twitter = new Twitter();
twitter.postTweet(1, 5); // User 1 posts a new tweet (id = 5).
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5]. return [5]
twitter.follow(1, 2);    // User 1 follows user 2.
twitter.postTweet(2, 6); // User 2 posts a new tweet (id = 6).
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 2 tweet ids -> [6, 5]. Tweet id 6 should precede tweet id 5 because it is posted after tweet id 5.
twitter.unfollow(1, 2);  // User 1 unfollows user 2.
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5], since user 1 is no longer following user 2.

```

 

**Constraints:**

	
- `1 <= userId, followerId, followeeId <= 500`

	
- `0 <= tweetId <= 104`

	
- All the tweets have **unique** IDs.

	
- At most `3 * 104` calls will be made to `postTweet`, `getNewsFeed`, `follow`, and `unfollow`.

	
- A user cannot follow himself.

## Key Idea

Heap sorted by timestamp + hash map for follow relationships

## Approach

1. Identify the core pattern for this category: **8. Heap / Priority Queue**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** `postTweet` is O(1). `getNewsFeed` is O(F log F) where F is the number of followees, using a heap to merge their most recent tweets. `follow`/`unfollow` are O(1).
**Space Complexity:** O(T + U) — O(T) to store all tweets across users and O(U) for the follow graph.

## Reference Solution (Python)

```python
import heapq
from collections import defaultdict


class Twitter:
    def __init__(self):
        self.timestamp = 0
        self.tweets: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.following: dict[int, set[int]] = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.timestamp, tweetId))
        self.timestamp -= 1

    def getNewsFeed(self, userId: int) -> list[int]:
        heap: list[tuple[int, int, int, int]] = []
        users = self.following[userId] | {userId}

        for uid in users:
            tweets = self.tweets.get(uid)
            if tweets:
                idx = len(tweets) - 1
                time, tweetId = tweets[idx]
                heapq.heappush(heap, (time, tweetId, uid, idx - 1))

        result: list[int] = []
        while heap and len(result) < 10:
            time, tweetId, uid, idx = heapq.heappop(heap)
            result.append(tweetId)
            if idx >= 0:
                next_time, next_tweetId = self.tweets[uid][idx]
                heapq.heappush(heap, (next_time, next_tweetId, uid, idx - 1))

        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)
```

## Reference

- LeetCode: https://leetcode.com/problems/design-twitter/

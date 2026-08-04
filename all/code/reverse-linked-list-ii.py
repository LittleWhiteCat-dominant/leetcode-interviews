# 92. Reverse Linked List II
# https://leetcode.com/problems/reverse-linked-list-ii/

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseBetween(head: ListNode | None, left: int, right: int) -> ListNode | None:
    dummy = ListNode(0, head)
    prev = dummy

    for _ in range(left - 1):
        prev = prev.next
    
    cur = pre.next

    for i in range(right - left):
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = pre.next
        prev.next = nxt
    
    return dummy.next


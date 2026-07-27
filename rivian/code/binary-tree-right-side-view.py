from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def right_side_view(root: "TreeNode | None") -> list[int]:
    if not root:
        return []

    result = []
    
    queue = deque([root])

    while queue:
        level_len = len(queue)
        for i in range(level_len):
            node = queue.popleft()
            if i == level_len - 1:
                result.append(node.val)
            # append next level to the queue
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
    return result

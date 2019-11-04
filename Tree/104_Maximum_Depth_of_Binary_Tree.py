""" Given a binary tree, find its maximum depth.
The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.
    3
   / \
  9  20
    /  \
   15   7
return its depth = 3.
"""
from collections import deque

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def max_depth_v1(root):
    """ Do it recursively.
    Time complexity: O(N), where N is the number of nodes
    Space complexity: in the worst case, the tree is completely unbalanced, e.g. each node has only left child node,
    the recursion call would occur N times (the height of the tree), therefore the storage to keep the call stack
    would be O(N). But in the best case (the tree is completely balanced), the height of the tree would be log(N).
    Therefore, the space complexity in this case would be O(log(N)).
    """
    if not root:
        return 0
    left_depth = max_depth_v1(root.left)
    right_depth = max_depth_v1(root.right)
    return max(left_depth, right_depth) + 1  # Add 1 to account for the root level


def max_depth_v2(root):
    """ We start from a stack which contains the root node and the corresponding depth which is 1. Then we proceed to
    the iterations: pop the current node out of the stack and push the child nodes. The depth is updated at each
    step.
    Time complexity: O(N)
    Space complexity: O(log N)
    """
    if not root:
        return 0
    res, stack = 0, [(root, 0)]
    while stack:
        node, depth = stack.pop()
        if not node.left and not node.right:
            res = max(res, depth)
        else:
            stack.extend([(kid, depth + 1) for kid in (node.left, node.right) if kid])
    return res + 1


def max_depth_v3(root):
    """ Same solution nut using a queue and traversing the tree in BFS.
    Time complexity: O(N)
    Space complexity: O(logN) best case, O(N) worst case
    """
    if not root:
        return 0
    res, queue = 0, deque([root])
    while queue:  # At every iteration,queue holds the nodes of one level of the tree: there is no need to track depth
        res += 1
        n = len(queue)
        for _ in range(n):
            node = queue.popleft()
            queue.extend([kid for kid in (node.left, node.right) if kid])
    return res


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    def test_max_depth(self):
        self.assertEqual(3, max_depth_v1(self.root))
        self.assertEqual(3, max_depth_v2(self.root))
        self.assertEqual(3, max_depth_v3(self.root))


if __name__ == '__main__':
    unittest.main()


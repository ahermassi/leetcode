""" Given a binary tree, return the level order traversal of its nodes' values. (ie, from left to right, level by level).
"""

from collections import deque
import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def level_order_v1(root):
    """ Let's keep nodes of each tree level in the queue structure.
        Initiate queue with a root. While queue is not empty:
            - Start the current level by creating an empty list
            - Compute how many elements should be on the current level : It's queue length
            - Pop out all these elements from the queue and add them into the current level
            - Push their child nodes into the queue for the next level
            - Add the current level's list to the output
    Time complexity: O(N), where N is the number of nodes
    Space complexity: O(N)
    """
    if not root:
        return None
    res, queue = [], deque([root])
    while queue:
        n, level = len(queue), []
        for _ in range(n):
            node = queue.popleft()
            level.append(node.val)
            queue.extend([kid for kid in (node.left, node.right) if kid])
        res.append(level)
    return res


def level_order_v2(root):
    """ Recursive solution which resembles the pre-order traversal. The dfs function uses the current node's level as
        an index of the output list. With each call to node's left/right child, increment the level as we go deeper in
        the tree.
    Time complexity: O(N)
    Space complexity: O(N), in the worst case of a skewed tree, O(logN) average
    """

    def dfs(root, level):
        if not root:
            return
        if level == len(res):  # Add a new level
            res.append([])
        res[level].append(root.val)
        dfs(root.left, level + 1)
        dfs(root.right, level + 1)

    res = []
    dfs(root, 0)  # We initially start at level 0
    return res


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    result = [
        [3],
        [9, 20],
        [15, 7]
    ]

    def test_level_order(self):
        self.assertEqual(self.result, level_order_v1(self.root))
        self.assertEqual(self.result, level_order_v2(self.root))


if __name__ == '__main__':
    unittest.main()

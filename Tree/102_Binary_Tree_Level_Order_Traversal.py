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
        Initiate queue with a root. While queue is not empty :
            Compute how many elements should be on the current level : it's a queue length.
            Pop out all these elements from the queue and add them into the current level.
            Push their child nodes into the queue for the next level.
    Time complexity: O(N) where N is the number of nodes
    Space complexity: O(N)
    """
    if not root:
        return None
    queue, level, ans = deque(), [], []
    queue.append(root)
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.pop()
            level.append(node.val)
            if node.left:
                queue.appendleft(node.left)
            if node.right:
                queue.appendleft(node.right)
        ans.append(level)
    return ans


def level_order_v2(root):
    """ This solution uses a list instead of deque. 'level' is a list of the nodes in the current level. Keep appending
        a list of the values of these nodes to ans and then updating level with all the nodes in the next level (leaves)
        until it reaches an empty level. Python's list comprehension makes it easier to deal with many conditions in a
        concise manner.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    level, ans = [root], []
    while level:
        ans.append([node.val for node in level])
        leaves = []
        for node in level:
            leaves.extend([node.left, node.right])
        level = [leaf for leaf in leaves if leaf]
    return ans


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

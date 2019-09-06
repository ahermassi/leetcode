""" Given a binary tree, return the zigzag level order traversal of its nodes' values. (ie, from left to right, then right to left for the next level and alternate between).

For example:
Given binary tree [3,9,20,null,null,15,7],
    3
   / \
  9  20
    /  \
   15   7
return its zigzag level order traversal as:
[
  [3],
  [20,9],
  [15,7]
] """

import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def zigzag_level_order(root):
    """ Simple BFS traversal. Use a 'direction' flag to indicate the order of appending nodes to the next level.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    level, direction, res = [root], 1, []
    while level:
        values, next_level = [], []
        for _ in range(len(level)):
            node = level.pop()
            values.append(node.val)
            if direction == 1:
                next_level.extend([child for child in (node.left, node.right) if child])
            else:
                next_level.extend([child for child in (node.right, node.left) if child])
        res.append(values)
        direction, level = -direction, next_level
    return res


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    result = [
        [3],
        [20, 9],
        [15, 7]
    ]

    def test_zigzag_level_order(self):
        self.assertEqual(self.result, zigzag_level_order(self.root))


if __name__ == '__main__':
    unittest.main()

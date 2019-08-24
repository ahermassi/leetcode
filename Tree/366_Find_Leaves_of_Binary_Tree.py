""" Given a binary tree, collect a tree's nodes as if you were doing this: Collect and remove all leaves,
repeat until the tree is empty. """

import collections
import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def find_leaves(root):
    """ The idea is to store together the nodes that have same height in a hash map and associate that height to them.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def find_height(root, d):
        if not root:
            return 0
        left_height = find_height(root.left, d)
        right_height = find_height(root.right, d)
        height = max(left_height, right_height) + 1
        d[height].append(root.val)
        return height

    d = collections.defaultdict(list)
    find_height(root, d)
    return list(d.values())


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    output = [[4, 5, 3], [2], [1]]

    def test_find_leaves(self):
        self.assertEqual(self.output, find_leaves(self.root))


if __name__ == '__main__':
    unittest.main()

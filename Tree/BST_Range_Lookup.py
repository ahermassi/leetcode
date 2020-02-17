""" Write a program that takes as input a BST and an interval and returns the BST keys that lie in the interval. """

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def range_lookup_in_bst_v1(root, interval):
    """ We can use the BST property to prune the traversal as follows:
            - If the root of the tree holds a key that is less than the left endpoint of the interval, the left
              subtree cannot contain any node whose key lies in the interval
            - If the root of the tree holds a key that is greater than the right endpoint of the interval, the right
              subtree cannot contain any node whose key lies in the interval
            - Otherwise, the root of the tree holds a key that lies within the interval, and it is possible for both
              the left and right subtrees to contain nodes whose keys lie in the interval.
    Time complexity: O(N), where N is the number of nodes in the interval
    Space complexity: ?
    """

    def helper(root):
        if not root:
            return
        if root.val >= interval[0]:
            helper(root.left)
        if interval[0] <= root.val <= interval[1]:
            res.append(root.val)
        if root.val <= interval[1]:
            helper(root.right)

    res = []
    helper(root)
    return res


def range_lookup_in_bst_v2(root, interval):
    """ Slightly different version. """

    def helper(root):
        if not root:
            return
        if interval[0] <= root.val <= interval[1]:
            helper(root.left)
            res.append(root.val)
            helper(root.right)
        elif root.val < interval[0]:
            helper(root.right)
        else:
            helper(root.left)

    res = []
    helper(root)
    return res


class Test(unittest.TestCase):
    root = TreeNode(6)
    root.left = TreeNode(2)
    root.right = TreeNode(8)
    root.left.left = TreeNode(0)
    root.left.right = TreeNode(4)
    root.right.left = TreeNode(7)
    root.right.right = TreeNode(9)
    interval = [2, 7]
    result = [2, 4, 6, 7]

    def test_range_lookup_in_bst(self):
        self.assertEqual(self.result, range_lookup_in_bst_v1(self.root, self.interval))
        self.assertEqual(self.result, range_lookup_in_bst_v2(self.root, self.interval))


if __name__ == '__main__':
    unittest.main()

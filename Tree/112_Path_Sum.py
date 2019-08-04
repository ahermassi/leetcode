""" Given a binary tree and a sum, determine if the tree has a root-to-leaf path such that adding up all the values
along the path equals the given sum. """

import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def has_path_sum_v1(root, sum):
    """ Do it recursively. If the base case is not valid, substract current node's value from sum and try to find its
        complement in either left or right subtree.
    Time complexity: O(N), in the worst case we visit each node exactly once
    Space complexity: in the worst case, the tree is completely unbalanced and the recursion call would occur N times
    so O(N); in the best case (the tree is completely balanced), it is O(log N) which is the height of the tree
    """
    if not root:
        return False
    if not root.left and not root.right and root.val == sum:
        return True
    sum -= root.val
    return has_path_sum_v1(root.left, sum) or has_path_sum_v1(root.right, sum)


class Test(unittest.TestCase):
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.right.right.right = TreeNode(1)
    root.left.right = TreeNode(4)

    def test_find_target(self):
        self.assertEqual(True, has_path_sum_v1(self.root, 22))


if __name__ == '__main__':
    unittest.main()



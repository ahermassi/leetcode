""" Given an array where elements are sorted in ascending order, convert it to a height balanced BST.
For this problem, a height-balanced binary tree is defined as a binary tree in which the depth of the two subtrees of
every node never differ by more than 1. """

import unittest2 as unittest


# Definition for a  binary tree node


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def sorted_array_to_bst_v1(nums):
    """ For a sorted array, the left half will be in the left subtree, middle value as the root, right half in the
    right subtree. This holds true for every node.
    Time complexity: since Python slicing takes O(N), this algorithm is actually O(N log N)
    Space complexity: O(log N) (draw recursion tree)
    """
    if not nums:
        return
    if len(nums) == 1:
        return TreeNode(nums[0])
    mid = len(nums) // 2
    root = TreeNode(nums[mid])
    root.left = sorted_array_to_bst_v1(nums[:mid])
    root.right = sorted_array_to_bst_v1(nums[mid + 1:])
    return root


def sorted_array_to_bst_v2(nums):
    """ Slicing the array is expensive. It is better to pass the left and right bounds into recursive calls instead.
    Time complexity: O(log N)
    Space complexity: O(log N), there is no case of skewed binary tree because we're creating a balanced BST from the
    start, by picking the middle element every time. It's not possible to have a skewed input or output
    """

    def convert(left, right):
        if left > right:
            return None
        mid = (left + right) // 2
        node = TreeNode(nums[mid])
        node.left = convert(left, mid - 1)
        node.right = convert(mid + 1, right)
        return node

    return convert(0, len(nums) - 1)


class Test(unittest.TestCase):
    data = [-10, -3, 0, 5, 9]

    def test_sorted_array_to_bst(self):
        root = sorted_array_to_bst_v1(self.data)
        self.assertEqual(0, root.val)
        self.assertEqual(-3, root.left.val)
        self.assertEqual(9, root.right.val)
        self.assertEqual(-10, root.left.left.val)
        self.assertEqual(5, root.right.left.val)


if __name__ == '__main__':
    unittest.main()

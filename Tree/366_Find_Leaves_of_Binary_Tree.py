""" Given a binary tree, collect a tree's nodes as if you were doing this: Collect and remove all leaves,
repeat until the tree is empty. """

from collections import defaultdict
import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def find_leaves_v1(root):
    """ The idea is to store together the nodes that have same height in a hash map and associate that height to them.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def find_height(root):
        if not root:
            return -1
        height = 1 + max(find_height(root.left), find_height(root.right))
        heights[height].append(root.val)
        return height

    heights = defaultdict(list)
    find_height(root)
    return heights.values()


def find_leaves_v2(root):
    """ Same solution but without using a hash map. The height of a node is also its index in the result list 'res'.
        For example, leaves, whose heights are 0, are stored in res[0]. Once we find the height of a node, we can put
        it directly into the result.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def find_height(root):
        if not root:
            return -1
        height = 1 + max(find_height(root.left), find_height(root.right))
        if height == len(res):  # This is where check that we have a new height not encountered previously
            res.append([])
        res[height].append(root.val)
        return height

    res = []
    find_height(root)
    return res


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    output = [[4, 5, 3], [2], [1]]

    def test_find_leaves(self):
        self.assertEqual(self.output, find_leaves_v1(self.root))
        self.assertEqual(self.output, find_leaves_v2(self.root))


if __name__ == '__main__':
    unittest.main()

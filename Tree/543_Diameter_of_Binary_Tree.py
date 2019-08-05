""" Given a binary tree, you need to compute the length of the diameter of the tree. The diameter of a binary tree is
the length of the longest path between any two nodes in a tree. This path may or may not pass through the root. """

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def diameter_of_binary_tree(root):
    """ height() function returns the height of the deepest subtree of the passed in node (which is the max of
        either the left child subtree or the right child subtree). diameter (which is what we return at the end) should
        contain information about the largest diameter observed (which would be the maximum of the previous largest
        diameter or the current nodes “diameter”, which the sum of the left and right sub trees). Every node will
        return the two information in the same iteration , height of that node and diameter of tree with respect to
        that node.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def height(root):
        global diameter
        diameter = 0
        if not root:
            return 0
        left_height = height(root.left)
        right_height = height(root.right)
        diameter = max(diameter, left_height + right_height)  # Update diameter as we recursively iterate over each node
        return 1 + max(left_height, right_height)  # The output of the height(root) call just returns the maximum
        # height of the root tree and not the diameter.

    height(root)
    return diameter


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    def test_diameter_of_binary_tree(self):
        self.assertEqual(3, diameter_of_binary_tree(self.root))


if __name__ == '__main__':
    unittest.main()


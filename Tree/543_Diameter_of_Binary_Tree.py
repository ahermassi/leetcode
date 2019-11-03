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
    """ The diameter is the maximum of either:
            1- Passing through the root, in which case the longest path would be using the maximum height of left and
            right child
            2- The diameter of the left child
            3- The diameter of the right child
        So, we can solve this problem with two different cases:
        If the longest path will include the root node, then the longest path must be the height of left child +
        height of right child
        If the longest path does not include the root node, this problem is divided into 2 sub-problem: set left child
        and right child as the new root separately, and repeat previous step.
        Conclusion:
        Diameter of a tree w.r.t root can be defined as:
            Maximum(Diameter of left subtree, Diameter of right subtree, Longest path between two nodes which passes
                through the root)
        Now the diameter of left and right subtree’s can be solved recursively. And Longest path between two nodes
        which passes through the root can be calculated as (1 + height of left subtree + height of right subtree)
    Time complexity: O(N)
    Space complexity: O(N)
    """
    def dfs(root):
        if not root:
            return 0, 0  # Returning diameter, height
        left_diameter, left_height = dfs(root.left)
        right_diameter, right_height = dfs(root.right)
        cur_height = max(left_height, right_height) + 1
        cur_diameter = max(left_height + right_height, left_diameter, right_diameter)  # Cases 1, 2, 3 respectively
        return cur_diameter, cur_height

    return dfs(root)[0]


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


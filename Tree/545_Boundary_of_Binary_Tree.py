""" Given a binary tree, return the values of its boundary in anti-clockwise direction starting from root. Boundary
includes left boundary, leaves, and right boundary in order without duplicate nodes.  (The values of the nodes may
still be duplicates.) """

import unittest2 as unittest


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def boundary_of_binary_tree_v1(root):
    """ Use three different traversals. Pre-order for left boundary , in-order for bottom boundary, and reverse
        post-order (going right node first) for right boundary.
    Time complexity: O(N), where N is the number of nodes in the tree
    Space complexity: O(log N) a balanced binary tree, O(N) worst case for skewed binary tree
    """

    def left_boundary(node):  # Pre-order
        if not node or not node.left and not node.right:  # Exclude leaf nodes from the traversal
            return
        res.append(node.val)
        if node.left:
            left_boundary(node.left)
        else:
            left_boundary(node.right)

    def leaves(node):  # In-order
        if not node:
            return
        leaves(node.left)
        if node != root and not node.left and not node.right:  # Add node only when it's a leaf
            res.append(node.val)
        leaves(node.right)

    def right_boundary(node):  # Reverse post-order
        if not node or not node.left and not node.right:  # Exclude leaf nodes from the traversal
            return
        if node.right:
            right_boundary(node.right)
        else:
            right_boundary(node.left)
        res.append(node.val)

    if not root:
        return None
    res = [root.val]
    left_boundary(root.left)
    leaves(root)
    right_boundary(root.right)
    return res


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.right = TreeNode(2)
    root.right.left = TreeNode(3)
    root.right.right = TreeNode(4)
    result = [1, 3, 4, 2]

    def test_boundary_of_binary_tree(self):
        self.assertEqual(self.result, boundary_of_binary_tree_v1(self.root))


if __name__ == '__main__':
    unittest.main()

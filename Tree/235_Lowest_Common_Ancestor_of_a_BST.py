""" Given a binary search tree (BST), find the lowest common ancestor (LCA) of two given nodes in the BST. """

import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def lowest_common_ancestor_v1(root, p, q):
    """ Lowest common ancestor for two nodes p and q would be the last ancestor node common to both of them. Here last
        is defined in terms of the depth of the node.
        Note: One of p or q would be in the left subtree and the other in the right subtree of the LCA node.
        Start traversing the tree from the root node.
        If both the nodes p and q are in the right subtree, then continue the search with right subtree starting step 1.
        If both the nodes p and q are in the left subtree, then continue the search with left subtree starting step 1.
        If both step 2 and step 3 are not true, this means we have found the node which is common to node p's and q's
        subtrees. and hence we return this common node as the LCA.
    Time complexity: O(N), in the worst case we might be visiting all the nodes of the BST.
    Space complexity: O(1)
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:  # We have found the split point, i.e. the LCA node.
            return root


def lowest_common_ancestor_v2(root, p, q):
    """ Recursive approach. Instead of recursively calling the function, we traverse down the tree iteratively. This is
        possible without using a stack or recursion since we don't need to backtrace to find the LCA node.
    Time complexity: O(N), in the worst case we might be visiting all the nodes of the BST.
    Space complexity: O(N) in the worst case (skewed tree), O(logN) in the case of a balanced BST
    """
    if p.val < root.val and q.val < root.val:
        return lowest_common_ancestor_v2(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lowest_common_ancestor_v2(root.right, p, q)
    return root  # We have found the split point, i.e. the LCA node.


class Test(unittest.TestCase):
    root = TreeNode(6)
    root.left = TreeNode(2)
    root.right = TreeNode(8)
    root.left.left = TreeNode(0)
    root.left.right = TreeNode(4)
    root.right.left = TreeNode(7)
    root.right.right = TreeNode(9)
    values = [(2, 8, 6), (2, 4, 2)]

    def test_lowest_common_ancestor(self):
        for p, q, result in self.values:
            self.assertEqual(result, lowest_common_ancestor_v1(self.root, TreeNode(p), TreeNode(q)).val)
            self.assertEqual(result, lowest_common_ancestor_v2(self.root, TreeNode(p), TreeNode(q)).val)


if __name__ == '__main__':
    unittest.main()

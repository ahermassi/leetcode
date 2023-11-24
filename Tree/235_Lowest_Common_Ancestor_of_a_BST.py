""" Given a binary search tree (BST), find the lowest common ancestor (LCA) of two given nodes in the BST. """

import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# Video explanation: https://youtu.be/gs2LMfuOR9k


def lowest_common_ancestor_v1(root, p, q):
    """ Lowest Common Ancestor of two nodes p and q would be the last ancestor node common to both of them. In this
         context, "last" is defined in terms of the depth of the node.

        Without loss of generality, assume the value at p is smaller (since the problem specified values are distinct,
        it cannot be that p and q hold equal values). Consider the value stored at the root of the BST.
        There are 4 possibilities:

            1- If the root's value is the same as that stored at p or at q, we are done: The root is the LCA.

            2- If the value at p is smaller than the value at the root, and the value at q is greater than the value
                 at the root, the root is the LCA.

            3- If the values at p and q are both smaller than that at the root, the LCA must lie in the left subtree of
               the root.

            4- If both values are larger than that at the root, then the LCA must lie in the right subtree of the root.

        Instead of recursively calling the function, we traverse down the tree iteratively. This is possible without
        using a stack or recursion since we don't need to backtrace to find the LCA node. We just want to find the split
        point, the point from where p and q won't be part of the same subtree or when one is the parent of the other.

        Just walk down from the whole tree's root as long as both p and q are in the same subtree (meaning their values
        are both smaller or both larger than root's). This walks straight from the root to the LCA.

        Start traversing the tree from the root node.
        If both the nodes p and q are in the right subtree, then continue the search with right subtree.
        If both the nodes p and q are in the left subtree, then continue the search with left subtree.
        If the previous two statements are not true, this means we have found the node which is common to node
        p's and q's subtrees, and hence we return this common node as the LCA.

    Time complexity: O(height); O(N), in the worst case when all nodes have only one child (skewed tree) and p and q
    are near the bottom; O(logN) for a balanced BST since we reduce the nodes to check by half after each step
    Space complexity: O(1)
    """
    cur = root
    while cur:
        if p.val < cur.val and q.val < cur.val:
            cur = cur.left
        elif p.val > cur.val and q.val > cur.val:
            cur = cur.right
        else:
            # We have found the split point, i.e. the LCA node: min(p.val, q.val) <= cur.val <= max(p.val, q.val)
            return cur


def lowest_common_ancestor_v2(root, p, q):
    """ Recursive approach.

    Time complexity: O(N), in the worst case when all nodes have only one child (skewed tree) and p and q are near the
    bottom. O(logN) for a balanced BST
    Space complexity: O(N) in the worst case (skewed tree), O(logN) in the case of a balanced BST
    """
    if p.val < root.val and q.val < root.val:
        return lowest_common_ancestor_v2(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lowest_common_ancestor_v2(root.right, p, q)
    return root  # We have found the split point, i.e. the LCA node


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

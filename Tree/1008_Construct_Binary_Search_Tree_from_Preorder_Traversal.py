""" Return the root node of a binary search tree that matches the given pre-order traversal. """

from collections import deque

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def bst_from_preorder_v1(preorder):
    """ In any pre-order traversal sequence, the first key corresponds to the root. The sub-sequence which begins at
        the second element and ends at the last key less than the root, corresponds to the pre-order traversal of the
        root's left subtree. The final sub-sequence, consisting of keys greater than the root, corresponds to the
        pre-order traversal of the root's right subtree.
        We recursively reconstruct the BST by recursively reconstructing the left and right subtrees from the two
        sub-sequences then adding them to the root.
        This could be verified with the help of lower and upper limits for each element as for the 98- Validate BST
        Tree problem.
    Time complexity: O(N), since it performs a constant amount of work per node
    Space complexity: O(h)
    """

    def helper(lower, upper):
        if not preorder or not lower <= preorder[0] <= upper:
            return None
        root = TreeNode(preorder.popleft())
        root.left = helper(lower, root.val)
        root.right = helper(root.val, upper)
        return root

    preorder = deque(preorder)
    return helper(float('-inf'), float('inf'))

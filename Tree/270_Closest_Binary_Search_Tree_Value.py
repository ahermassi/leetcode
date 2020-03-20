""" Given a non-empty binary search tree and a target value, find the value in the BST that is closest to the target.
Note:
Given target value is a floating point.
You are guaranteed to have only one unique value in the BST that is closest to the target. """

# Definition for a binary tree node.


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def closest_value_v1(root, target):
    """ It makes sense to use a binary search: go left if target is smaller than current root value, and go right
        otherwise. Choose the closest to target value at each step. The logic is similar to 285- In-order Successor in
        BST.
    Time complexity: O(h)
    Space complexity: O(1)
    """
    candidate = root
    while root:
        if abs(root.val - target) < abs(candidate.val - target):
            candidate = root
        if root.val > target:
            root = root.left
        else:
            root = root.right
    return candidate.val


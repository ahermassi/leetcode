""" Given the root node of a binary search tree, return the sum of values of all nodes with value between L and R
(inclusive).
The binary search tree is guaranteed to have unique values. """


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def range_sum_bst_v1(root, L, R):
    """ We traverse the tree using a depth first search. If node's value falls outside the range [L, R], (for example
        node.val < L), then we know that only the right branch could have nodes with value inside [L, R].
    Time complexity: O(N), DFS will traverse all nodes in worst case
    Space complexity: O(h)
    """
    if not root:
        return 0
    if root.val < L:
        return range_sum_bst_v1(root.right, L, R)
    if root.val > R:
        return range_sum_bst_v1(root.left, L, R)
    return root.val + range_sum_bst_v1(root.right, L, R) + range_sum_bst_v1(root.left, L, R)


def range_sum_bst_v2(root, L, R):
    """ Another way to look at the problem.
    Time complexity: O(N)
    Space complexity: O(h)
    """
    if not root:
        return 0
    res = 0
    if L <= root.val <= R:
        res += root.val
    if root.val > L:
        res += range_sum_bst_v2(root.left, L, R)  # Left child is a possible candidate
    if root.val < R:
        res += range_sum_bst_v2(root.right, L, R)  # Right child is a possible candidate
    return res

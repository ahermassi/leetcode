"""
Given the root node of a binary search tree, return the sum of values of all nodes with value between L and R (inclusive).

The binary search tree is guaranteed to have unique values.

Submitted to Leetcode by Anouer Hermassi
"""


#  Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def range_sum_bst(root: TreeNode, l: int, r: int) -> int:
    if not root:
        return 0
    elif root.val > r:
        return range_sum_bst(root.left, l, r)
    elif root.val < l:
        return range_sum_bst(root.right, l, r)
    else:
        return root.val + range_sum_bst(root.right, l, r) + range_sum_bst(root.left, l, r)


if __name__ == '__main__':
    root = [10, 5, 15, 3, 7, None, 18]
    L = 7
    R = 15

    print(range_sum_bst(root, L, R))

"""
Runtime: 224 ms, faster than 90.99% of Python3 online submissions for Range Sum of BST.
Memory Usage: 21.6 MB, less than 75.45% of Python3 online submissions for Range Sum of BST.
"""

""" Given the root of a Binary Search Tree (BST), return the minimum absolute difference between the values of any two
different nodes in the tree. """


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def get_minimum_difference(root):
    """ Let's try to solve a simpler problem first. Given a sorted array of integers, find the minimum difference
        between any two integers in the array. To solve this problem, we don't need to check every pair of integers.
        Instead, checking the difference between every two consecutive integers would work. This is because the array
        is sorted. We will make use of this to solve the original problem.

        A unique property of a binary search tree is that an inorder traversal handles the nodes in sorted order.

        Iterate over inorder nodes' values starting from index 1, and for each element at index i, find the difference
        with the element at index i-1 and update the min difference variable accordingly.


    Time complexity: O(N), we visit every node exactly once and iterate over the list of size N to find the minimum
    difference
    Space complexity: O(N), for the call stack and the list of values. The maximum number of active stack calls at a
    time would be the tree's height, which in the worst case would be O(N) when the tree is skewed.
    """

    def inorder(root):
        if not root:
            return
        inorder(root.left)
        values.append(root.val)
        inorder(root.right)

    res, values = float('inf'), []
    inorder(root)
    n = len(values)
    for i in range(1, n):
        res = min(res, values[i] - values[i - 1])
    return res
""" Given two binary search trees, return True if and only if there is a node in the first tree and a node in the
second tree whose values sum up to a given integer target. """


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def two_sum_bst_v1(root1, root2, target):
    """ The idea is simple.
        Traverse the first tree, and store the values of all nodes in a hash set.
        Traverse the second tree and check if any of the complement (target - node.val) of its elements exists in the
        hash set. If yes - return True. If no - return False.
        These functions are slightly modified versions of recursive in-order traversal.
    Time complexity: O(N + M), where N and M are the numbers of nodes in the first and the second tree, respectively
    Space complexity: O(2N + M), N to keep the hash set and up to N + M for the recursive stacks
    """

    def inorder(root):
        if root:
            inorder(root.left)
            vals.add(root.val)
            inorder(root.right)

    def controlled_inorder(root):
        if not root:
            return False
        return controlled_inorder(root.left) or target - root.val in vals or controlled_inorder(root.right)

    vals = set()
    inorder(root1)
    return controlled_inorder(root2)



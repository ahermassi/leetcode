""" Write a program that takes as input a BST and an integer k, and returns the k largest elements in the BST in
decreasing order. """


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def find_k_largest_in_bst(tree, k):
    """ The brute-force approach is to do an in-order traversal, which enumerates keys in ascending order, and return
        the last k visited nodes. A drawback of this approach is that it potentially processes many nodes that cannot
        possibly be in the result, e.g., if k is small and the left subtree is large.
        A better approach is to begin with the desired nodes, and work backwards. We do this by recursing first on the
        right subtree and then on the left subtree. This amounts to a reverse in-order traversal. As soon as we visit k
        nodes, we can halt.
    Time complexity: O(h + k), the number of times the program descends in the tree can be at most h more than the
    number of times it ascends the tree, and each ascent happens after we visit a node in the result.
    Space complexity: O(h)
    """

    def reverse_inorder(root):
        if not root:
            return
        reverse_inorder(root.right)
        if len(res) < k:
            res.append(root.val)
            reverse_inorder(root.left)

    res = []
    reverse_inorder(tree)
    return res

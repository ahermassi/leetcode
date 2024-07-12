""" Write a program that efficiently computes the kth node appearing in an in-order traversal. Assume
that each node stores the number of nodes in the subtree rooted at that node. """


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        self.size = 0


def find_kth_node_binary_tree(root, k):
    """ If k is greater than the number of nodes in the left subtree, the kth node cannot exist in the left subtree.
         More precisely, if the left subtree has L nodes, then the kth node in the original tree is the (k - L - 1)th
         node when we skip the left subtree. Conversely, if k < L, the desired node is in the left subtree.

    Time complexity: O(logN) best case, O(N) worst case of a skewed tree
    Space complexity: O(1)
    """
    cur = root
    while cur:
        left_subtree_size = cur.left.size if cur.left else 0
        if left_subtree_size == k - 1:
            return cur
        if left_subtree_size < k - 1:
            cur = cur.right
        else:
            cur = cur.left
    return None

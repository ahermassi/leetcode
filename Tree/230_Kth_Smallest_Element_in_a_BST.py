""" Given a binary search tree, write a function kthSmallest to find the kth smallest element in it.
Note:
You may assume k is always valid, 1 ≤ k ≤ BST's total elements. """

import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def kth_smallest_v1(root, k):
    """ Iterative approach using stack (in-order). There is no need to build the entire in-order traversal, and we can
        stop after the kth element.
    Time complexity: O(N + k) in the worst case of a skewed BST, since before starting to pop out we have to go down to
    a leaf. O(logN + k) in the best case of a balanced BST.
    Space complexity: O(logN) average case, O(N) worst case
    """
    stack = []
    while stack or root:
        while root:
            stack.append(root)
            root = root.left
        node = stack.pop()
        k -= 1
        if not k:
            return node.val
        root = node.right


def kth_smallest_v2(root, k):
    """ Recursive solution. View comments in inorder_traversal_iterative.py, inorder_v2()
    Time complexity: O(N + k) in the worst case of a skewed BST, since before starting to pop out we have to go down to
    a leaf. O(logN) in the best case of a balanced BST.
    Space complexity: O(logN) average case, O(N) worst case
    """

    def push_leftmost(root):
        while root:
            stack.append(root)
            root = root.left

    stack, count = [], k
    push_leftmost(root)
    while stack:
        node = stack.pop()
        count -= 1
        if not count:
            return node.val
        push_leftmost(node.right)


def kth_smallest_v3(root, k):
    pass
    # This is implemented in 230- Kth Element in Inorder Traversal
    # Follow-up question: What if the BST is modified (insert/delete operations) often and you need to find the kth
    # smallest frequently? How would you optimize the kthSmallest routine?
    # The idea is to maintain rank of each node. Since we need K-th smallest element, we can maintain number of
    # elements of left subtree in every node.
    # Assume that the root is having N nodes in its left subtree:
    # If K = N + 1, root is K-th node.
    # If K < N, we will continue our search (recursion) for the Kth smallest element in the left subtree of root.
    # If K > N + 1, we continue our search in the right subtree for the (K – N – 1)-th smallest element.
    # Note that we need the count of elements in left subtree only.


class Test(unittest.TestCase):
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(4)
    root.left.left.left = TreeNode(2)
    k = 3
    result = 3

    def test_kth_smallest(self):
        self.assertEqual(self.result, kth_smallest_v1(self.root, self.k))
        self.assertEqual(self.result, kth_smallest_v2(self.root, self.k))


if __name__ == '__main__':
    unittest.main()

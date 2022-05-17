""" Given a binary search tree, write a function kthSmallest to find the kth smallest element in it.
Note:
You may assume k is always valid, 1 ≤ k ≤ BST's total elements. """

import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# Video explanation: https://www.youtube.com/watch?v=5LUXSvjmGCw


def kth_smallest_v1(root, k):
    """ Iterative in-order. This way we could speed up the solution because there is no need to build the entire
         inorder traversal, and we can stop once we meet the kth element.

         The idea is that we're maintaining a stack of nodes to visit as well as our current active node. Because we're
         doing an in-order traversal of a BST we always want to visit the leftmost child first since we know that is the
         lowest value (between left, root, right). We want to go left as many times as we can since we want to find the
         smallest value we haven't looked at yet. Only when we reach a node with no left do we evaluate it. (Here, the
         code sets cur = None and requires us the pop the non-empty node off the stack).

        After we've visited that node without a left, we check to see if it has a right by setting our active node to
        its right. From there, we restart our iteration checking if the right node has any left children adding nodes to
        visit later to the stack.

    Time complexity: O(N + k) in the worst case of a skewed BST, since before starting to pop out we have to go down to
    a leaf. O(logN + k) in the best case of a balanced BST.
    Space complexity: O(logN) average case, O(N) worst case, to keep the stack
    """
    stack, cur = [], root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        node = stack.pop()
        k -= 1
        if not k:
            return node.val
        cur = node.right


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
    # This is implemented in 230- Kth Element in In-order Traversal
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

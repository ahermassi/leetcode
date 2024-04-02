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
    """ Iterative inorder.

         We can use the property of BST: inorder traversal of a BST is an array sorted in ascending order. We could
         speed up the solution knowing that there is no need to build the entire inorder traversal, as we can stop once
         we meet the kth element.

         The idea is to maintain a stack of nodes to visit as well as the current active node. Because we're doing an
         inorder traversal of a BST, we always want to visit the leftmost child first since we know that is the lowest
         value (between left, root, right). We want to go left as many times as we can since we want to find the
         smallest value we haven't looked at yet. Only when we reach a node with no left do we evaluate it. Here, the
         code sets cur = None and requires us to pop the non-empty node off the stack.

        After we've visited that node without a left, we check to see if it has a right by setting the current node to
        its right. From there, we restart the iteration and check if the right node has any left children adding nodes
        to visit later to the stack.

    Time complexity: O(N + k) in the worst case of a skewed BST with all the nodes in the left subtree, since before
    starting to pop we have to go down to a leaf. O(logN + k) in the best case of a balanced BST.
    Space complexity: O(logN) average case, O(N) worst case to keep the stack
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
    """ Recursive inorder traversal.

         If the length of our resulting list becomes k, then we have enough elements. Break out of the recursion and
         return the last element in the list.

    Time complexity: O(N)
    Space complexity: O(logN) average case, O(N) worst case
    """
    def inorder(node):
        if not node:
            return
        inorder(node.left)
        if len(inorder_values) == k:
            return
        inorder_values.append(node.val)
        inorder(node.right)

    inorder_values = []
    inorder(root)
    return inorder_values[-1]


def kth_smallest_v3(root, k):
    pass
    # Follow-up question: What if the BST is modified (insert/delete operations) often, and we need to find the kth
    # smallest frequently? How would you optimize the kthSmallest routine?
    # This is implemented in 230- Kth Element in Inorder Traversal and
    # https://leetcode.com/problems/kth-smallest-element-in-a-bst/discuss/63659/What-if-you-could-modify-the-BST-node's-structure
    # The idea is to maintain the rank of each node. Since we need the Kth smallest element, we can maintain the number
    # of nodes of LEFT subtree in every node's data.
    # Assume the root has M nodes in its left subtree:
    # If K = M + 1, i.e. M = K - 1, root is Kth node.
    # If K < M + 1, we will continue our search (recursion) for the Kth smallest element in the left subtree of root.
    # If K > M + 1, we continue our search in the right subtree for the (K – M – 1)th smallest element.
    # Note that we need the count of nodes in the left subtree only.


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

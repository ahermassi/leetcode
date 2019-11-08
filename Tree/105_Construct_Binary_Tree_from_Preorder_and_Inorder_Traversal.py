""" Given preorder and inorder traversal of a tree, construct the binary tree.

Note:
You may assume that duplicates do not exist in the tree.

For example, given

preorder = [3,9,20,15,7]
inorder = [9,3,15,20,7]
Return the following binary tree:

    3
   / \
  9  20
    /  \
   15   7 """
from collections import deque

import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def build_tree_v1(preorder, inorder):
    """ Looking at pre-order traversal, the first value (node 1) must be the root. Then, we find the index of root
        within in-order traversal, and split into two sub problems.
        Example: pre-order = [3, 9, 20, 15, 7], in-order = [9, 3, 15, 20, 7]
                3 is root, [9] is the left subtree, [15, 20, 7] is the right subtree, and so on (recursively)
    Time complexity: O(N^2), since index lookup in in-order list takes O(N)
    Space complexity: O(N)
    """

    def get_tree(inorder):
        if inorder:
            val = preorder.popleft()
            index = inorder.index(val)
            root = TreeNode(inorder[index])
            root.left = get_tree(inorder[:index])
            root.right = get_tree(inorder[index + 1:])
            return root

    preorder = deque(preorder)  # Speed up a bit by making pre-order a queue (cheap left pops as opposed to list.pop(0))
    return get_tree(inorder)


def build_tree_v2(preorder, inorder):
    """ We can improve the previous solution by mapping values to indices of in-order list. This way, we can look up
        the index of root in in-order in constant time.
    Time complexity: O(N)
    Space complexity: O(N) for hash map, O(N) worst case / O(logN) average case for call stack
    """

    def get_tree(inorder_start, inorder_end):
        if inorder_start > inorder_end:
            return None
        root = TreeNode(preorder.popleft())
        index = indices[root.val]
        root.left = get_tree(inorder_start, index - 1)
        root.right = get_tree(index + 1, inorder_end)
        return root

    preorder = deque(preorder)
    indices = {v: i for i, v in enumerate(inorder)}
    return get_tree(0, len(inorder) - 1)  # These boundaries are used only to check if the subtree is empty or not.


def build_tree_v3(preorder, inorder):
    """ Iterative, stack based solution. """
    if not preorder:
        return None
    inorder_indexes = {num: i for i, num in enumerate(inorder)}  # build a map of the indices of the values as they
    # appear in the in-order array
    root = TreeNode(preorder[0])
    stack = [root]  # Initialize the stack of tree nodes
    for i in range(1, len(preorder)):
        val = preorder[i]
        node = TreeNode(val)
        index = inorder_indexes[val]
        if index < inorder_indexes[stack[-1].val]:  # The new node's index in inorder is less than the stack top's
            # index then it is on the left of the last node, so it must be its left child (that's the way preorder
            # works)
            stack[-1].left = node
        else:
            # The new node is on the right of the last node, so it must be the right child of either the last node or
            # one of the last node's ancestors. pop the stack until we either run out of ancestors or the node at the
            # top of the stack is to the right of the new node
            parent = None
            while stack and index > inorder_indexes[stack[-1].val]:
                parent = stack.pop()
            parent.right = node
        stack.append(node)
    return root


class Test(unittest.TestCase):
    preorder = [3, 9, 20, 15, 7]
    inorder = [9, 3, 15, 20, 7]
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    def test_build_tree(self):
        root = build_tree_v2(self.preorder, self.inorder)
        self.assertEqual(3, root.val)
        self.assertEqual(9, root.left.val)
        self.assertEqual(20, root.right.val)
        self.assertEqual(15, root.right.left.val)
        self.assertEqual(7, root.right.right.val)


if __name__ == '__main__':
    unittest.main()

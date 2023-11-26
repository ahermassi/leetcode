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


# Video explanation: https://youtu.be/ihj4IQGZ2zc
def build_tree_v1(preorder, inorder):
    """ The two key observations are:

            - Preorder traversal follows Root -> Left -> Right, therefore, given the preorder array, we have easy
               access to the root which is preorder[0].

            - Inorder traversal follows Left -> Root -> Right, therefore if we know the position of root in the inorder
               list, we can recursively split the entire array into two subtrees.

        Now the idea should be clear enough. We will design a recursive function that will set the first element of
        preorder as the root, and then construct the entire tree. To find the left and right subtrees, it will look for
        the index of root in inorder list, so that everything on the left should be the left subtree, and everything on
        the right should be the right subtree. Both subtrees can be constructed by making another recursive call.

        It is worth noting that we should build a hashmap to record the relation of value -> index for inorder, so that
        we can find the position of root in constant time. Furthermore, if we don't want to create a deque out of the
        preorder  list, we can instead use an integer variable preorderIndex to keep track of the element that will be
        used to construct the root.

        The reason we are given two types of binary tree traversals is because it is not possible to construct binary
        tree from a single traversal.

        Example: preorder = [3, 9, 20, 15, 7], inorder = [9, 3, 15, 20, 7]
        3 is root, [9] is the left subtree, [15, 20, 7] is the right subtree, and so on (recursively)

    Time complexity: O(N), the recursive helper method has a cost of O(1) for each call and is called once for each of
    the N nodes, giving a total of O(N)
    Space complexity: O(N) for hash map, O(N) worst case / O(logN) average case for call stack
    """

    def build_tree(left, right):
        # These boundaries are only used to check if the subtree is empty
        if not left > right:
            # There are no elements to construct the tree
            return None
        root = TreeNode(preorder.popleft())
        index = indices[root.val]
        # Build left and right subtrees excluding 'index' element because it's the root
        root.left = build_tree(left, index - 1)
        root.right = build_tree(index + 1, right)
        return root

    preorder = deque(preorder)  # Speed up a bit by making preorder a queue (cheap left pops as opposed to list.pop(0))
    indices = {val: i for i, val in enumerate(inorder)}
    return build_tree(0, len(inorder) - 1)


def build_tree_v2(preorder, inorder):
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

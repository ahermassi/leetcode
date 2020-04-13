""" Given a Binary Search Tree (BST), convert it to a Greater Tree such that every key of the original BST is changed
to the original key plus sum of all keys greater than the original key in BST.
"""

import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def convert_bst_v1(root):
    """ The key to this solution would be a way to visit nodes in DESCENDING order, keeping a sum of all values that we
        have already visited, and adding that sum to the node's values as we traverse the tree. This technique is known
        as reverse in-order traversal. The basic idea of such a traversal is that before visiting any node in the tree,
        we must first visit all nodes with greater value, keeping sum of all values that we have already visited, and
        adding that sum to the node's values as we traverse the tree. Where are all of these nodes conveniently
        located? In the right subtree.
        We maintain some minor 'global' state so each recursive call can access and modify the current total sum.
        Essentially, we ensure that the current node exists, recurse on the right subtree, visit the current node by
        updating its value and the total sum, and finally recurse on the left subtree. If we know that recursing on
        root.right properly updates the right subtree and that recursing on root.left properly updates the left
        subtree, then we are guaranteed to update all nodes with larger values before the current node and all nodes
        with smaller values after.
    Time complexity: O(N), function gets called on each node no more than once
    Space complexity: O(N) in the worst case
    """

    def reverse_inorder(root):
        if not root:
            return
        reverse_inorder(root.right)  # Go get all the values greater than myself: in the right subtree !
        root.val += total[0]
        total[0] = root.val
        return reverse_inorder(root.left)  # Recurse to the left subtree with total = total + root.val

    total = [0]  # An integer 'total' variable would cause referencing issues
    reverse_inorder(root)
    return root


def convert_bst_v2(root):
    """ Perform a reverse in-order traversal via iteration and a literal stack to emulate the call stack. First,
        we initialize an empty stack and set the current node to the root. Then, we push all of the nodes along the
        path to the rightmost leaf onto the stack. This is equivalent to always processing the right subtree first
        in the recursive solution. Next, we visit the node on the top of our stack, and consider its left subtree.
    Time complexity: O(N)
    Space complexity: O(N), the stack can contain (at most) N nodes
    """
    node, total = root, 0
    stack = []
    while stack or node:
        while node:
            stack.append(node)
            node = node.right
        node = stack.pop()
        total += node.val
        node.val = total
        node = node.left
    return root


class Test(unittest.TestCase):
    root = TreeNode(5)
    root.left = TreeNode(2)
    root.right = TreeNode(8)
    root.left.left = TreeNode(0)
    root.left.right = TreeNode(4)
    root.right.left = TreeNode(7)
    root.right.right = TreeNode(9)
    root = convert_bst_v1(root)

    def test_convert_bst(self):
        self.assertEqual(29, self.root.val)
        self.assertEqual(35, self.root.left.val)
        self.assertEqual(17, self.root.right.val)
        self.assertEqual(35, self.root.left.left.val)
        self.assertEqual(33, self.root.left.right.val)
        self.assertEqual(24, self.root.right.left.val)
        self.assertEqual(9, self.root.right.right.val)


if __name__ == '__main__':
    unittest.main()




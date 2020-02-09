""" Given a binary tree, return the preorder traversal of its nodes' values. """

import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def preorder_traversal_v1(root):
    """ Let's start from the root and then at each iteration pop the current node out of the stack and push its child
        nodes. In the implemented strategy we push nodes into output list following the order Top->Bottom and
        Left->Right, that naturally reproduces pre-order traversal.
    Time complexity: O(N)
    Space complexity: O(logN) best case, O(N) worst case
    """
    if not root:
        return None
    stack, res = [root], []
    while stack:
        node = stack.pop()
        res.append(node.val)
        stack.extend(kid for kid in (node.right, node.left) if kid)
    return res


def preorder_traversal_v2(root):
    """ Inspired from the iterative in-order traversal.
    Time complexity: O(N)
    Space complexity: O(logN) best case, O(N) worst case
    """
    if not root:
        return None
    stack, cur, res = [], root, []
    while stack or cur:
        while cur:
            res.append(cur.val)
            stack.append(cur.right)
            cur = cur.left
        cur = stack.pop()
    return res


class Test(unittest.TestCase):
    root = TreeNode(7)
    root.left = TreeNode(3)
    root.right = TreeNode(15)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(20)
    result = [7, 3, 15, 9, 20]

    def test_inorder_traversal(self):
        self.assertEqual(self.result, preorder_traversal_v1(self.root))
        self.assertEqual(self.result, preorder_traversal_v2(self.root))


if __name__ == '__main__':
    unittest.main()

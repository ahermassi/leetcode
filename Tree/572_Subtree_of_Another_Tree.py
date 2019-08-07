""" Given two non-empty binary trees s and t, check whether tree t has exactly the same structure and node values
with a subtree of s. A subtree of s is a tree consists of a node in s and all of this node's descendants. The tree s
could also be considered as a subtree of itself. """

from collections import deque
import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_subtree(s, t):
    """ We do a BFS traversal of the first tree s. At each node whose value is equal to the second tree t root value,
        we perform a recursive check to verify if the subtree at the current node is equal to the tree t. If it's not
        the case, we carry on the BFS until the stack is empty or a match is found.
    Time complexity: O(N * M) where N is the number of s nodes and M is the number of t nodes. In worst case(skewed
    tree) the traversal takes O(N * M)
    Space complexity: O(N), the depth of the recursion tree can go up to N
    """

    def is_identical(s, t):
        if not s and not t:
            return True
        if s and t and s.val == t.val:
            return is_identical(s.left, t.left) and is_identical(s.right, t.right)

    queue = deque()
    queue.append(s)
    while queue:
        node = queue.popleft()
        if node:
            if node.val == t.val and is_identical(node, t):
                return True
            queue.append(node.left)
            queue.append(node.right)
    return False


class Test(unittest.TestCase):
    root1 = TreeNode(3)
    root1.left = TreeNode(4)
    root1.right = TreeNode(5)
    root1.left.left = TreeNode(1)
    root1.left.right = TreeNode(2)
    root2 = TreeNode(4)
    root2.left = TreeNode(1)
    root2.right = TreeNode(2)
    root3 = TreeNode(4)
    root3.left = TreeNode(1)
    root3.right = TreeNode(2)
    root3.right.left = TreeNode(0)

    def test_is_subtree(self):
        self.assertTrue(is_subtree(self.root1, self.root2))
        self.assertFalse(is_subtree(self.root1, self.root3))


if __name__ == '__main__':
    unittest.main()
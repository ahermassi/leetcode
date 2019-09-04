""" Given a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can
see ordered from top to bottom. """

from collections import deque
import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def right_side_view_v1(root):
    """ Queue version. Perform a BFS on the tree with the right side being always in the front.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    queue, ans = deque([root]), []
    while queue:
        ans.append(queue[-1].val)
        n = len(queue)
        for _ in range(n):
            node = queue.pop()
            if node.right:
                queue.appendleft(node.right)
            if node.left:
                queue.appendleft(node.left)
    return ans


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(4)
    result = [1, 3, 4]

    def test_level_order(self):
        self.assertEqual(self.result, right_side_view_v1(self.root))


if __name__ == '__main__':
    unittest.main()


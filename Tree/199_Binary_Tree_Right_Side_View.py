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
    res, queue = [], deque([root])
    while queue:
        res.append(queue[-1].val)
        n = len(queue)
        for _ in range(n):
            node = queue.popleft()
            queue.extend([kid for kid in (node.left, node.right) if kid])
    return res


def right_side_view_v2(root):
    """ Do a reverse pre-order traversal where the right child is always visited after the root is processed. The idea
        is that this order guarantees that the FIRST node to be seen at each level is the one that is visible from the
        right side view. We use the level as index of the result list.
    Time complexity: O(N)
    Space complexity: O(N) worst case, O(logN) average case
    """
    def dfs(root, depth):
        if not root:
            return
        if depth == len(res):  # Make sure the first element of that level will be added to the result list
            res.append(root.val)
        dfs(root.right, depth + 1)
        dfs(root.left, depth + 1)

    res = []
    dfs(root, 0)
    return res


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(4)
    result = [1, 3, 4]

    def test_right_side_view(self):
        self.assertEqual(self.result, right_side_view_v1(self.root))
        self.assertEqual(self.result, right_side_view_v2(self.root))


if __name__ == '__main__':
    unittest.main()


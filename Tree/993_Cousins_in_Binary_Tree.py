""" Two nodes of a binary tree are cousins if they have the same depth, but have different parents.
We are given the root of a binary tree with unique values, and the values x and y of two different nodes in the tree.
Return true if and only if the nodes corresponding to the values x and y are cousins. """

from collections import deque
import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_cousins(root, x, y):
    """ Perform a BFS to get access to nodes that exist at the same level. The only thing that is left to check is
        whether both x and y exist at the same level and have different parents.
    Time complexity: O(N)
    Space complexity: O(N) used by the queue
    """
    if not root:
        return False
    queue = deque([root])
    while queue:
        n = len(queue)
        x_exist = y_exist = False
        for _ in range(n):
            node = queue.popleft()
            if node.val == x:
                x_exist = True
            elif node.val == y:
                y_exist = True
            if node.left and node.right and {node.left.val, node.right.val} == {x, y}:  # Early exit if x and y are
                # both children of same node. This check ensures that all nodes examined at all (subsequent) levels
                # are not children of same node
                return False
            queue.extend([kid for kid in (node.left, node.right) if kid])
        if x_exist and y_exist:  # x and y exist at the current level and have different parents
            return True


class Test(unittest.TestCase):
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)
    root1.left.left = TreeNode(4)
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(3)
    root2.left.right = TreeNode(4)
    root2.right.right = TreeNode(5)

    def test_is_cousins(self):
        self.assertFalse(is_cousins(self.root1, 4, 3))
        self.assertTrue(is_cousins(self.root2, 5, 4))


if __name__ == '__main__':
    unittest.main()

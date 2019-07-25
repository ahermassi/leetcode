""" Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center). """

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_symmetric(root):
    """ Each two consecutive nodes in the nodes list should be equal. The algorithm works similarly to BFS,
    with some key differences. Each time, two nodes are extracted and their values compared. Then, the right and left
    children of the two nodes are inserted in the queue in opposite order.
    Time complexity: O(N)
    Space complexity: O(N). In the worst case, we have to insert O(n)O(n) nodes in the list
    """
    if not root:
        return True
    nodes = [root.left, root.right]
    while nodes:
        left_node, right_node = nodes.pop(), nodes.pop()
        if not left_node and not right_node:
            continue
        if not left_node or not right_node:
            return False
        if left_node.val != right_node.val:
            return False
        nodes.append(left_node.left)
        nodes.append(right_node.right)
        nodes.append(left_node.right)
        nodes.append(right_node.left)
    return True


class Test(unittest.TestCase):
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(2)
    root1.left.left = TreeNode(3)
    root1.left.right = TreeNode(4)
    root1.right.left = TreeNode(4)
    root1.right.right = TreeNode(3)
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(2)
    root2.left.right = TreeNode(3)
    root2.right.right = TreeNode(3)

    def test_is_symmetric(self):
        self.assertTrue(is_symmetric(self.root1))
        self.assertFalse(is_symmetric(self.root2))


if __name__ == '__main__':
    unittest.main()

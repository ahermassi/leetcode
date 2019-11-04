""" Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center). """

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_symmetric_v1(root):
    """ Level order traversal using BFS.
        Each two consecutive nodes in the nodes list should be equal. The algorithm works similarly to BFS, with some
        key differences. Each time, two nodes are extracted and their values compared. Then, the right and left
        children of the two nodes are inserted in the queue in opposite order.
    Time complexity: O(N)
    Space complexity: O(N), a full binary tree of n nodes has roughly half of those nodes at the lowest level, hence
    O(n) space
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
        nodes.extend([left_node.left, right_node.right])
        nodes.extend([right_node.left, left_node.right])
    return True


def is_symmetric_v2(root):
    """ Two trees are a mirror reflection of each other if:
        1- Their two roots have the same value.
        2- The right subtree of each tree is a mirror reflection of the left subtree of the other tree.
        This is like a person looking at a mirror. The reflection in the mirror has the same head, but the reflection's
        right arm corresponds to the actual person's left arm, and vice versa.
     Time complexity: O(N)
     Space complexity: O(N), the number of recursive calls is bound by the height of the tree. In the worst case,
     the tree is linear and the height is O(N)
     """
    def is_mirror(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        if left.val == right.val:
            return is_mirror(left.left, right.right) and is_mirror(left.right, right.left)
        return False

    if not root:
        return True
    return is_mirror(root.left, root.right)


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
        self.assertTrue(is_symmetric_v1(self.root1))
        self.assertFalse(is_symmetric_v1(self.root2))
        self.assertTrue(is_symmetric_v2(self.root1))
        self.assertFalse(is_symmetric_v2(self.root2))


if __name__ == '__main__':
    unittest.main()

""" Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center). """

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# Video explanation: https://youtu.be/XV7Sg2hJO3Q
def is_symmetric_v1(root):
    """ A tree is symmetric if the left subtree is a mirror reflection of the right subtree.

         Two trees are a mirror reflection of each other if:

            1- Their two roots have the same value
            2- The right subtree of each tree is a mirror reflection of the left subtree of the other tree

         This is like a person looking in a mirror. The reflection in the mirror has the same head, but the reflection's
         right arm corresponds to the actual person's left arm, and vice versa.

     Time complexity: O(N), we traverse the entire input tree once, the total run time is O(N), where N is the total
     number of nodes in the tree
     Space complexity: O(N), the number of recursive calls is bound by the height of the tree. In the worst case,
     the tree is skewed and the height is N
     """
    def is_mirror(left, right):
        if not left and not right:
            return True
        if not left or not right:
            # As soon as a pair fails the test, we can short circuit the check to false
            return False
        if left.val != right.val:
            return False
        return is_mirror(left.left, right.right) and is_mirror(left.right, right.left)

    return is_mirror(root.left, root.right)


# Video explanation: https://youtu.be/Mao9uzxwvmc
def is_symmetric_v2(root):
    """ Iterative implementation of the previous algorithm using a stack.

         Each two consecutive nodes in the stack should be equal. The algorithm works similarly to BFS, with some
         key differences. Each time, two nodes are extracted and their values compared. Then, the right and left
         children of the two nodes are inserted in the queue in opposite order.

    Time complexity: O(N)
    Space complexity: O(N), in the worst case we have to insert O(N) nodes in the stack
    """
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

""" Given a complete binary tree, count the number of nodes.

Note:
Definition of a complete binary tree from Wikipedia:
In a complete binary tree every level, except possibly the last, is completely filled, and all nodes in the last level
are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h. """

from collections import deque
import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def count_nodes_v1(root):
    """ Iterative solution. Perform a BFS on the tree and record each level and add the number of nodes to final count.

    Time complexity: O(N)
    Space complexity: O(2^h) = O(2^logN), since the maximum number of nodes at each level is 2^height of level, and
    height == logN
    """
    if not root:
        return 0
    queue, count = deque([root]), 0
    while queue:
        n = len(queue)
        count += n
        for _ in range(n):
            node = queue.popleft()
            queue.extend([kid for kid in (node.left, node.right) if kid])
    return count


def count_nodes_v2(root):
    """ The height of a complete tree can be found by only going left because all nodes in the last level are as far
         to the left as possible.

            - Find the height of left subtree and right subtree.

            - If left and right subtrees have the same height, then:
                    1) the last node in the last tree level is in the right subtree, and
                    2) the left subtree is a PERFECT tree
               So we take (2 ^ left_height) nodes of the left subtree plus the 1 root node plus recursively the number
               of nodes in the right subtree.

            - If left and right subtrees have different heights, then:
                    1) the last node in the last tree level is in the left subtree, and
                    2) the right subtree is a PERFECT tree
               So we take the (2 ^ right_height) nodes of the right subtree plus the 1 root node plus recursively the
               number of nodes in the left subtree.

         In other words:

            - If left subtree height equals right subtree height then:
                    1) left subtree is perfect binary tree
                    2) right subtree is complete binary tree

            - If left subtree height is greater than right subtree height then:
                    1) left subtree is complete binary tree
                    2) right subtree is perfect binary tree

    Time complexity: we halve the tree in every recursive step, so we have O(logN) steps, and finding the height costs
    O(logN), so overall O(logN ^ 2).
    Space complexity: O(logN ^ 2)
    """

    def get_height(root):
        if not root:
            return 0
        return 1 + get_height(root.left)

    if not root:
        return 0
    left_height, right_height = get_height(root.left), get_height(root.right)
    if left_height == right_height:
        return pow(2, left_height) + count_nodes_v2(root.right)
    return pow(2, right_height) + count_nodes_v2(root.left)


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    result = 6

    def test_count_nodes(self):
        self.assertEqual(self.result, count_nodes_v1(self.root))
        self.assertEqual(self.result, count_nodes_v2(self.root))


if __name__ == '__main__':
    unittest.main()
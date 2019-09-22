""" Given a binary tree, determine if it is a complete binary tree.
Definition of a complete binary tree from Wikipedia:
In a complete binary tree every level, except possibly the last, is completely filled, and all nodes in the last level
are as far left as possible. It can have between 1 and 2 ** h nodes inclusive at the last level h. """

import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_complete_tree(root):
    """ Use BFS to do a level order traversal, add children to the bfs queue, until we met the first empty node.
        For a complete binary tree, there should not be any node after we met an empty one.
        It's using the key feature of level order traversal - from top to bottom and from left to right, so as soon as
        we see null node(previous level or last level), there should be no more non-null node as we continue the
        traversal.
    Time complexity: O(N), where N is the number of nodes in the tree
    Space complexity: O(N)
    """
    nodes, i = [root], 0
    while nodes[i]:
        nodes.append(nodes[i].left)
        nodes.append(nodes[i].right)
        i += 1
    for j in range(i + 1, len(nodes)):
        if nodes[j]:
            return False
    return True


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)

    def test_lowest_common_ancestor(self):
        self.assertTrue(is_complete_tree(self.root))


if __name__ == '__main__':
    unittest.main()
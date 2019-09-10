""" Given a binary tree and a sum, find all root-to-leaf paths where each path's sum equals the given sum.
Note: A leaf is a node with no children. """

import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def path_sum_v1(root, sum):
    """ Good old BFS using stack.
    Time complexity: O(N)
    Space complexity: in the worst case, the tree is completely unbalanced and we would keep all N nodes in the stack
    so O(N); in the best case (the tree is completely balanced), it is O(log N) which is the height of the tree
    """
    if not root:
        return None
    stack, res = [(root, [], sum)], []
    while stack:
        node, path, s = stack.pop()
        if node.val == s and not node.left and not node.right:
            res.append(path + [node.val])
        else:
            stack.extend([(kid, path + [node.val], s - node.val) for kid in (node.right, node.left) if kid])
    return res


class Test(unittest.TestCase):
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.right.right.left = TreeNode(5)
    root.right.right.right = TreeNode(1)
    sum = 22
    result = [
        [5, 4, 11, 2],
        [5, 8, 4, 5]
    ]

    def test_path_sum(self):
        self.assertEqual(self.result, path_sum_v1(self.root, self.sum))


if __name__ == '__main__':
    unittest.main()

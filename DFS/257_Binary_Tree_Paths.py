""" Given a binary tree, return all root-to-leaf paths.
Input:

   1
 /   \
2     3
 \
  5

Output: ["1->2->5", "1->3"]
"""

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def binary_tree_paths_v1(root):
    """ The most intuitive way is to use a recursion. Go through the tree by considering at each step the node itself
        and its children. If node is not a leaf, extend the current path by a node value and call recursively the path
        construction for its children. If node is a leaf, close the current path and add it into the list of paths.
    Time complexity: O(N), we visit each node exactly once
    Space complexity: O(logN),in the worst case when the tree is completely unbalanced, e.g. each node has only one
    child node, the recursion call would occur N times (the height of the tree), therefore the storage to keep the call
    stack would be O(N). But in the best case (the tree is balanced), the height of the tree would be logN.
    """
    def find_paths(root, path):
        path += str(root.val)
        if not root.left and not root.right:
            res.append(path)
            return
        if root.left:
            find_paths(root.left, path + '->')
        if root.right:
            find_paths(root.right, path + '->')

    if not root:
        return None
    res = []
    find_paths(root, '')
    return res


def binary_tree_paths_v2(root):
    """ Initiate the stack by a root node and then at each step we pop out one node and its path. If the popped node
        is a leaf, update the list of all paths. If not, push its child nodes and corresponding paths into stack till
        all nodes are checked.
    Time complexity: O(N) since each node is visited exactly once
    Space complexity: O(N) in the worst case of a skewed tree
    """
    if not root:
        return None
    res, stack = [], [(root, '')]
    while stack:
        node, path = stack.pop()
        path += str(node.val)
        if not node.left and not node.right:
            res.append(path)
        else:
            stack.extend([(kid, path + '->') for kid in (node.left, node.right) if kid])
    return res


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)
    result = ['1->2->5', '1->3']

    def test_binary_tree_paths(self):
        self.assertEqual(self.result, binary_tree_paths_v1(self.root))
        self.assertEqual(self.result, binary_tree_paths_v2(self.root))


if __name__ == '__main__':
    unittest.main()

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
    Space complexity: O(log N), paths contains as many elements as leafs in the tree and hence couldn't be larger than
    log N for the trees containing more than one element. Hence the space complexity is determined by a stack call.
    In the worst case, when the tree is completely unbalanced, e.g. each node has only one child node, the recursion
    call would occur NN times (the height of the tree), therefore the storage to keep the call stack would be O(N).
    But in the best case (the tree is balanced), the height of the tree would be log N.
    """
    if not root:
        return []
    paths = []
    find_paths(root, '', paths)
    return paths


def find_paths(root, path, paths):
    path += str(root.val)
    if root.left:
        find_paths(root.left, path + '->', paths)
    if root.right:
        find_paths(root.right, path + '->', paths)
    if not root.left and not root.right:
        paths.append(path)


def binary_tree_paths_v2(root):
    """ Initiate the stack by a root node and then at each step we pop out one node and its path. If the popped node
    is a leaf, update the list of all paths. If not, push its child nodes and corresponding paths into stack till all
    nodes are checked.
    Time complexity: O(N) since each node is visited exactly once
    Space complexity: O(N)
    """
    if not root:
        return []
    paths, stack = [], [(root, '')]
    while stack:
        node, path = stack.pop()
        if not node.left and not node.right:
            path += str(node.val)
            paths.append(path)
        if node.right:
            stack.append((node.right, path + str(node.val) + '->'))
        if node.left:
            stack.append((node.left, path + str(node.val) + '->'))
    return paths


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
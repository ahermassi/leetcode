""" Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree. According to the
definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node
in T that has both p and q as descendants (where we allow a node to be a descendant of itself).” """

import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def lowest_common_ancestor_v1(root, p, q):
    """ If we have parent pointers for each node we can traverse back from p and q to get their ancestors. The first
        common node we get during this traversal would be the LCA node. We can save the parent pointers in a dictionary
        as we traverse the tree.
        Once we have found both p and q, we get all the ancestors for p using the parent dictionary and add to a set
        called 'ancestor'. Similarly, we traverse through ancestors for node q. If the ancestor is present in the
        ancestors set for p, this means this is the first ancestor common between p and q (while traversing UPWARDS)
        and hence this is the LCA node.
    Time complexity: O(N), in the worst case we might be visiting all the nodes of the binary tree
    Space complexity: O(N), in the worst case space utilized by the stack, the parent pointer dictionary and the
    ancestor set, would be N each, since the height of a skewed binary tree could be N
    """
    parent = {root: None}
    stack = [(root, None)]
    while p not in parent or q not in parent:
        node, par = stack.pop()
        if node:
            parent[node] = par if par else None
            stack.append((node.left, node))
            stack.append((node.right, node))
    p_ancestor = set()
    while p:
        p_ancestor.add(p)
        p = parent[p]
    while q not in p_ancestor:
        q = parent[q]
    return q


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.right.left.left = TreeNode(7)
    root.right.right.right = TreeNode(4)
    p = 5
    q = 4
    result = 5

    def test_lowest_common_ancestor(self):
        self.assertEqual(self.result, lowest_common_ancestor_v1(self.root, self.p, self.q))


if __name__ == '__main__':
    unittest.main()

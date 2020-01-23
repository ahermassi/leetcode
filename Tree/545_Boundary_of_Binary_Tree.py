""" Given a binary tree, return the values of its boundary in anti-clockwise direction starting from root. Boundary
includes left boundary, leaves, and right boundary in order without duplicate nodes.  (The values of the nodes may
still be duplicates.) """

import unittest2 as unittest


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# https://leetcode.com/articles/boundary-of-binary-tree/

def boundary_of_binary_tree_v1(root):
    """ Use three different traversals. Pre-order for left boundary , in-order for bottom boundary, and reverse
        post-order (going right node first) for right boundary.
            - Left Boundary: We keep on traversing the tree towards the left and keep on adding the nodes in the res
              array, provided the current node isn't a leaf node. If at any point, we can't find the left child of a
              node, but its right child exists, we put the right child in the res and continue the process.
            - Leaf Nodes: We make use of a recursive function leaves(root), in which we change the root node for every
              recursive call. If the current root node happens to be a leaf node, it is added to the res array.
              Otherwise, we make the recursive call using the left child of the current node as the new root. After
              this, we make the recursive call using the right child of the current node as the new root.
            - Right Boundary: We perform the same process as the left boundary. But, this time, we traverse towards the
              right. If the right child doesn't exist, we move towards the left child.
    Time complexity: O(N), where N is the number of nodes in the tree. One complete traversal for leaves and two
    traversals up to depth of tree for left and right boundaries
    Space complexity: O(logN), for a balanced binary tree, O(N) worst case for skewed binary tree
    """

    def left_boundary(node):  # Pre-order: Root - Left - Right
        if not node or not node.left and not node.right:  # Exclude leaf nodes from the traversal
            return
        res.append(node.val)
        if node.left:
            left_boundary(node.left)
        else:
            left_boundary(node.right)

    def leaves(node):  # In-order: Left - Root - Right
        if not node:
            return
        leaves(node.left)
        if node != root and not node.left and not node.right:  # Add node only when it's a leaf
            res.append(node.val)
        leaves(node.right)

    def right_boundary(node):  # Reverse post-order: Right - Left - Root
        if not node or not node.left and not node.right:  # Exclude leaf nodes from the traversal
            return
        if node.right:
            right_boundary(node.right)
        else:
            right_boundary(node.left)
        res.append(node.val)

    if not root:
        return None
    res = [root.val]
    left_boundary(root.left)
    leaves(root)
    right_boundary(root.right)
    return res


def boundary_of_binary_tree_v2(root):
    """ To get nodes from the left boundary, we start from root.left and move left if we can, else right, until we
        can't move anymore. The right boundary is similar.
        To get nodes from the leaves, we DFS until we hit a leaf (until node.left and node.right are both None).
        We should take care to add to our stack in the order (right, left) so that they are popped in the order
        (left, right).
        Now armed with all the nodes we could visit, let's visit them in order. As we visit a node, we should skip over
        the ones we've seen before.
    Time complexity: O(N), where N is the number of nodes in the tree
    Space complexity: O(log N) a balanced binary tree, O(N) worst case for skewed binary tree
    """

    def visit(val):
        if val not in visited:
            res.append(val)
            visited.add(val)

    if not root:
        return None
    res, visited = [root.val], set()
    left_boundary = []
    cur = root.left
    while cur:
        left_boundary.append(cur.val)
        cur = cur.left or cur.right
    right_boundary = []
    cur = root.right
    while cur:
        right_boundary.append(cur.val)
        cur = cur.right or cur.left
    leaves, stack = [], [root]
    while stack:
        cur = stack.pop()
        if cur.val != root.val and not cur.left and not cur.right:
            leaves.append(cur.val)
        else:
            stack.extend([kid for kid in (cur.right, cur.left) if kid])
    for i in left_boundary:
        visit(i)
    for i in leaves:
        visit(i)
    for i in reversed(right_boundary):
        visit(i)
    return res


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.right = TreeNode(2)
    root.right.left = TreeNode(3)
    root.right.right = TreeNode(4)
    result = [1, 3, 4, 2]

    def test_boundary_of_binary_tree(self):
        self.assertEqual(self.result, boundary_of_binary_tree_v1(self.root))
        self.assertEqual(self.result, boundary_of_binary_tree_v2(self.root))


if __name__ == '__main__':
    unittest.main()

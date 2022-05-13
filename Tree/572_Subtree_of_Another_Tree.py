""" Given two non-empty binary trees s and t, check whether tree t has exactly the same structure and node values
with a subtree of s. A subtree of s is a tree consists of a node in s and all of this node's descendants. The tree s
could also be considered as a subtree of itself. """

from collections import deque
import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_subtree_v1(root, sub_root):
    """ Recursive DFS.

            1- Start with a node of tree 'root' (lets call this root-node)
            2- Compare the trees forming with root root-node and root 'sub_root'
            3- If the trees match (100- Same Tree logic) then return true
            4- Otherwise, go to step 1 and check for root.left || root.right

    Time complexity: O(N * M), where N and M is the number of nodes in root and sub_root, respectively. In worst case
    (skewed tree) the traversal takes O(N * M)
    Space complexity: O(N), the depth of the recursion tree can go up to N. Recursion stack space is dictated by the
    height of 'root'. Even if 'sub_root' is the bigger tree, 'root' has no clue and will keep checking till its max
    depth.
    """

    def is_identical(s, t):  # Dumb comprehensive comparison off all nodes of s and t
        if not s and not t:
            return True
        if not s or not t or s.val != t.val:
            return False
        return is_identical(s.left, t.left) and is_identical(s.right, t.right)

    if not root:
        return False
    if is_identical(root, sub_root):  # If root and sub_root are equal right off the bat, we're done!
        return True
    # Check if we can find sub_root to the left or right of root
    return is_subtree_v1(root.left, sub_root) or is_subtree_v1(root.right, sub_root)


def is_subtree_v2(root, sub_root):
    """ We do a BFS traversal of the first tree 'root'.

         At each node whose value is identical to the second tree  'sub_root' root value, we perform a recursive check
         to verify if the subtree at the current node is identical to the tree 'sub_root'. If it's not the case, we
         carry on the BFS until the queue is empty or a match is found.

    Time complexity: O(N * M), where N and M is the number of nodes in root and sub_root, respectively
    Space complexity: O(N), since in the worst case the queue will contain all nodes in one level of the binary tree.
    For a full binary tree, the leaf level has ⌈N/2⌉= O(N) leaves.
    """

    def is_identical(s, t):
        if not s and not t:
            return True
        if not s or not t or s.val != t.val:
            return False
        return is_identical(s.left, t.left) and is_identical(s.right, t.right)

    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node.val == sub_root.val and is_identical(node, sub_root):
            return True
        queue.extend([kid for kid in (node.left, node.right) if kid])
    return False


def is_subtree_v3(s, t):
    """ Convert the tree into string representation, then just check whether substring exists in target string.
    Time complexity: O(N * M)
    Space complexity: O(N), the depth of the recursion tree in convert() function
    """

    def convert(root):
        if not root:
            return '$'
        return '^' + str(root.val) + '#' + convert(root.left) + convert(root.right)

    return convert(t) in convert(s)


class Test(unittest.TestCase):
    root1 = TreeNode(3)
    root1.left = TreeNode(4)
    root1.right = TreeNode(5)
    root1.left.left = TreeNode(1)
    root1.left.right = TreeNode(2)
    root2 = TreeNode(4)
    root2.left = TreeNode(1)
    root2.right = TreeNode(2)
    root3 = TreeNode(4)
    root3.left = TreeNode(1)
    root3.right = TreeNode(2)
    root3.right.left = TreeNode(0)

    def test_is_subtree(self):
        self.assertTrue(is_subtree_v1(self.root1, self.root2))
        self.assertFalse(is_subtree_v1(self.root1, self.root3))
        self.assertTrue(is_subtree_v2(self.root1, self.root2))
        self.assertFalse(is_subtree_v2(self.root1, self.root3))
        self.assertTrue(is_subtree_v3(self.root1, self.root2))
        self.assertFalse(is_subtree_v3(self.root1, self.root3))


if __name__ == '__main__':
    unittest.main()
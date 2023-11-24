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


def is_subtree_v0(root, sub_root):
    """ Brute force.

         We perform a BFS (or recursive DFS) traversal of the first tree 'root'.

         At each node, we perform a recursive check to verify if the subtree at the current node is identical to the
         tree 'sub_root'. If it's not the case, we carry on the BFS until the queue is empty or a match is found.

    Time complexity: O(N * M), where N and M is the number of nodes in root and sub_root, respectively
    Space complexity: O(N), since in the worst case the queue will contain all nodes in one level of the binary tree.
    For a full binary tree, the leaf level has ⌈N/2⌉= O(N) leaves.
    """

    def same_tree(s, t):
        if not s and not t:
            return True
        if not s or not t or s.val != t.val:
            return False
        return same_tree(s.left, t.left) and same_tree(s.right, t.right)

    queue = deque([root])
    while queue:
        node = queue.popleft()
        if same_tree(node, sub_root):
            return True
        queue.extend([child for child in (node.left, node.right) if child])
    return False


# Video explanation: https://youtu.be/E36O5SWp-LE
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


def is_subtree_v3(root, sub_root):
    """ Merkle hashing.

        For each node in both trees, we can create node.tag, a hash representing the subtree rooted at that node.
        This hash is formed using the concatenation of the node's value, the merkle of the left child, and the merkle of
        the right child.

        Then, two trees are identical if and only if the merkle hash of their roots are equal. From there, finding the
        answer is straightforward: We simply check if any node in 'root' has node.tag == sub_root.tag.

    Time complexity: O(N + M)
    Space complexity: O(N + M), the depth of the recursion tree in tag_tree() function
    """

    def tag_tree(root):
        if not root:  # We include the hash of null nodes to uniquely identify the tree with its pre-order traversal
            return '#'
        tag = ''.join(['#', str(root.val), '#', tag_tree(root.left), tag_tree(root.right)])  # Without '#' separator,
        # [31, 1, 2] and [3, 11,2] would have the same tag
        root.tag = tag
        return tag

    def dfs(root):
        if not root:
            return False
        if root.tag == sub_root.tag:
            return True
        return dfs(root.left) or dfs(root.right)

    tag_tree(root)
    tag_tree(sub_root)
    return dfs(root)


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
        self.assertTrue(is_subtree_v0(self.root1, self.root2))
        self.assertFalse(is_subtree_v0(self.root1, self.root3))
        self.assertTrue(is_subtree_v1(self.root1, self.root2))
        self.assertFalse(is_subtree_v1(self.root1, self.root3))
        self.assertTrue(is_subtree_v3(self.root1, self.root2))
        self.assertFalse(is_subtree_v3(self.root1, self.root3))


if __name__ == '__main__':
    unittest.main()

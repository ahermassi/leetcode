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


# Video explanation: https://youtu.be/E36O5SWp-LE
def is_subtree_v1(root, sub_root):
    """ Recursive DFS.

        We can traverse the tree rooted at root, and for each node in the tree check if the tree rooted at that node is
        identical to the tree rooted at subRoot. If we find such a node, we can return true. If traversing the entire
        tree rooted at root doesn't yield any such node, we can return false.

        Since we have to check for identicality, again and again, we can write a function same_tree which takes two
        roots of two trees and returns true if the trees are identical and false otherwise.

    Time complexity: O(N * M), where N and M is the number of nodes in root and subRoot, respectively. For every node
    in the first tree we check if the tree rooted at that node is identical to subRoot. This check takes O(M) time.
    Space complexity: O(N + M), the depth of the recursion tree can go up to N. Recursion stack space is dictated by the
    height of 'root'. Each of these calls will have M recursive calls to same_tree.
    """

    def same_tree(s, t):
        if not s and not t:
            return True
        if not s or not t or s.val != t.val:
            return False
        return same_tree(s.left, t.left) and same_tree(s.right, t.right)

    if not root:
        return False
    if same_tree(root, sub_root):
        # If root and sub_root are equal right off the bat, we're done!
        return True
    # Check if we can find sub_root to the left or right of root
    return is_subtree_v1(root.left, sub_root) or is_subtree_v1(root.right, sub_root)


def is_subtree_v2(root, sub_root):
    """ We perform a BFS traversal of the first tree 'root'.

         At each node, we perform a recursive check to verify if the subtree at the current node is identical to the
         tree 'sub_root'. If it's not the case, we carry on the BFS until the queue is empty or a match is found.

         BFS is useful if the node we're looking for is near the root (first few levels).

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


def is_subtree_v3(root, sub_root):
    """ Merkle hashing.

        What we are doing can be broadly labeled as pattern matching. We are trying to match the "tree rooted at root"
        portion with the "tree rooted at subRoot".

        Can we somehow port the string matching to this problem? Yes, we can if there is a mechanism to convert the
        trees into strings and then use string matching.

        The task now is to find a mechanism to transform the trees into strings. Note that serialization must contain
        information about the node values as well as information about the tree structure.

        The most intuitive way is to traverse the tree and add each node's value to the string. Now, there are multiple
        ways to traverse the tree. We can either do a preorder traversal, inorder traversal, postorder traversal, or
        even a level-order traversal. However, it turns out that none of them is sufficient to uniquely identify
        a tree.

        If we include '#' or any other character for the null node while serializing, then we can uniquely identify a
        tree with only one traversal (either preorder or postorder). Note that only inorder traversal (with markers
        for null node) is still not sufficient to uniquely identify a binary tree, as it is difficult to locate the root
        node in the serialized string as the root is visited between the left and right subtrees.

        We want to hash (map) each subtree to a unique value in such a way that if two trees are identical, then their
        hash values are equal.

        We build the hash of each node as a function of the hash of its left and right child. The hash of the root node
        represents the hash of the whole tree because to build the hash of the root node, we used (directly, or
        indirectly) the hash values of all the nodes in its subtrees.

        For each node in both trees, we can create node.tag, an attribute representing the hash of the subtree rooted at
        that node. This hash is formed using the concatenation of the node's value, the merkle of the left child, and
        the merkle of the right child.

        Then, two trees are identical if and only if the merkle hash of their roots are equal. From there, finding the
        answer is straightforward: We simply check if any node in 'root' has node.tag == sub_root.tag.

    Time complexity: O(N + M), we are traversing the tree rooted at root in O(N) time, and we are also traversing the
    tree rooted at subRoot in O(M) time. For each node, we are doing constant time operations.
    Space complexity: O(N + M), the size of the recursion stack in tag_tree function
    """

    def tag_tree(root):
        if not root:
            # We include the hash of null nodes to uniquely identify the tree using its preorder traversal
            return '#'
        # Without '#' separator, [31, 1, 2] and [3, 11,2] would have the same tag
        tag = ''.join(['#', str(root.val), '#', tag_tree(root.left), tag_tree(root.right)])
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
        self.assertTrue(is_subtree_v1(self.root1, self.root2))
        self.assertFalse(is_subtree_v1(self.root1, self.root3))
        self.assertTrue(is_subtree_v2(self.root1, self.root2))
        self.assertFalse(is_subtree_v2(self.root1, self.root3))
        self.assertTrue(is_subtree_v3(self.root1, self.root2))
        self.assertFalse(is_subtree_v3(self.root1, self.root3))


if __name__ == '__main__':
    unittest.main()

""" Given a Binary Search Tree and a target number, return true if there exist two elements in the BST such that
their sum is equal to the given target. """

import unittest2 as unittest

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def find_target_v1(root, k):
    """ Check out problem 1. Two Sum. Same logic.
    While we traverse the tree and insert nodes' values into the set, we also look back to check if current node's
    complement already exists in the set. If it exists, we have found a solution and return immediately.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return False
    vals, nodes = set(), [root]
    while nodes:
        node = nodes.pop()
        if k - node.val in vals:
            return True
        vals.add(node.val)
        nodes.extend([kid for kid in (node.left, node.right) if kid])
    return False


def find_target_v2(root, k):
    """ Recursive DFS version of above solution.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def dfs(root):
        if not root:
            return False
        if k - root.val in vals:
            return True
        vals.add(root.val)
        return dfs(root.left) or dfs(root.right)

    vals = set()
    return dfs(root)


def find_target_v3(root, k):
    """ We make use of the fact that the given tree is a Binary Search Tree. We know that the in-order traversal of a
        BST gives the nodes in ascending order. Thus, we do the in-order traversal of the given tree and put the
        results in a list which contains the nodes sorted in ascending order. Then, we use two pointers which begin
        from the start and end of the array to find if there is a sum k.
    Time complexity: O(N), we need to traverse over the whole tree once to do the inorder traversal
    Space complexity: O(N)
    """

    def inorder(root):
        if not root:
            return
        inorder(root.left)
        vals.append(root.val)
        inorder(root.right)

    vals = []
    inorder(root)
    left, right = 0, len(vals) - 1
    while left < right:
        if vals[left] + vals[right] == k:
            return True
        if vals[left] + vals[right] < k:
            left += 1
        else:
            right -= 1
    return False


class Test(unittest.TestCase):
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.right.right = TreeNode(7)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)

    def test_find_target(self):
        self.assertTrue(find_target_v1(self.root, 9))
        self.assertFalse(find_target_v1(self.root, 28))
        self.assertTrue(find_target_v2(self.root, 9))
        self.assertFalse(find_target_v2(self.root, 28))
        self.assertTrue(find_target_v3(self.root, 9))
        self.assertFalse(find_target_v3(self.root, 28))


if __name__ == '__main__':
    unittest.main()

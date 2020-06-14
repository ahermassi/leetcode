""" Given a binary tree, determine if it is a valid binary search tree (BST). """

from collections import deque
import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def is_valid_bst_v1(root):
    """ Iterative in-order traversal.
        Do we need to keep the whole in-order traversal list? Actually, no. The last added in-order element is enough
        to ensure at each step that the tree is BST (or not). In fact, 'pre' variable is what should've been inserted
        into an in-order list at this point of iteration if 'pre' was a list.
    Time complexity: O(N), in the worst case when the tree is BST or the 'bad' element is a rightmost leaf.
    Space complexity: O(N), to keep stack
    """
    stack, pre = [], float('-inf')
    while stack or root:
        while root:
            stack.append(root)
            root = root.left
        node = stack.pop()
        if node.val <= pre:  # We encountered a value which is less than previous one in in-order traversal
            return False
        pre = node.val
        root = node.right
    return True


def is_valid_bst_v2(root):
    """ Use recursion. Pass down two parameters: lower (which means that all nodes in the the current subtree must
        be greater than this value) and upper (all must be less than it). Compare root of the current subtree
        with these two values. Then, recursively check the left and right subtree of the current one. Take care of the
        values passed down.
    Time complexity: O(N), since we visit each node exactly once
    Space complexity: O(N), since we keep up to the entire tree
    """

    def helper(root, lower, upper):
        if not root:
            return True
        if not lower < root.val < upper:
            return False
        return helper(root.left, lower, root.val) and helper(root.right, root.val, upper)

    return helper(root, float('-inf'), float('inf'))


def is_valid_bst_v3(root):
    """ All the previous approaches explore the left subtree first. Therefore, even if the BST property does not hold
        at a node which is close to the root (e.g., the key stored at the right child is less than the key stored at
        the root), their time complexity is still O(N).
        We can search for violations of the BST property in a BFS manner, thereby reducing the time complexity when the
        property is violated at a node whose depth is small.
        Specifically, we use a queue, where each queue entry contains a node, as well as an upper and a lower bound on
        the keys stored at the subtree rooted at that node. The queue is initialized to the root, with lower bound -∞
        and upper bound +∞. We iteratively check the constraint on each node. If it violates the constraint we stop:
        The BST property has been violated. Otherwise, we add its children along with the corresponding constraint.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    queue = deque([(root, float('-inf'), float('inf'))])
    while queue:
        n = len(queue)
        for _ in range(n):
            node, lower, upper = queue.popleft()
            if not node:
                continue
            if not lower < node.val < upper:
                return False
            queue.append((node.left, lower, node.val))
            queue.append((node.right, node.val, upper))
    return True


class Test(unittest.TestCase):
    root1 = TreeNode(2)
    root1.left = TreeNode(1)
    root1.right = TreeNode(3)
    root2 = TreeNode(5)
    root2.left = TreeNode(1)
    root2.right = TreeNode(4)
    root2.right.left = TreeNode(3)
    root2.right.right = TreeNode(6)

    def test_is_valid_bst(self):
        self.assertTrue(is_valid_bst_v1(self.root1))
        self.assertFalse(is_valid_bst_v1(self.root2))
        self.assertTrue(is_valid_bst_v2(self.root1))
        self.assertFalse(is_valid_bst_v2(self.root2))
        self.assertTrue(is_valid_bst_v3(self.root1))
        self.assertFalse(is_valid_bst_v3(self.root2))


if __name__ == '__main__':
    unittest.main()


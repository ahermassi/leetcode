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
        to ensure that at each step the tree is BST (or not). At each iteration, 'prev' is the node value that
        should've been inserted into the in-order traversal list if 'prev' was a list.

    Time complexity: O(N), in the worst case when the tree is BST or the 'bad' element is a rightmost leaf
    Space complexity: O(N), to keep the stack in the worst case of a skewed BST
    """
    prev = float('-inf')
    stack, cur = [], root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        node = stack.pop()
        if node.val <= prev:  # We encountered a value which is less than previous one in in-order traversal
            return False
        prev = node.val
        cur = node.right
    return True

# Video explanation: https://www.youtube.com/watch?v=s6ATEkipzow


def is_valid_bst_v2(root):
    """  On the first sight, the problem is trivial. Let's traverse the tree and check at each step if
         node.right.val > node.val and node.left.val < node.val. The problem is this approach will not work for all
         cases. Not only the right child should be larger than the node but all the elements in the right subtree.

         That means we should keep both upper and lower limits for each node while traversing the tree, and compare the
         node's value not with children values but with these limits.

        The idea above could be implemented as a recursion. We pass down two parameters: 'lower' (which means that all
        nodes in the current subtree must be greater than this value) and 'upper' (all must be less than it). Compare
        the root of the current subtree with these two values. Then, recursively check the left and right subtrees of
        the current one and update limits accordingly.

    Time complexity: O(N), since we visit each node exactly once
    Space complexity: O(N), worst case to hold the function call stack if the tree is skewed
    """

    def validate(root, lower, upper):
        if not root:
            return True
        if not lower < root.val < upper:
            return False
        return validate(root.left, lower, root.val) and validate(root.right, root.val, upper)

    return validate(root, float('-inf'), float('inf'))


def is_valid_bst_v3(root):
    """ The previous solution might fail when the smallest node has the value Integer.MIN_VALUE or the largest node has
         the value Integer.MAX_VALUE. We can instead pass two null nodes to mark the two boundaries.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    def validate(root, lower, upper):
        if not root:
            return True
        if (lower and root.val <= lower.val) or (upper and root.val >= upper.val):
            return False
        return validate(root.left, lower, root) and validate(root.right, root, upper)

    return validate(root, None, None)


def is_valid_bst_v4(root):
    """ All the previous approaches explore the left subtree first. Therefore, even if the BST property does not hold
         at a node which is close to the root (e.g., the key stored at the right child is less than the key stored at
         the root), their time complexity is still O(N).

         We can search for violations of the BST property in a BFS manner, thereby reducing the time complexity when the
         property is violated at a node whose depth is small.

         Specifically, we use a queue, where each queue entry contains a node, as well as an upper and a lower bound on
         the keys stored at the subtree rooted at that node. The queue is initialized to the root, with lower bound -∞
         and upper bound +∞.

         We iteratively check the constraint on each node. If it violates the constraint we stop: The BST property has
         been violated. Otherwise, we add its children along with the corresponding constraint.

    Time complexity: O(N)
    Space complexity: O(N), in the worst case scenario, we have a completely balanced tree. In such case, the maximum
    space consumption will occur at the last level (at the leaves) where we have N/2 nodes in the queue
    """
    queue = deque([(root, float('-inf'), float('inf'))])
    while queue:
        n = len(queue)
        for _ in range(n):
            node, lower, upper = queue.popleft()
            if not lower < node.val < upper:
                return False
            if node.left:
                queue.append((node.left, lower, node.val))
            if node.right:
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
        self.assertTrue(is_valid_bst_v4(self.root1))
        self.assertFalse(is_valid_bst_v4(self.root2))


if __name__ == '__main__':
    unittest.main()


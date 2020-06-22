""" Given a binary tree, return the inorder traversal of its nodes' values. """

import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def inorder_traversal_v1(root):
    """ Recursive approach. Most straightforward.
    Time complexity: O(N) as we visit each node once
    Space complexity: O(N) worst case, O(logN) average case
    """

    def process(root):
        if not root:
            return
        process(root.left)
        values.append(root.val)
        process(root.right)

    values = []
    process(root)
    return values


def inorder_traversal_v2(root):
    """ Iterative solution. Use stack to store the nodes and iteratively construct the list of values.
    Time complexity: O(N)
    Space complexity: O(logN), this space is allocated dynamically, specifically it is the maximum depth of the
    function call stack for the recursive implementation, O(N) worst case
    """
    values, stack = [], []
    while root or stack:  # If you are wondering why it is 'while root or stack' and not 'while stack', take the
        # example of the tree [1,null,2,3]. 1 is pushed to stack, and since it has no left, it will be promptly popped
        # and 1 added to 'res' list. After that, we move to the right subtree with root = node.right, but the stack is
        # empty at this stage because 1 was the only node in the stack.
        while root:
            stack.append(root)
            root = root.left
        node = stack.pop()
        values.append(node.val)
        root = node.right
    return values


def inorder_traversal_v3(root):
    """ Morris traversal.
        The basic idea is that we create links to the in-order successor and add the data to the result list using the
        links we created, and finally revert the changes.
        1- Start from root
        2- While root is not null:
            2.1- If root has a left child:
                 Make root as right child of the rightmost node in root's left subtree, which is root's in-order
                 predecessor
                 Go to this left child, i.e., root = root.left
            2.2- If root has no left child:
                 Print root’s data
                 Go to the right, i.e., root = root.right
    Time complexity: O(N)
    Space complexity: O(1)
    """
    res = []
    while root:
        if root.left:
            pre = root.left
            while pre.right and pre.right != root:  # Find the in-order predecessor of current node which is the
                # rightmost node in root's left subtree. The second condition in while loop is used when reverting
                pre = pre.right
            if not pre.right:
                pre.right = root  # Make root as right child of the rightmost node in root's left subtree
                root = root.left  # Go to this left child
            else:  # Revert back the changes
                pre.right = None
                res.append(root.val)
                root = root.right
        else:
            res.append(root.val)
            root = root.right
    return res


class Test(unittest.TestCase):
    root = TreeNode(7)
    root.left = TreeNode(3)
    root.right = TreeNode(15)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(20)
    result = [3, 7, 9, 15, 20]

    def test_inorder_traversal(self):
        self.assertEqual(self.result, inorder_traversal_v1(self.root))
        self.assertEqual(self.result, inorder_traversal_v2(self.root))
        self.assertEqual(self.result, inorder_traversal_v3(self.root))


if __name__ == '__main__':
    unittest.main()

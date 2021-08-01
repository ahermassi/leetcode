""" Given a binary tree and a sum, find all root-to-leaf paths where each path's sum equals the given sum.
Note: A leaf is a node with no children. """

import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def path_sum_v1(root, sum):
    """ If we simply consider the depth first traversal on the tree, all it does is traverse one branch after another.
        All we need to do here is to simply execute the depth first traversal and maintain two things along the way:
            - Running sum of all the nodes traversed till that point in recursion
            - List of all those nodes
        If ever the sum becomes equal to the required sum, and the node where this happens is a leaf node, we can
        simply add the list of nodes to our final solution. We keep on doing this for every branch of the tree and we
        will get all the root to leaf paths in this manner that add up to a certain value.
    Time complexity: O(N)
    Space complexity: In the worst case, the tree is completely unbalanced and we would keep all N nodes in the stack
    so O(N); in the best case (the tree is completely balanced), it is O(logN) which is the height of the tree
    """

    def dfs(root, path, remaining):
        if not root:
            return
        if root.val == remaining and not root.left and not root.right:
            path.append(root.val)  # Only when we're sure that this node leads to a correct path we add it to final list
            res.append(path)
            return
        dfs(root.left, path + [root.val], remaining - root.val)
        dfs(root.right, path + [root.val], remaining - root.val)

    res = []
    dfs(root, [], sum)
    return res


def path_sum_v2(root, sum):
    """ Good ol' iterative DFS using stack.
    Time complexity: O(N)
    Space complexity: In the worst case, the tree is completely unbalanced and we would keep all N nodes in the stack
    so O(N); in the best case (the tree is completely balanced), it is O(logN) which is the height of the tree
    """
    if not root:
        return None
    stack, res = [(root, [], sum)], []
    while stack:
        node, path, remaining = stack.pop()
        if node.val == remaining and not node.left and not node.right:
            res.append(path + [node.val])
        else:
            stack.extend([(kid, path + [node.val], remaining - node.val) for kid in (node.right, node.left) if kid])
    return res


def path_sum_v3(root, sum):
    """ DFS with a backtracking flavor.
        During the execution, we first blindly add (or use) the current node and check if it satisfies the condition
        we expect to meet. If it does, we add the path to the resulting list. After removing ourselves from the partial
        list, we basically say "let's try this without me" and explore other branches of the decision tree.
        Here, we are using the same vector path to save the result. If we don't use path.pop(), after we call dfs()
        on the left branch, the path will contain all the elements that were pushed on the left branch. This way, when
        we call dfs() on the right branch, the result on the right branch will be screwed.
        Let's say the sum is 8, and we are at node 4, see the tree below:

                1
               / \
              2   3
             / \
            4   5
        The current solution array is [1, 2, 4], as 4 is the leaf node, we are done with this path. The next node we
        need to scan is 5, and the solution list should look like [1, 2, 5] which represents the correct path, that's
        why we need to remove 4 from the solution array, otherwise, the solution array will be [1, 2, 4, 5].
    Time complexity: O(N^2), for tree traversal and copying the list of nodes
    Space complexity: O(N)
    """
    def dfs(root, remaining, path):
        if not root:
            return
        path.append(root.val)
        if root.val == remaining and not root.left and not root.right:
            res.append(path[:])  # Notice how we add a copy, otherwise we'll store a REFERENCE to path not path itself.
            # Without copying the items from 'path' into a new list, 'res' will contain a reference to the 'path'
            # array, not the array content itself, so changes to 'path' will create changes to the specified index of
            # 'res'.
        else:
            dfs(root.left, remaining - root.val, path)
            dfs(root.right, remaining - root.val, path)
        path.pop()  # Remove current node. This is the backtracking point. If we execute two recursive calls in the
        # else branch and still can't get a match 'path', this means the current node which was already added into the
        # list 'path' can not lead us to the correct answer, so we need to remove it from 'path' and try other possible
        # branches. This is what backtracking is all about.

    res = []
    dfs(root, sum, [])
    return res


class Test(unittest.TestCase):
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.right.right.left = TreeNode(5)
    root.right.right.right = TreeNode(1)
    sum = 22
    result = [
        [5, 4, 11, 2],
        [5, 8, 4, 5]
    ]

    def test_path_sum(self):
        self.assertEqual(self.result, path_sum_v1(self.root, self.sum))
        self.assertEqual(self.result, path_sum_v2(self.root, self.sum))
        self.assertEqual(self.result, path_sum_v3(self.root, self.sum))


if __name__ == '__main__':
    unittest.main()

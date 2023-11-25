""" Given a binary tree, return the level order traversal of its nodes' values. (ie, from left to right, level by level).
"""

from collections import deque
import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def level_order_v1(root):
    """ Let's keep nodes of each tree level in the queue structure. The zero level contains only one node root.
         While the queue is not empty:

            - Start the current level by creating an empty list
            - Compute how many elements should be in the current level : It's queue's size
            - Pop out all these elements from the queue and add them into the current level
            - Push their child nodes into the queue for the next level
            - Add the current level to the output

    Time complexity: O(N), where N is the number of nodes
    Space complexity: O(N), in the worst case scenario, we have a completely balanced tree. In such case, the maximum
    space consumption will occur at the last level (at the leaves) where we have N/2 nodes in the queue
    """
    if not root:
        return None
    res = []
    queue = deque([root])
    while queue:
        n, cur_level = len(queue), []
        for _ in range(n):
            node = queue.popleft()
            cur_level.append(node.val)
            queue.extend([kid for kid in (node.left, node.right) if kid])
        res.append(cur_level)
    return res


def level_order_v2(root):
    """ The simplest way to solve the problem is to use a recursion.

         Let's first ensure that the tree is not empty, and then call recursively the function dfs(node, depth), which
         takes the current node and its level/depth as the arguments.
         This function does the following :

            - The output list here is called res, and hence the current level is just the length of this list,
               len(res). The dfs function uses the current node's depth as index of the output list

            - Append the node value to the last list in levels

            - Process recursively child nodes if they are not null

    Time complexity: O(N)
    Space complexity: O(N), in the worst case of a skewed tree, O(logN) average
    """

    def dfs(root, depth):
        if depth == len(res):  # Start a new level
            res.append([])
        res[depth].append(root.val)
        if root.left:
            dfs(root.left, depth + 1)
        if root.right:
            dfs(root.right, depth + 1)

    res = []
    dfs(root, 0)  # We initially start at depth 0
    return res


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    result = [
        [3],
        [9, 20],
        [15, 7]
    ]

    def test_level_order(self):
        self.assertEqual(self.result, level_order_v1(self.root))
        self.assertEqual(self.result, level_order_v2(self.root))


if __name__ == '__main__':
    unittest.main()

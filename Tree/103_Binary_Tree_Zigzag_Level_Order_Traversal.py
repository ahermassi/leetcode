""" Given a binary tree, return the zigzag level order traversal of its nodes' values. (ie, from left to right, then right to left for the next level and alternate between).

For example:
Given binary tree [3,9,20,null,null,15,7],
    3
   / \
  9  20
    /  \
   15   7
return its zigzag level order traversal as:
[
  [3],
  [20,9],
  [15,7]
] """

from collections import deque
import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def zigzag_level_order_v1(root):
    """ The most intuitive solution would be the BFS approach through which we traverse the tree level-by-level.
         The default ordering of BFS within a single level is from left to right. As a result, we should adjust the BFS
         algorithm a bit to generate the desired zigzag ordering.

         There are several ways to implement the BFS algorithm. One way would be to run a two-level nested loop, with
         the outer loop iterating each level on the tree, and with the inner loop iterating each node within a single
         level.

         We use a 'direction' flag to indicate whether to add the child nodes to the next level in left->right or
         right->left order.

         Note that this implementation uses a stack to mimic the queue.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    level, direction, res = [root], 1, []
    while level:
        values, next_level, n = [], [], len(level)
        for _ in range(n):
            node = level.pop()
            values.append(node.val)
            if direction == 1:
                next_level.extend([child for child in (node.left, node.right) if child])
            else:
                next_level.extend([child for child in (node.right, node.left) if child])
        res.append(values)
        direction, level = -direction, next_level
    return res


def zigzag_level_order_v2(root):
    """ The previous solution uses a stack to mimic the queue. This version uses an actual deque.
        If zigzag = 1, pop_back, push_front, left then right
        If zigzag = -1, pop_front, push_back, right then left
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    res, queue, zigzag = [], deque([root]), 1
    while queue:
        n, values = len(queue), []
        for _ in range(n):
            if zigzag == 1:
                node = queue.pop()
                queue.extendleft([kid for kid in (node.left, node.right) if kid])
            else:
                node = queue.popleft()
                queue.extend([kid for kid in (node.right, node.left) if kid])
            values.append(node.val)
        res.append(values)
        zigzag = -zigzag
    return res


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    result = [
        [3],
        [20, 9],
        [15, 7]
    ]

    def test_zigzag_level_order(self):
        self.assertEqual(self.result, zigzag_level_order_v1(self.root))
        self.assertEqual(self.result, zigzag_level_order_v2(self.root))


if __name__ == '__main__':
    unittest.main()

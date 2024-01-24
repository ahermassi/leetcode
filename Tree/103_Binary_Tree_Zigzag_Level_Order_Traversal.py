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

         direction==1 means process the nodes of the CURRENT level from left to right.
         direction==-1 means process the nodes of the CURRENT level from right to left.

         For the ordering of left-to-right of the NEXT level (current direction==-1), we append the new elements to the
         tail of the queue, so that the element that comes late would get out late as well.

         For the ordering of right-to-left of the NEXT level (current direction==1), we insert the new element to the
         head of the queue, so that the element that comes late would get out first.

    Time complexity: O(N), we visit each node once and only once. In addition, the insertion operation on either end of
    the queue takes a constant time
    Space complexity: O(N), the queue would hold the nodes that are at most across two levels. Therefore, at most, the
    size of the queue would be no more than 2⋅L, where L is the maximum number of nodes that might reside on the
    same level. Since we have a binary tree, the level that contains the most nodes is the one that has all the leave
    nodes in a full binary tree, which is roughly N/2. As a result, we have the space complexity of 2 * N/2 = N
    """
    if not root:
        return None
    res, queue, direction = [], deque([root]), 1
    while queue:
        n, values = len(queue), []
        for _ in range(n):
            node = queue.pop() if direction == 1 else queue.popleft()
            if direction == 1:
                queue.extendleft([kid for kid in (node.left, node.right) if kid])
            else:
                queue.extend([kid for kid in (node.right, node.left) if kid])
            values.append(node.val)
        res.append(values)
        direction = -direction
    return res


def zigzag_level_order_v2(root):
    """ The same BFS approach, but we use a queue to hold the values of the popped nodes of the current level which
         makes it easier to append to either end.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    res = []
    direction = 1
    queue = deque([root])
    while queue:
        n, values = len(queue), deque()
        for _ in range(n):
            node = queue.popleft()
            if direction == 1:
                values.append(node.val)
            else:
                values.appendleft(node.val)
            queue.extend([kid for kid in (node.left, node.right) if kid])
        res.append(values)
        direction *= -1
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

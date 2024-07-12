""" Given a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can
see ordered from top to bottom. """

from collections import deque
import unittest2 as unittest


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def right_side_view_v1(root):
    """ The problem asks to return a list of last elements from all levels, so it's natural to use BFS here.

         Perform a BFS on the tree with the right side being always in the front of the queue.

    Time complexity: O(N)
    Space complexity: O(N), we use the last level to estimate the queue size, and this level could contain up to
    N/2 tree nodes in the case of complete binary tree.
    """
    if not root:
        return None
    res, queue = [], deque([root])
    while queue:
        res.append(queue[0].val)
        n = len(queue)
        for _ in range(n):
            node = queue.popleft()
            # Push the right child before the left child
            queue.extend([kid for kid in (node.right, node.left) if kid])
    return res


# Video explanation: https://youtu.be/d4zLyf32e3I
def right_side_view_v2(root):
    """ Pop the nodes one by one from the current level and push their children into the next level. Each time
         the current level's queue is exhausted, we have the right side element in hand.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    res, queue = [], deque([root])
    while queue:
        right_side_node = None
        n = len(queue)
        for _ in range(n):
            node = queue.popleft()
            right_side_node = node
            queue.extend([kid for kid in (node.left, node.right) if kid])
        if right_side_node:
            res.append(right_side_node.val)
    return res


def right_side_view_v3(root):
    """ Another approach is to push all the nodes in one queue and to use a sentinel node to separate the levels.
         Typically, we could use null as a sentinel.

         The first step is to initialize the first level [root, null]. Once it's done, keep popping the nodes one by one
         from the front of the queue and add their children to the rear.

         Stop each time the popped node is null it means we hit the end of the current level. Each stop is the time to
         update the right side view list and to push null to the queue to mark the end of the next level.

    Time complexity: O(N)
    Space complexity: O(D)
    """
    if not root:
        return None
    res, queue = [], deque([root, None])
    while queue:
        right_side_node = None
        node = queue.popleft()
        while node:
            queue.extend([kid for kid in (node.left, node.right) if kid])
            right_side_node = node
            node = queue.popleft()
        # Now the last popped node is null, i.e. we reached the end of the current level. Hence, right_side_node is the
        # rightmost and is part of the right side view.
        res.append(right_side_node.val)
        if queue:
            queue.append(None)
    return res


def right_side_view_v4(root):
    """  Do a reverse preorder traversal where the right child is always visited after the root is processed. The idea
         is that this order guarantees that the FIRST node to be visited at each level is the one that is visible from
         the right side of the tree. We use the node depth as index of the result list.

         We push one element at each level. So, the size of the output list will actually be equal to the number of
         levels we have already stored in the list. If the node's depth is equal to the size of the result list, that
         means the current level/depth is visited for the first time and the current node is the rightmost.

    Time complexity: O(N)
    Space complexity: O(N) worst case, O(logN) average case, to keep the recursion stack
    """
    def dfs(root, depth):
        if not root:
            return
        if depth == len(res):
            # When we get to this depth for the first time, we add the first node as the rightmost
            res.append(root.val)
        dfs(root.right, depth + 1)
        dfs(root.left, depth + 1)

    res = []
    dfs(root, 0)
    return res


class Test(unittest.TestCase):
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(4)
    result = [1, 3, 4]

    def test_right_side_view(self):
        self.assertEqual(self.result, right_side_view_v1(self.root))
        self.assertEqual(self.result, right_side_view_v2(self.root))
        self.assertEqual(self.result, right_side_view_v3(self.root))
        self.assertEqual(self.result, right_side_view_v4(self.root))


if __name__ == '__main__':
    unittest.main()


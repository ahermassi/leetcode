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
    """ The problem asks to return a list of last elements from all levels, so it's the natural to implement BFS here.

        Perform a BFS on the tree with the right side being always in the back.
        While the queue is not empty:

            - Write down the length of the current level

            - Iterate over i from 0 to level_length - 1:

            - Pop the current node from the queue

            - If i == level_length - 1, then it's the last node in the current level, so push it to result list.

            - Add first left and then right child node into the queue.

    Time complexity: O(N)
    Space complexity: O(D), where D is a tree diameter. Let's use the last level to estimate the queue size. This level
    could contain up to N/2 tree nodes in the case of complete binary tree.
    """
    if not root:
        return None
    res, queue = [], deque([root])
    while queue:
        n = len(queue)
        for i in range(n):
            node = queue.popleft()
            if i == n - 1:
                res.append(node.val)
            queue.extend([kid for kid in (node.left, node.right) if kid])
    return res


def right_side_view_v2(root):
    """ BFS using 2 queues.

        Let's use two queues, one for the current level, and one for the next. The idea is to pop the nodes one by one
        from the current level and push their children into the next level queue. Each time the current queue is empty,
        we have the right side element in hand.

    Time complexity: O(N)
    Space complexity: O(D)
    """
    if not root:
        return None
    res, cur_level = [], deque([root])
    while cur_level:
        next_level = deque()
        node = None
        while cur_level:
            node = cur_level.popleft()
            next_level.extend([kid for kid in (node.left, node.right) if kid])
        res.append(node.val)  # The current level is finished. Its last element is the rightmost node.
        cur_level = next_level
    return res


def right_side_view_v3(root):
    """ Another approach is to push all the nodes in one queue and to use a sentinel node to separate the levels.
        Typically, we could use null as a sentinel.
        The first step is to initiate the first level: root + null as a sentinel. Once it's done, continue to pop the
        nodes one by one from the left and push their children to the right. Stop each time the current node is null
        because it means we hit the end of the current level. Each stop is a time to update a right side view list and
        to push null in the queue to mark the end of the next level.
    Time complexity: O(N)
    Space complexity: O(D)
    """
    if not root:
        return None
    res, queue = [], deque([root, None])
    cur = root
    while queue:
        prev = cur
        cur = queue.popleft()
        while cur:
            queue.extend([kid for kid in (cur.left, cur.right) if kid])
            prev = cur
            cur = queue.popleft()
        res.append(prev.val)  # Now the current node is null, i.e. we reached the end of the current level. Hence the
        # previous node is the rightmost one and makes a part of the right side view.
        if queue:
            queue.append(None)
    return res


def right_side_view_v4(root):
    """ Do a reverse pre-order traversal where the right child is always visited after the root is processed. The idea
        is that this order guarantees that the FIRST node to be seen at each level is the one that is visible from the
        right side view. We use the level as index of the result list.
        We will push one element at each level. So, the size of the res array will actually be equal to the number of
        levels we have already stored the result. If the level of some element is more than the size of res array,
        that means this will be a new level for which we have not pushed anything in the res array. So, we will push
        this element in the res array.
    Time complexity: O(N)
    Space complexity: O(N) worst case, O(logN) average case
    """
    def dfs(root, depth):
        if not root:
            return
        if depth == len(res):  # Make sure the first element of that level will be added to the result list
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


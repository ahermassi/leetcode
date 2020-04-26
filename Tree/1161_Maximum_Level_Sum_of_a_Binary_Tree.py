""" Given the root of a binary tree, the level of its root is 1, the level of its children is 2, and so on.
Return the smallest level X such that the sum of all the values of nodes at level X is maximal. """

from collections import deque


def max_level_sum_v1(root):
    """ Do BFS traversal, level by level. Compute the cur_sum for each level, and update global maximum at the end of
        each level. Return the number of level with max sum.
    Time complexity: O(N)
    Space complexity: O(N), at each moment the queue contains not more than all nodes from one level. The max number of
    nodes at one level is (N + 1)/2, in the case of perfect tree
    """
    max_sum, res = float('-inf'), 1
    queue, cur_level = deque([root]), 1
    while queue:
        n, cur_sum = len(queue), 0
        for _ in range(n):
            node = queue.popleft()
            cur_sum += node.val
            queue.extend([kid for kid in (node.left, node.right) if kid])
        if cur_sum > max_sum:
            max_sum, res = cur_sum, cur_level
        cur_level += 1
        # Could be rewritten much shorter with the help of list comprehension
        # cur_sum = sum([node.val for node in queue])
        # if cur_sum > max_sum:
        #     max_sum, res = cur_sum, cur_level
        # queue = [kid for node in queue for kid in [node.left, node.right] if kid]
        # cur_level += 1
    return res




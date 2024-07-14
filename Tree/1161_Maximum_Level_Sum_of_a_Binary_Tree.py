""" Given the root of a binary tree, the level of its root is 1, the level of its children is 2, and so on.
Return the smallest level X such that the sum of all the values of nodes at level X is maximal. """

from collections import deque, defaultdict


def max_level_sum_v1(root):
    """ We can use a standard breadth-first searchBFS traversal because we need to analyze nodes by level.

         We initialize a queue of integers and an integer cur_level=0 to track the current level. In the queue, we push
         the root node.

         We perform a level-wise traversal, incrementing cur_level by 1 each time we move to a new level. At each
         iteration, we remove all nodes at level, compute the sum of all node values at this level, and insert all their
         neighbouring nodes at level cur_level+1.

         To get the answer, we compare the sum of all node values at the current level to the maximum sum of values
         we've already seen. If the current sum of node values is greater than what we've seen before, we update the
         answer to cur_level, and the current sum becomes the largest sum of values seen thus far. Since we are
         traversing the higher levels first, by only updating the answer when the level sum is greater than what we've
         seen before, we handle the tiebreakers automatically.

    Time complexity: O(N), each node is pushed and popped once
    Space complexity: O(N), at each moment the queue contains not more than all nodes from one level. The max number of
    nodes at one level is (N + 1)/2, in the case of a complete binary tree
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


def max_level_sum_v2(root):
    """ Create a hash map 'level_sum' which keeps a sum for the current level. Implement recursive traversal which
        takes a node and its level as input variables and recursively updates level_sum[level]. Return the key with max
        value in 'level_sum'.
    Time complexity: O(N)
    Space complexity: O(h), O(logN) in the average case of balanced tree and O(N) in the worst case of the skewed tree
    """

    def dfs(root, cur_level):
        if not root:
            return
        level_sum[cur_level] += root.val
        dfs(root.left, cur_level + 1)
        dfs(root.right, cur_level + 1)

    level_sum = defaultdict(int)
    max_sum, max_level = float('-inf'), -1
    dfs(root, 1)
    for level, s in level_sum.items():  # Python 3 dictionaries preserve the insertion order of keys
        if s > max_sum:
            max_sum, max_level = s, level
    return max_level




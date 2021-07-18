""" Find the largest value in each row of a binary tree. """

from collections import deque


def largest_values_v1(root):
    """ Good old BFS.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not root:
        return None
    queue, res = deque([root]), []
    while queue:
        n, max_value = len(queue), float('-inf')
        for _ in range(n):
            node = queue.popleft()
            max_value = max(max_value, node.val)
            queue.extend([child for child in (node.left, node.right) if child])
        res.append(max_value)
    return res


def largest_values_v2(root):
    """ DFS. Do a pre-order traversal and use 'level' to expand result list size and put the max value in the
        appropriate position.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def dfs(root, level):
        if not root:
            return
        if level == len(res):
            res.append(root.val)
        else:
            res[level] = max(res[level], root.val)
        dfs(root.left, level + 1)
        dfs(root.right, level + 1)

    res = []
    dfs(root, 0)
    return res


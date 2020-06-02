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
    """ DFS. Do a pre-order traversal and use depth to expand result list size and put the max value in the appropriate
        position.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def dfs(root, depth):
        if not root:
            return
        if depth == len(res):
            res.append(root.val)
        else:
            res[depth] = max(res[depth], root.val)
        dfs(root.left, depth + 1)
        dfs(root.right, depth + 1)

    res = []
    dfs(root, 0)
    return res


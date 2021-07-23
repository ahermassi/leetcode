""" You have n binary tree nodes numbered from 0 to n - 1 where node i has two children leftChild[i] and rightChild[i].
Return true if and only if all the given nodes form exactly one valid binary tree.

If node i has no left child then leftChild[i] will equal -1, similarly for the right child.

Note that the nodes have no values and that we only use the node numbers in this problem. """

from collections import deque


def validate_binary_tree_nodes_v1(n, leftChild, rightChild):
    """ A tree has a single root node (in-degree = 0) and all other nodes have in-degree = 1. We can use this
        observation to find the root. We can then traverse the tree using that root to check if all nodes have been
        visited exactly once. There can't be any cycles if exactly one node has in-degree of 0 and all other nodes have
        in-degree 1. The traversal can done in a BFS manner and is similar to Kahn's topological sorting used in
        207- Course Schedule.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    indegree = [0] * n
    for node in range(n):
        left, right = leftChild[node], rightChild[node]
        if left != -1:
            indegree[left] += 1
        if right != -1:
            indegree[right] += 1
        if indegree[left] > 1 or indegree[right] > 1:  # If in-degree exceeds 1 return false
            return False
    queue = deque([node for node in range(n) if indegree[node] == 0])
    if len(queue) != 1:  # We have multiple roots
        return False
    visited = set()
    while queue:
        node = queue.popleft()
        visited.add(node)
        queue.extend([child for child in (leftChild[node], rightChild[node]) if child != -1])
    return len(visited) == n  # If len(visited) != n it means that some nodes are unreachable


def validate_binary_tree_nodes_v2(n, leftChild, rightChild):
    """ This time we use DFS to traverse the tree using the root and check if all nodes have been visited exactly once.
        dfs(root) checks whether the graph is connected, i.e. whether all nodes are reachable from the node 'root'.
        We add all nodes reachable from the root to a hash set.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def dfs(root):
        visited.add(root)
        for child in leftChild[root], rightChild[root]:
            if child != -1 and child not in visited:
                dfs(child)

    parents = [0] * n
    for node in range(n):
        left, right = leftChild[node], rightChild[node]
        if left != -1:
            parents[left] += 1
        if right != -1:
            parents[right] += 1
        if parents[left] > 1 or parents[right] > 1:
            return False
    root = -1
    for node in range(n):
        if parents[node] == 0:
            if root != -1:
                return False
            root = node
    visited = set()
    dfs(root)
    return len(visited) == n  # If the total number of visited nodes is not n, it means there are islands



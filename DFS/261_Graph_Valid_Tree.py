""" Given n nodes labeled from 0 to n-1 and a list of undirected edges (each edge is a pair of nodes), write a function
to check whether these edges make up a valid tree. """

from collections import defaultdict, deque
import unittest2 as unittest


def valid_tree_v1(n, edges):
    """ According to the definition of tree on Wikipedia: 'a tree is an undirected graph in which any two vertices are
        connected by exactly one path. In other words, any CONNECTED graph without simple CYCLES is a tree.'
        Therefore, we have to check 2 things:
            1- Whether there is a cycle
            2- Whether all vertices are connected (the number of connected components is 1)
        Finding a cycle is a simple extension of cycle detection algorithm for directed graphs, except we need to
        include the parent node as well in the DFS call.
    Time complexity: O(|V| + |E|)
    Space complexity: O(|V| + |E|)
    """

    def dfs(vertex, parent):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor in visited and neighbor != parent:  # If a neighbor was previously visited and this neighbor is
                # NOT my parent (the graph is undirected, so A-B == A->B and B->A), then we have a cycle.
                # Example: edges = [0, 1], graph = {0: [1], 1: [0, 2]}
                # Mark 0 as visited and proceed to its neighbors, which is only node 1. When dfs() is called with
                # (vertex=1, parent=0), we again proceed to examine the neighbors of 1: node 0 is there, but 0 is
                # 1's parent due to the undirected nature of the graph.
                return False
            if neighbor not in visited and not dfs(neighbor, vertex):  # 'neighbor' has not been visited, so let's
                # check if there's cycle starting from 'neighbor'
                return False
        return True

    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    visited = set()
    if not dfs(0, -1):  # Make sure there's no cycle
        return False
    if any(i for i in range(n) if i not in visited):  # Make sure all vertices are connected. If the graph is a tree,
        # all nodes will be marked as visited by the end of DFS.
        return False
    return True


def valid_tree_v2(n, edges):
    """ BFS version of the previous algorithm.
    Time complexity: O(|V| + |E|)
    Space complexity: O(|V| + |E|)
    """
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    visited = set()
    queue = deque([(0, -1)])
    while queue:
        vertex, parent = queue.popleft()
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor in visited and neighbor != parent:
                return False
            if neighbor not in visited:
                queue.append((neighbor, vertex))
    if any(i for i in range(n) if i not in visited):
        return False
    return True


class Test(unittest.TestCase):
    data = [(5, [[0, 1], [0, 2], [0, 3], [1, 4]], True), (5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]], False)]

    def test_valid_tree(self):
        for test_n, test_edges, result in self.data:
            self.assertEqual(result, valid_tree_v1(test_n, test_edges))
            self.assertEqual(result, valid_tree_v2(test_n, test_edges))


if __name__ == '__main__':
    unittest.main()

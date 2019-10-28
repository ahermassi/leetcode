""" Read description on Leetcode """

from collections import defaultdict
import unittest2 as unittest


def find_redundant_connection_v1(edges):
    """ The algorithm is based on the following fact in graph theory:
            An undirected connected graph with no cycle is a tree.
        The statement of the problem guarantees that by deleting one and only one edge the graph is a tree, so we know
        it is connected and has one cycle. Our goal is to find the edge in this cycle with the largest index and return
        it.
        For each edge (u, v), traverse the graph with a DFS to see if we can connect u to v. If we can, then it must be
        the duplicate edge.
    Time complexity: O(N ** 2), where N is the number of vertices (and also the number of edges) in the graph. In the
    worst case, for every edge we include, we have to search every previously-occurring edge of the graph.
    Space complexity: O(N)
    """

    def dfs(u, v):
        if u not in visited:
            visited.add(u)
            if u == v:
                return True
            for neighbor in graph[u]:
                if dfs(neighbor, v):
                    return True
        return False

    graph = defaultdict(set)
    for u, v in edges:
        visited = set()
        if u in graph and v in graph and dfs(u, v):
            return [u, v]
        graph[u].add(v)
        graph[v].add(u)


# https://leetcode.com/articles/redundant-connection/
# https://leetcode.com/problems/redundant-connection/discuss/123819/Union-Find-with-Explanations-(Java-Python)

def find_redundant_connection_v2(edges):
    """ Union-find solution. We simply find the first edge occurring in the graph that is already connected.
    Time complexity: O(N), where N is the number of vertices (and also the number of edges) in the graph
    Space complexity: O(N)
    """

    def find(x):
        if parent[x] == 0:
            return x
        parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX == rootY:
            return False
        parent[rootX] = rootY
        return True

    parent = [0] * len(edges)
    for x, y in edges:
        if not union(x - 1, y - 1):
            return [x, y]


class Test(unittest.TestCase):
    data = [([[1, 2], [1, 3], [2, 3]], [2, 3]), ([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]], [1, 4])]

    def test_find_redundant_connection(self):
        for test_edges, result in self.data:
            self.assertEqual(result, find_redundant_connection_v1(test_edges))
            self.assertEqual(result, find_redundant_connection_v2(test_edges))


if __name__ == '__main__':
    unittest.main()

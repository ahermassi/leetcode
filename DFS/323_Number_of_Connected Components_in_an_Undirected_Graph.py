""" Given n nodes labeled from 0 to n - 1 and a list of undirected edges (each edge is a pair of nodes), write a
function to find the number of connected components in an undirected graph. """

from collections import defaultdict, deque
import unittest2 as unittest


def count_components_v1(n, edges):
    """ If we run DFS from each of the nodes, all connected components will be visited if they are a part of the
        initial node to be explored. If not, then there is some other connected component to be found from another node.
        Once the DFS finishes, we increment the count because this means we're exploring another set of connected
        components.
    Time complexity: O(|V| + |E|), where V is the number of vertices (n) and E is the number of edges (length of edges'
    list)
    Space complexity: O(|V|^2) worst case when every node is connected to all other nodes, which means V keys in the
    hah map and each has an V-1 size list. O(|V| + |E|) average case
    """

    def dfs(vertex):
        if vertex in visited:
            return
        visited.add(vertex)
        for neighbor in graph[vertex]:
            dfs(neighbor)

    visited, res = set(), 0
    graph = defaultdict(list)
    for src, dest in edges:
        graph[src].append(dest)
        graph[dest].append(src)
    for i in range(n):
        if i not in visited:
            dfs(i)
            res += 1
    return res


def count_components_v2(n, edges):
    """ BFS is the same idea, except where do we start BFS from? If we start it from any node, we may only find that
        one connected component, so instead we start it from all nodes and visit the max number of nodes using BFS and
        only increment the count once we visit a new node from the adjacency list, meaning we only increment the count
        once we're exploring a new connected component.

    """
    res, visited = 0, set()
    graph = defaultdict(list)
    for src, dest in edges:
        graph[src].append(dest)
        graph[dest].append(src)
    for i in range(n):
        if i not in visited:
            res += 1
            queue = deque([i])
            while queue:
                vertex = queue.popleft()
                visited.add(vertex)
                for neighbor in graph[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
    return res


class Test(unittest.TestCase):
    data = [(5, [[0, 1], [1, 2], [3, 4]], 2), (5, [[0, 1], [1, 2], [2, 3], [3, 4]], 1)]

    def test_count_components(self):
        for test_n, test_edges, result in self.data:
            self.assertEqual(result, count_components_v1(test_n, test_edges))
            self.assertEqual(result, count_components_v2(test_n, test_edges))


if __name__ == '__main__':
    unittest.main()
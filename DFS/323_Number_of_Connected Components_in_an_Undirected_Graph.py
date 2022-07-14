""" Given n nodes labeled from 0 to n - 1 and a list of undirected edges (each edge is a pair of nodes), write a
function to find the number of connected components in an undirected graph. """

from collections import defaultdict, deque
import unittest2 as unittest


def count_components_v1(n, edges):
    """ In an undirected graph, a connected component is a subgraph in which each pair of vertices is connected via a
         path. So essentially, all vertices in a connected component are reachable from one another.

         If we run DFS, starting from a particular vertex, it will continue to visit the vertices depth-wise until there
         are no more adjacent vertices left to visit. Thus, it will visit all the vertices within the connected
         component that contains the starting vertex.

         Each time we finish exploring a connected component, we can find another vertex that has not been visited yet,
         and start a new DFS from there.

         The number of times we start a new DFS will be the number of connected components.

    Time complexity: O(|V| + |E|), where V is the number of vertices (n) and E is the number of edges. Building the
    adjacency list will take O(E) operations, as we iterate over the list of edges once, and insert each edge into two
    lists. During the DFS traversal, each vertex will only be visited once. This is because we mark each vertex as
    visited as soon as we see it, and then we only visit vertices that are not marked as visited. In addition, when we
    iterate over the edge list of each vertex, we look at each edge once. This has a total cost of O(V + E).
    Space complexity: O(|V| + |E|), building the adjacency list will take O(E) space. To keep track of visited vertices,
    a hash set of size O(V) is required. Also, the runtime stack for DFS will use O(V) space.
    """

    def dfs(vertex):
        if vertex in visited:
            return
        visited.add(vertex)
        for neighbor in graph[vertex]:
            dfs(neighbor)

    graph = defaultdict(list)
    for src, dest in edges:
        graph[src].append(dest)
        graph[dest].append(src)
    visited, res = set(), 0
    for vertex in range(n):
        if vertex not in visited:
            dfs(vertex)
            res += 1
    return res


def count_components_v2(n, edges):
    """ BFS is the same idea, except where do we start BFS from?

         If we start it from any node, we may only find that one connected component, so instead we start it from all
         nodes and visit the max number of nodes using BFS and only increment the count once we visit a new node from
         the adjacency list, meaning we only increment the count when we're exploring a new connected component.
    """
    graph = defaultdict(list)
    for src, dest in edges:
        graph[src].append(dest)
        graph[dest].append(src)
    res, visited = 0, set()
    for i in range(n):
        if i not in visited:
            queue = deque([i])
            while queue:
                vertex = queue.popleft()
                visited.add(vertex)
                for neighbor in graph[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
            res += 1
    return res


class Test(unittest.TestCase):
    data = [(5, [[0, 1], [1, 2], [3, 4]], 2), (5, [[0, 1], [1, 2], [2, 3], [3, 4]], 1)]

    def test_count_components(self):
        for test_n, test_edges, result in self.data:
            self.assertEqual(result, count_components_v1(test_n, test_edges))
            self.assertEqual(result, count_components_v2(test_n, test_edges))


if __name__ == '__main__':
    unittest.main()
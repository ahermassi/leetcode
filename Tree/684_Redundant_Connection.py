""" In this problem, a tree is an undirected graph that is connected and has no cycles.

You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added
edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented
as an array edges of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the
graph.

Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there are multiple answers,
return the answer that occurs last in the input. """

from collections import defaultdict
import unittest2 as unittest

# Video explanation (first 7 minutes): https://www.youtube.com/watch?v=FXWRE67PLL0


def find_redundant_connection_v1(edges):
    """ The algorithm is based on the following fact in graph theory:

                An undirected connected graph with no cycle is a tree

        The statement of the problem guarantees that by deleting one and only one edge the graph is a tree.
        So, we know it is connected and has exactly one cycle. Our goal is to find the edge in this cycle with the
        largest index and return it.

        For each edge (u, v), traverse the graph with DFS to see if we can already connect u to v. If we can, then it
        must be the duplicate edge.

        We're basically doing cycle prevention (and not detection). We're building the graph one edge at a time.
        However, before adding an edge between u and v, we first check if there is already a path between them,
        avoiding a cycle.

        How does the algorithm handle "If there are multiple answers, return the answer that occurs last in the input" ?

        Since we are already iterating in the order of the input edges, and since we return the edge as soon as it
        produces the cycle, it is prerequisite that all the other edges that participate in forming the cycle have
        already come before this edge. That is why adding this edge would give us a cycle. Hence, this should be the
        last edge among the edges that participate in the cycle.

        Since there are N vertices and N edges, there can be only one cycle. All the edges from that same cycle are
        candidates for removal, but since we are iterating the input array from left to right, there is only one edge
        that "completes" the cycle. Consider this example: edges = [[1,2],[1,3],[2,3]]. All edges are part of the cycle,
        but it's [2,3] that actually "introduces" it.

        Remember that the input graph contains a unique cycle. The main goal is to find the last edge of that cycle,
        which is equivalent with finding the edge that will close that cycle. By adding edges one by one (in the order
        they appear in input) we can be sure that we will stop at the last edge in the input which forms a cycle
        (i.e., edge which destroys the tree property of the initial graph).

    Time complexity: O(N^2), where N is the number of vertices (and also the number of edges) in the graph. In the
    worst case, for every edge we include, we have to search every previously-occurring edge of the graph.
    Space complexity: O(N)
    """

    def path_exists(src, dest):
        # path_exists(src, dest) return True if dest node is reachable from src in the currently built graph.
        if src in visited:
            return False
        if src == dest:
            return True
        visited.add(src)
        for neighbor in graph[src]:
            if path_exists(neighbor, dest):
                return True
        return False

    graph = defaultdict(list)
    for src, dest in edges:
        visited = set()
        if path_exists(src, dest):
            return [src, dest]
        graph[src].append(dest)
        graph[dest].append(src)


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

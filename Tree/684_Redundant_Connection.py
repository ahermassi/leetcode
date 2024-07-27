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

                An undirected connected graph with no trivial cycles is a tree

         The statement of the problem guarantees that by deleting one and only one edge, the graph is a tree.
         So, we know it is connected and has exactly one cycle. The goal is to find the edge in this cycle with the
         largest index and return it.

         For each edge (u, v), traverse the graph using DFS to see if we can already connect u to v. If we can, then it
         must be the duplicate edge.

         We're basically doing cycle prevention (and not detection). We build the graph one edge at a time. However,
         before adding an edge between u and v, we first check if a path already exists between u and v, avoiding a
         cycle.

        How does the algorithm handle "If there are multiple answers, return the answer that occurs last in the input" ?

         Since we are already iterating in the order of the input edges, and since we return the edge as soon as it
         produces a cycle, it is a prerequisite that all the other edges that participate in forming the cycle appeared
         before this edge. That is why adding this edge would result in a cycle. Hence, this should be the last edge
         among the edges that participate in the cycle.

         Adding an edge to a tree creates only one cycle (trivial to prove). Assume that returned edge isn't the last.
         We now have a cycle. When the last edge is reached, we detect another cycle and that is contradiction.

         Since there are N vertices and N edges, there can be only one cycle. All the edges from that same cycle are
         candidates for removal, but since we are iterating the input array from left to right, there is only one edge
         that "completes" the cycle. Consider this example: edges = [[1,2],[1,3],[2,3]]. All edges are part of the cycle,
         but it's [2,3] that actually first "introduces" it. By adding edges one by one (in the order they appear in the
         input), we can be sure that we will stop at the last edge in the input which forms a cycle, i.e., the edge that
         destroys the tree property of the graph.

    Time complexity: O(N^2), where N is the number of vertices (and also the number of edges) in the graph. In the
    worst case, for every edge we include, we have to search every previously-occurring edge of the graph.
    Space complexity: O(N)
    """

    def path_exists(src, target):
        # path_exists(src, target) returns True if target node is reachable from src in the current graph
        if src == target:
            # A path was found
            return True
        visited.add(src)
        for neighbor in graph[src]:
            if neighbor not in visited and path_exists(neighbor, target):
                return True
        return False

    graph = defaultdict(list)
    for a, b in edges:
        # Perform DFS before adding the edge so that we if a cycle is detected we know this edge would cause the cycle
        visited = set()
        if path_exists(a, b):
            return [a, b]
        graph[a].append(b)
        graph[b].append(a)


def find_redundant_connection_v2(edges):
    """ In an undirected graph, like the one we're working with here, trivial "cycles" will be detected. For example,
         if there's an undirected edge between node A and node B, a detected cycle will include A → B → A. This is
         because an undirected edge is actually 2 edges in the adjacency list, and so forms a trivial cycle.

         We can keep track of the "parent" of the current node. Then, when we iterate over the neighbors of the node,
         we ignore the "parent" node as otherwise it would lead to the detection of a trivial cycle (and we know that
         the parent node has already been visited at this point anyway).

         Note that we no longer need to use a visited set because, with the introduction of parent, we're working with
         a "directed" graph, and we already know that no cycle exists yet before each call to path_exists().

    Time complexity: O(N^2)
    Space complexity: O(N)
    """

    def path_exists(src, target, parent):
        if src == target:
            return True
        for neighbor in graph[src]:
            if neighbor != parent and path_exists(neighbor, target, src):
                return True
        return False

    graph = defaultdict(list)
    for a, b in edges:
        if path_exists(a, b, 0):  # 0 is a non-existent node, so we use it as parent
            return [a, b]
        graph[a].append(b)
        graph[b].append(a)


class Test(unittest.TestCase):
    data = [([[1, 2], [1, 3], [2, 3]], [2, 3]), ([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]], [1, 4])]

    def test_find_redundant_connection(self):
        for test_edges, result in self.data:
            self.assertEqual(result, find_redundant_connection_v1(test_edges))
            self.assertEqual(result, find_redundant_connection_v2(test_edges))


if __name__ == '__main__':
    unittest.main()

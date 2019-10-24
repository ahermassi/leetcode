""" Given an undirected graph, return true if and only if it is bipartite.
Recall that a graph is bipartite if we can split it's set of nodes into two independent subsets A and B such that every
edge in the graph has one node in A and another node in B. """

from collections import deque
import unittest2 as unittest


def is_bipartite_v1(graph):
    """ Our goal is trying to use two colors to color the graph and see if there are any adjacent nodes having the
        same color. We start coloring an uncolored root node with Blue/0, and start the DFS, where if a node is colored
        Blue, all its neighbors are colored Yellow/1 and vice versa. If at any point, we find that the node we are
        about to color with Yellow is already colored with Blue (or vice versa), this essentially means that then our
        coloring is impossible. We should be able to greedily color the graph if and only if it is bipartite.
        We'll keep a hash map to lookup the color of each node.
    Time complexity: O(V + E), where V is the number of vertices in the graph, and E is the number of edges. We explore
    each node once when we transform it from uncolored to colored, traversing all its edges in the process.
    Space complexity: O(V + E), the space used to store the colors and the call stack
    """

    def dfs(vertex):
        for neighbor in graph[vertex]:
            if neighbor in color:
                if color[neighbor] == color[vertex]:  # Immediate neighbor has the same color
                    return False
            else:
                color[neighbor] = 1 - color[vertex]  # Color the neighbor with the opposite color
                if not dfs(neighbor):  # Carry on coloring neighbors if neighbor using alternate colors
                    return False
        return True

    n, color = len(graph), {}
    for vertex in range(n):
        if vertex not in color:
            color[vertex] = 0
            if not dfs(vertex):
                return False
    return True


def is_bipartite_v2(graph):
    """ Iterative version of previous DFS.
    Time complexity: O(V + E)
    Space complexity: O(E)
    """
    n, color = len(graph), {}
    for vertex in range(n):
        if vertex not in color:
            stack = [vertex]
            color[vertex] = 0
            while stack:
                node = stack.pop()
                for neighbor in graph[node]:
                    if neighbor not in color:
                        color[neighbor] = 1 - color[node]
                        stack.append(neighbor)
                    elif color[neighbor] == color[node]:
                        return False
    return True


def is_bipartite_v3(graph):
    """ BFS version using a queue. The complexities of DFS and BFS are the same since the only difference is the order
        of traversal. Both of them need to traverse every nodes and edges when the graph is bipartite.
    Time complexity: O(V + E)
    Space complexity: O(E)
    """
    n, color = len(graph), {}
    for vertex in range(n):
        if vertex not in color:
            queue = deque([vertex])
            color[vertex] = 0
            while queue:
                node = queue.pop()
                for neighbor in graph[node]:
                    if neighbor not in color:
                        color[neighbor] = 1 - color[node]
                        queue.appendleft(neighbor)
                    elif color[neighbor] == color[node]:
                        return False
    return True


class Test(unittest.TestCase):
    data = [([[1, 3], [0, 2], [1, 3], [0, 2]], True), ([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]], False)]

    def test_is_bipartite(self):
        for test_graph, result in self.data:
            self.assertEqual(result, is_bipartite_v1(test_graph))
            self.assertEqual(result, is_bipartite_v2(test_graph))
            self.assertEqual(result, is_bipartite_v3(test_graph))


if __name__ == '__main__':
    unittest.main()

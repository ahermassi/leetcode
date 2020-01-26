""" Given an undirected graph, return true if and only if it is bipartite.
Recall that a graph is bipartite if we can split it's set of nodes into two independent subsets A and B such that every
edge in the graph has one node in A and another node in B. """

from collections import deque
import unittest2 as unittest


def is_bipartite_v1(graph):
    """ Our goal is trying to use two colors to color the graph and see if there are any adjacent nodes having the
        same color. We start coloring an uncolored node with Blue/0, and start the DFS, where if a node is colored
        Blue, all its neighbors are colored Yellow/1 and vice versa. If at any point we find a neighbor colored the
        same color as the current node, then our coloring was impossible.
        We should be able to greedily color the graph if and only if it is bipartite.
        We'll keep a hash map to lookup the color of each node.
        IMPORTANT: We should be careful to consider disconnected components of the graph, by searching each node.
    Time complexity: O(V + E), where V is the number of vertices in the graph, and E is the number of edges. We explore
    each node once when we transform it from uncolored to colored, traversing all its edges in the process.
    Space complexity: O(V + E), the space used to store the colors and the call stack
    """

    def dfs(vertex, color):
        colors[vertex] = color
        for neighbor in graph[vertex]:
            if neighbor in colors and colors[neighbor] == color:  # Immediate neighbor has the same color
                return False
            if neighbor not in colors and not dfs(neighbor, 1 - color):  # Color the neighbor with the opposite color
                # and carry on coloring neighbors of neighbor using alternate colors
                return False
        return True

    n, colors = len(graph), {}
    for vertex in range(n):
        if vertex not in colors and not dfs(vertex, 0):
            return False
    return True


def is_bipartite_v2(graph):
    """ Iterative version of previous DFS using a stack.
    Time complexity: O(V + E)
    Space complexity: O(E)
    """
    n, colors = len(graph), {}
    for i in range(n):
        if i not in colors:
            stack = [(i, 0)]
            while stack:
                vertex, color = stack.pop()
                colors[vertex] = color
                for neighbor in graph[vertex]:
                    if neighbor in colors and colors[neighbor] == color:
                        return False
                    if neighbor not in colors:
                        stack.append((neighbor, 1 - color))
    return True


def is_bipartite_v3(graph):
    """ BFS version using a queue. The complexities of DFS and BFS are the same since the only difference is the order
        of traversal. Both of them need to traverse every node and edge when the graph is bipartite.
    Time complexity: O(V + E)
    Space complexity: O(E)
    """
    n, colors = len(graph), {}
    for i in range(n):
        if i not in colors:
            queue = deque([(i, 0)])
            while queue:
                vertex, color = queue.popleft()
                colors[vertex] = color
                for neighbor in graph[vertex]:
                    if neighbor in colors and colors[neighbor] == color:
                        return False
                    if neighbor not in colors:
                        queue.append((neighbor, 1 - color))
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

""" Given n nodes labeled from 0 to n-1 and a list of undirected edges (each edge is a pair of nodes), write a function
to check whether these edges make up a valid tree. """

from collections import defaultdict, deque
import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=bXsUuownnoQ


def valid_tree_v1(n, edges):
    """ According to the definition of tree on Wikipedia: 'a tree is an undirected graph in which any two vertices are
        connected by exactly one path. In other words, any CONNECTED graph without simple CYCLES is a tree.'

        Therefore, a graph G is a tree iff the following two conditions are met:

            1- G is fully connected. In other words, for every pair of nodes in G, there is a path between them.
            2- G contains no cycles. In other words, there is exactly one path between each pair of nodes in G.

        Depth-first search is a classic graph traversal algorithm that can be used to check for both of these
        conditions:

            1- G is fully connected if, and only if, we started a depth-first search from a single source and discovered
                 all nodes in G during it.
            2- G contains no cycles if, and only if, the depth-first search never goes back to an already discovered
                 node. We need to be careful though not to count trivial cycles of the form A → B → A that occur with
                 most implementations of undirected edges.


        Depth-first search requires being able to look up the adjacent (immediate neighbours) of a given node. Like
        many graph problems though, the input format we're given doesn't allow us to quickly get the neighbours of a
        node. Therefore, our first step is to convert the input into an adjacency list.

        Recall that most depth-first searches follow a template like the one below for iterative depth-first search.
        Note that this doesn't yet solve the problem of determining whether the input graph is a tree—we're simply
        using it as a step towards building up a solution.

            - Use a stack to keep track of unexplored nodes.
            - Use a set to keep track of already seen nodes to avoid infinite looping.
            - While there are nodes remaining on the stack, take one off to visit.
            - Check for unseen neighbours of this node.
            - If we've already seen this node, continue. Otherwise, put this neighbour onto the stack and record that
               it has been seen.

        Let's now figure out how we can modify the basic depth-first search template to do the two checks we need.

        The first check is straightforward. If the graph is fully connected, then every node must have been seen.
        This means that all nodes must be in the seen set at the end. Because a set removes duplicates, and the only
        values going into it were valid node numbers, then we know that the graph was fully connected if, and only if,
        the seen set contains n values at the end.

        For the second check, you might be thinking: can't we just modify the above algorithm to return false when a
        neighbour is in visited set?

        This, however, would only work on a directed graph. On an undirected graph, like the one we're working with
        here, trivial "cycles" will be detected. For example, if there's an undirected edge between node A and node B,
        a detected cycle will include A → B → A. This is because an undirected edge is actually 2 edges in the adjacency
        list, and so forms a trivial cycle.

        There are several strategies of detecting whether an undirected graph contains cycles, while excluding the
        trivial cycles. Most rely on the idea that a depth-first search should only go along each edge once, and
        therefore only in one direction. This means that when we go along an edge, we should do something to ensure
        that we don't then later go back along it in the opposite direction.

        One of the strategies is to keep track of the "parent" node that we got to a node from. Then, when we iterate
        through the neighbours of a node, we ignore the "parent" node as otherwise it'll be detected as a trivial cycle
        (and we know that the parent node has already been visited by this point anyway). The starting node (0 in this
        implementation) has no "parent", so put it as -1.

        At first, it's a little more difficult to understand why this strategy even works. A good way to think about it
        is to remember that we just want to avoid going along edges we've already been on (in the opposite direction).
        The parent links prevent that, as each node is only entered for exploration once. So, imagine you're walking
        through a maze, with the condition that you're not allowed to go back along any path you've already been on.
        If you still somehow end up somewhere you were previously, there must have been a cycle!

    Time complexity: O(|V| + |E|), creating the adjacency list requires initialising a list of length V, with a cost of
    O(V), and then iterating over and inserting E edges, for a cost of O(E). This gives us O(V) + O(N) = O(N + E).
    Each node is added to the data structure once. This means that the outer loop will run V times. For each of the V
    nodes, its adjacent edges is iterated over once. In total, this means that all E edges are iterated over once by the
    inner loop. This, therefore, gives a total time complexity of O(|V| + |E|)
    Space complexity: O(|V| + |E|), the adjacency list is a list of length V, with inner lists with lengths that add to
    a total of E. This gives a total of O(V + E) space. In the worst case, the recursion stack will have all V nodes on
    it at the same time, giving a total of O(V) space.
    """

    def dfs(vertex, parent):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor == parent:
                continue
            if neighbor in visited:
                # If a neighbor was previously visited and this neighbor is NOT my parent (the graph is undirected,
                # so A-B == A->B and B->A), then we have a cycle.
                # Example: edges = [0, 1], graph = {0: [1], 1: [0, 2]}.
                # Mark 0 as visited and proceed to its neighbors, which is only node 1. When dfs() is called with
                # (vertex=1, parent=0), we again proceed to examine the neighbors of 1: node 0 is there, but 0 is 1's
                # parent due to the undirected nature of the graph.
                return False
            # 'neighbor' has not been visited and is not the parent of current vertex, so let's check if there's
            # cycle starting from 'neighbor'
            if not dfs(neighbor, vertex):
                return False
        return True

    graph = defaultdict(list)
    for src, dest in edges:
        graph[src].append(dest)
        graph[dest].append(src)
    visited = set()
    if not dfs(0, -1):
        # Make sure there's no cycle. Note: node 0 isn't guaranteed to exist, so we can get a key error if we don't
        # use a defaultdict.
        return False
    # Check if all vertices are connected. If the graph is a tree, all nodes will be visited by the end of DFS.
    return len(visited) == n


def valid_tree_v2(n, edges):
    """ Depending on how much graph theory you know, there's a better definition for determining whether a given graph
         is a tree.

         For the graph to be a valid tree, it must have exactly n-1 edges. Any less, and it can't possibly be fully
         connected. Any more, and it has to contain cycles. Additionally, if the graph is fully connected and contains
         exactly n-1 edges, it can't possibly contain a cycle, and therefore must be a tree!

         Going by this definition, our algorithm needs to do the following:

            - Check whether there are n-1 edges. If there's not, then return false.

            - Check whether the graph is fully connected. Return true if it is, false if otherwise.

        Recall that the most complicated part of the previous approach was in checking whether the graph contained
        cycles. This was because in an undirected graph, we needed to be careful of trivial cycles. Checking whether a
        graph is fully connected is straightforward—we simply check if all nodes were reachable from a search starting
        at a single node.

        Like before, we can check for connectivity using recursive depth-first search, iterative depth-first search, or
        iterative breadth-first search. We still need to use a visited set to prevent the algorithm getting caught in an
        infinite loop if there are indeed cycles (and to prevent looping on the trivial cycles).

        In other words: In order for a graph to be a tree, it must satisfy the following condition:

                    Number of edges = Number of nodes - 1 and is connected
                (the 1st condition implies that the connected graph has no cycle)

        The DFS followed by length of visited set check allows us to verify that there is only one connected component
        in the graph.

    Time complexity: O(|V| + |E|)
    Space complexity: O(|V|)
    """

    def dfs(vertex):
        if vertex in visited:
            return
        visited.add(vertex)
        for neighbor in graph[vertex]:
            dfs(neighbor)

    if len(edges) != n - 1:
        return False
    graph = defaultdict(list)
    for src, dest in edges:
        graph[src].append(dest)
        graph[dest].append(src)
    visited = set()
    dfs(0)
    # If the graph is connected then all vertices must be visited
    return len(visited) == n


def valid_tree_v3(n, edges):
    """ BFS version of the first DFS approach.

    Time complexity: O(|V| + |E|)
    Space complexity: O(|V| + |E|)
    """
    graph = defaultdict(list)
    for src, dest in edges:
        graph[src].append(dest)
        graph[dest].append(src)
    visited = set()
    queue = deque([(0, -1)])
    while queue:
        vertex, parent = queue.popleft()
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor == parent:
                continue
            if neighbor in visited:
                return False
            queue.append((neighbor, vertex))
    return len(visited) == n


class Test(unittest.TestCase):
    data = [(5, [[0, 1], [0, 2], [0, 3], [1, 4]], True), (5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]], False)]

    def test_valid_tree(self):
        for test_n, test_edges, result in self.data:
            self.assertEqual(result, valid_tree_v1(test_n, test_edges))
            self.assertEqual(result, valid_tree_v2(test_n, test_edges))
            self.assertEqual(result, valid_tree_v3(test_n, test_edges))


if __name__ == '__main__':
    unittest.main()

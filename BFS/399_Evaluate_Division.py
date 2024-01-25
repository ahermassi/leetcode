""" Equations are given in the format A / B = k, where A and B are variables represented as strings, and k is a real
number (floating point number). Given some queries, return the answers. If the answer does not exist, return -1.0. """

from collections import deque, defaultdict
import unittest2 as unittest


def calc_equation_v1(equations, values, queries):
    """ Let's look at the example given in the problem description. Given two equations, namely a/b=2, b/c=3, we could
         derive the following equations:

            1) b/a=1/2, c/b=1/3
            2) a/c=a/b * b/c=2 * 3=6

        Each division implies the reverse of the division, which is how we derive the equations in (1). While by
        chaining up equations, we could obtain new equations in (2).

        We could reformulate the equations with the graph data structure, where each variable can be represented as a
        node in the graph, and the division relationship between variables can be modeled as an edge with direction and
        weight.

        The direction of the edge indicates the order of division, and the weight indicates the result of division.

        To evaluate a query (e.g. a/c=?) is equivalent to performing two tasks on the graph:

            - Find if there exists a path between the two entities
            - If so, calculate the cumulative products along the paths

        As we can see, we just transform the problem into a path searching problem in a graph. More precisely, we can
        reinterpret the problem as:

                Given two nodes, we are asked to check if there exists a path between them. If so, we should return
                the cumulative products along the path as the result.

         Visualize a/b = k as a link between nodes a and b, the weight from a to b is k, the reverse link is 1/k. Query
         is to find a path between the two nodes.

        Given the above problem statement, it seems intuitive that we could apply DFS. Essentially, we can break down
        the algorithm into two steps overall:

            - Build the graph out of the list of input equations. Each equation corresponds to two edges in the graph.

            - Once the graph is built, we then can evaluate the queries one by one.

                * The evaluation of a query is done via searching the path between the given two variables.
                * Other than the above searching operation, we need to handle two exceptional cases as follows:
                   Case 1): if either of the nodes does not exist in the graph, i.e. the variables did not appear in any
                   of the input equations, then we can assert that no path exists.
                   Case 2): if the origin and the destination are the same node, i.e. a/a, we can assume that there
                   exists an invisible self-loop path for each node and the result is 1.

    Time complexity: O(N * M), where N is the number of input equations and M be the number of queries. We iterate
    through the equations to build a graph. Each equation takes O(1) time to process. Therefore, this step will take
    O(N) time in total. For each query, we need to traverse the graph. In the worst case, we might need to traverse the
    entire graph, which could take O(N). Hence, in total, the evaluation of queries could take M * O(N)=O(N * M).
    Space complexity: O(N), we build a graph out of the equations; in the worst case where there is no overlapping among
    the equations, we would have N edges and 2N nodes in the graph. Therefore, the space complexity of the graph is
    O(N+2N)=O(3N)=O(N). Since we use recursion, we would consume additional memory in the function call stack, which
    could amount to O(N). In addition, we use a set visited to keep track of the nodes we visited during DFS. The space
    complexity of the visited set would be O(N).
    """

    def dfs(origin, destination, running_prod):
        if origin not in divisions or destination not in divisions or origin in visited:
            return -1
        if origin == destination:
            return running_prod
        visited.add(origin)
        for neighbor, val in divisions[origin]:
            result = dfs(neighbor, destination, running_prod * val)
            if result != -1:
                return result
        return -1

    divisions = defaultdict(list)
    for numbers, result in zip(equations, values):
        x, y = numbers
        divisions[x].append((y, result))
        divisions[y].append((x, 1 / result))
    res = []
    for x, y in queries:
        visited = set()
        res.append(dfs(x, y, 1))
    return res


def calc_equation_v2(equations, values, queries):
    """ Binary relationship is usually represented as a graph.
        Does the direction of an edge matter? Yes. Take a / b = 2 for example, it indicates a --2--> b as well
        as b --1/2--> a. Thus, it is a directed weighted graph.
        In this graph, how do we evaluate division?
        Take a / b = 2, b / c = 3, a / c = ? for example:
        a --2--> b --3--> c
        Visualize a/b = k as a link between node a and b, the weight from a to b is k, the reverse link is 1/k. Query
        is to find a path between two nodes.
        We simply find a path using BFS from node 'a' to node 'c' and multiply the weights of edges, node.e. 2 * 3 = 6.
    Time complexity: O(V ** 3), where V is the number of vertices
    Space complexity: O(V)
    """

    def bfs(src, dest):
        if src not in graph or dest not in graph:  # If either source or destination node is not in the graph, the
            # answer doesn't exist
            return -1
        if src == dest:
            return 1
        queue, visited = deque([(src, 1.0)]), set()  # A separate 'visited' set for each query
        while queue:
            node, cur_prod = queue.popleft()
            if node == dest:
                return cur_prod
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, cur_prod * graph[node][neighbor]))
        return -1

    graph = defaultdict(dict)
    for (src, dest), coef in zip(equations, values):
        graph[src][dest] = coef
        graph[dest][src] = 1 / coef
    res = [bfs(src, dest) for src, dest in queries]
    return res


class Test(unittest.TestCase):
    data = [([['a', 'b'], ['b', 'c']], [2.0, 3.0], [['a', 'c'], ['b', 'a'], ['a', 'e'], ['a', 'a'], ['x', 'x']],
             [6.0, 0.5, -1.0, 1.0, -1.0])]

    def test_calc_equation(self):
        for test_equations, test_values, test_queries, result in self.data:
            self.assertEqual(result, calc_equation_v1(test_equations, test_values, test_queries))
            self.assertEqual(result, calc_equation_v2(test_equations, test_values, test_queries))


if __name__ == '__main__':
    unittest.main()

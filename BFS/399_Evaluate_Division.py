""" Equations are given in the format A / B = k, where A and B are variables represented as strings, and k is a real
number (floating point number). Given some queries, return the answers. If the answer does not exist, return -1.0. """
from collections import deque, defaultdict

import unittest2 as unittest


def calc_equation_v1(equations, values, queries):
    """ Binary relationship is usually represented as a graph.
        Does the direction of an edge matters? -- Yes. Take a / b = 2 for example, it indicates a --2--> b as well
        as b --1/2--> a. Thus, it is a directed weighted graph.
        In this graph, how do we evaluate division?
        Take a / b = 2, b / c = 3, a / c = ? for example:
        a --2--> b --3--> c
        We simply find a path using BFS from node a to node c and multiply the weights of edges passed, i.e. 2 * 3 = 6.
    Time complexity: O(V ** 3), where V is the number of vertices
    Space complexity: O(V)
    """

    def bfs(num, denom):
        if num not in graph or denom not in graph:  # If either num or denom is not in graph, or num and denom are not
            # connected in graph, the answer doesn't exist
            return -1.0
        if num == denom:
            return 1.0
        queue, visited = deque([(num, 1.0)]), set()
        while queue:
            i, current_product = queue.popleft()
            if i == denom:
                return current_product
            visited.add(i)
            for neighbor, coef in graph[i]:
                if neighbor not in visited:
                    queue.append((neighbor, current_product * coef))
        return -1.0

    graph = defaultdict(list)
    for (num, denom), coef in zip(equations, values):
        graph[num].append((denom, coef))
        graph[denom].append((num, 1 / coef))
    res = [bfs(x, y) for x, y in queries]
    return res


class Test(unittest.TestCase):
    data = [([['a', 'b'], ['b', 'c']], [2.0, 3.0], [['a', 'c'], ['b', 'a'], ['a', 'e'], ['a', 'a'], ['x', 'x']],
             [6.0, 0.5, -1.0, 1.0, -1.0])]

    def test_calc_equation(self):
        for test_equations, test_values, test_queries, result in self.data:
            self.assertEqual(result, calc_equation_v1(test_equations, test_values, test_queries))


if __name__ == '__main__':
    unittest.main()

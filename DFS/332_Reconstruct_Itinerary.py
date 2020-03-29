""" Read description on Leetcode """

from collections import defaultdict
from heapq import heappush, heappop
import unittest2 as unittest


def find_itinerary_v1(tickets):
    """ All the airports are vertices and tickets are directed edges. Then all these tickets form a directed graph.
        The graph must be Hamiltonian (visit each vertex once and only once) since we know that a Hamiltonian path
        exists.
        Since the problem asks for lexical order smallest solution, we can put the neighbors in a min-heap. This way we
        always visit the smallest possible neighbor first in our trip.
        Start with JFK as starting airport and keep adding the next child to traverse for the last airport at the top
        of the stack. If we reach an airport from where we can't go further (dead end), we add it to the result. This
        airport should be the last to go since we can't go anywhere from here. That's why we return the reverse of the
        result list. After this, backtrack to the top airport in the stack and continue to traverse its children.
        To summarize, the main idea to find the path consists of two steps:
            1- Starting from any vertex, we keep following the unused edges until we get stuck at certain vertex where
               we have no more unvisited outgoing edges.
            2- We then backtrack to the nearest neighbor vertex in the current path that has unused edges and we repeat
               the process until all the edges have been used.
        The first vertex that we got stuck at would be the end point of our path. So if we follow all the stuck points
        backwards, we could reconstruct the path at the end.
        The essential step is that starting from the fixed starting vertex (JFK airport), we keep following the ordered
        and unused edges (flights) until we get stuck at certain vertex where we have no more unvisited outgoing edges.
        The point that we got stuck would be the last airport that we visit.
        In the resulted path, before we visit the last airport (denoted as V), we can say that we have already used all
        the rest flights, i.e. if there is any flight starting from V, then we must have already taken that before.
        Or to put it another way, before adding the last airport (vertex) in the final path, we have visited all its
        outgoing vertices.
        Actually, the above statement applies to each airport in the final itinerary. Before adding an airport into the
        final itinerary, we must first visit all its outgoing neighbor vertices.
        If we consider the outgoing vertices in a directed graph as children nodes in a tree, we could see the reason
        why we could consider the algorithm as a sort of post-order DFS traversal of a tree.
    Time complexity: O(N logN), where N is the number of tickets
    Space complexity: O(N)
    """
    graph = defaultdict(list)
    for origin, dest in tickets:
        heappush(graph[origin], dest)
    stack, res = ['JFK'], []
    while stack:
        arrivals = graph[stack[-1]]
        if arrivals:
            stack.append(heappop(arrivals))  # While we visit the edge, we trim it off from the graph
        else:
            res.append(stack.pop())
    return res[::-1]


def find_itinerary_v2(tickets):
    """ Recursive version of above algorithm.
        First keep going forward until you get stuck. That's a good main path already. Remaining tickets form cycles
        which are found on the way back and get merged into that main path.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """

    def travel(airport):
        arrivals = d[airport]
        while arrivals:
            travel(heappop(arrivals))
        res.append(airport)

    d = defaultdict(list)
    for origin, dest in tickets:
        heappush(d[origin], dest)
    res = []
    travel('JFK')
    return res[::-1]


class Test(unittest.TestCase):
    data = [([['MUC', 'LHR'], ['JFK', 'MUC'], ['SFO', 'SJC'], ['LHR', 'SFO']], ['JFK', 'MUC', 'LHR', 'SFO', 'SJC']),
            ([['JFK', 'SFO'], ['JFK', 'ATL'], ['SFO', 'ATL'], ['ATL', 'JFK'], ['ATL', 'SFO']],
             ['JFK', 'ATL', 'JFK', 'SFO', 'ATL',
              'SFO'])]

    def test_find_itinerary(self):
        for test_tickets, result in self.data:
            self.assertEqual(result, find_itinerary_v1(test_tickets))


if __name__ == '__main__':
    unittest.main()

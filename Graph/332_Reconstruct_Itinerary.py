""" Read description on Leetcode """

from collections import defaultdict
from heapq import heappush, heappop
import unittest2 as unittest


# Great explanation: https://www.youtube.com/watch?v=8MpoO2zA2l4

def find_itinerary_v1(tickets):
    """ Hierholzer’s Algorithm.

        In graph theory, an Eulerian trail (or Eulerian path) is a trail in a finite graph that visits every edge
        exactly once (allowing for revisiting vertices). In our problem, we are asked to construct an itinerary that
        uses all the flights (edges), starting from the airport of 'JFK'. As we can see, the problem is actually a
        variant of Eulerian path, with a fixed starting point.

        All the airports are vertices and tickets are directed edges. Then all these tickets form a directed graph.
        Since the problem asks for the lexically smallest solution, we can put the neighbors in a min-heap. This way, we
        always visit the smallest possible neighbor first in our trip.

        At each airport, given a list of possible destinations, at each step we would pick the destination greedily in
        lexical order, i.e. the one with the smallest lexical order would have its trial first. With this greedy
        strategy, we would ensure that the final solution that we find would have the smallest lexical order.

        The main idea to find the path consists of two steps:

            1- Starting from any vertex, we keep following the unused edges until we get stuck at a certain vertex where
                 we have no more unvisited outgoing edges.

            2- We then backtrack to the nearest neighbor vertex in the current path that has unused edges, and we repeat
                 the process until all the edges have been used.

        The first vertex that we get stuck at would be the end point of our path. So if we follow all the stuck points
        backwards, we could reconstruct the path at the end.

        Start with JFK as starting airport and keep adding the next child to traverse for the last airport at the top
        of the stack. If we reach an airport from where we can't go further (dead end), we add it to the result. This
        airport should be the last to go since we can't go anywhere from there. That's why we return the reverse of the
        result list. After this, backtrack to the top airport in the stack and continue to traverse its children.

        The essential step is that starting from the fixed starting vertex (JFK airport), we keep following the ordered
        and UNUSED edges (flights) until we get stuck at a certain vertex where we have no more unvisited outgoing
        edges. The point we get stuck at would be the LAST airport we visit.

        In the result path, before we visit the last airport (denoted as V), we can say that we have already used all
        the rest flights, i.e. if there is any flight starting from V, then we must have already taken that before.
        Or to put it another way, before adding the last airport (vertex) in the final path, we have visited all its
        outgoing vertices. Actually, this statement applies to each airport in the final itinerary. Before adding an
        airport into the final itinerary, we must first visit ALL its outgoing neighbor vertices.

        If we consider the outgoing vertices in a directed graph as children nodes in a tree, we could see the reason
        why we could consider the algorithm as a sort of postorder DFS traversal of a tree.

        The path we are going to find is an itinerary which 1- uses all tickets to travel among airports,
        and 2 - preferably in ascending lexical order of airport code. Keep in mind that requirement 1 must be satisfied
        before we consider 2. If we always choose the airport with the smallest lexical order, this would lead to a
        perfectly lexically ordered itinerary, but pay attention that when doing so, there can be a "dead end" somewhere
        in the tickets such that we are not ableto  visit all airports (or we can't use all our tickets), which is bad
        because it fails to satisfy requirement 1. Thus, we need to take a step back and try other possible airports,
        which might not give us a perfectly ordered solution, but will use all tickets and cover all airports.

        Example:
        graph = {'JFK': ['A', 'D'], 'A': ['C'], 'B': ['C'], 'C': ['D', 'JFK'], 'D': ['A', 'B']}
        route = []
        call stack = ['JFK']

        First point at which we get stuck:
        graph = {'JFK': ['D'], 'A': [], 'B': ['C'], 'C': ['JFK'], 'D': ['B']}
        route = []
        call stack = ['JFK', 'A', 'C', 'D', 'A']

        Update route:
        graph = {'JFK': ['D'], 'A': [], 'B': ['C'], 'C': ['JFK'], 'D': ['B']}
        route = ['A']
        call stack = ['JFK', 'A', 'C', 'D']

        Search forward again until stuck:
        graph = {'JFK': [], 'A': [], 'B': [], 'C': [], 'D': []}
        route = ['A']
        call stack = ['JFK', 'A', 'C', 'D', 'B', 'C', 'JFK', 'D']

        Update route:
        graph = {'JFK': [], 'A': [], 'B': [], 'C': [], 'D': []}
        route = ['A', 'D', 'JFK', 'C', 'B', 'D', 'C', 'A', 'JFK']
        call stack = []

        Return route in reverse:
        route = ['JFK', 'A', 'C', 'D', 'B', 'C', 'JFK', 'D', 'A']

        Example: tickets = [['JFK','A'], ['JFK','D'], ['A','C'], ['D','A'], ['D','B'], ['B', 'C'], ['C', 'D'], ['C', 'JFK']]

        From JFK we first visit JFK -> A -> C -> D -> A. There we're stuck, so we write down A as the end of the route
        and retreat back to D. There we see the unused ticket to B and follow it: D -> B -> C -> JFK -> D. Then we're
        stuck again, retreat and write down the airports while doing so: Write down D before the already written A, then
        JFK before the D, etc. When we're back from our cycle at D, the written route is D -> B -> C -> JFK -> D -> A.
        Then we retreat further along the original path, prepending C, A and finally JFK to the route, ending up with
        the route JFK -> A -> C -> D -> B -> C -> JFK -> D -> A.

    Time complexity: O(E logE), where E is the number of tickets/edges. During DFS, we would traverse each edge once.
    Therefore, the complexity of the DFS function would be O(|E|). However, before the DFS, we need to sort the
    outgoing edges for each vertex, and this dominates the overall complexity.
    Space complexity: O(|E| + |V|), where ∣E∣ is the number of flights and ∣V∣ is the number of airports. We construct
    the graph, which would require the space of O(|E| + |V|). We also incur additional memory consumption in the
    function call stack. The maximum depth of the recursion would be exactly the number of flights in the input,
    i.e. |E|.
    """

    def dfs(airport):
        destinations = graph[airport]
        while destinations:
            dfs(heappop(destinations))
        res.append(airport)
        # Note how the first airport to be added to the path is the one with no departing flights (empty
        # 'destinations' heap), but in reality this airport should be the last to visit. This is why we return a
        # reversed list

    graph = defaultdict(list)
    for src, dest in tickets:
        heappush(graph[src], dest)
    res = []
    dfs('JFK')
    return res[::-1]


def find_itinerary_v2(tickets):
    """ Iterative version of the above algorithm using an explicit stack.
        Considering the passenger has to be physically in one place before moving to another airport, we are
        considering using up all tickets and choose lexicographically smaller solution if case of a tie. Thinking as
        that passenger, they choose their flight greedily as the lexicographical order. Once they arrive at an airport
        without departure flights with more tickets at hand, the passenger will push current ticket in a stack and look
        at whether it is possible to travel to other places from the airport on their way.
    Time complexity: O(E logE)
    Space complexity: O(|E| + |V|)
    """

    graph = defaultdict(list)
    for origin, dest in tickets:
        heappush(graph[origin], dest)
    stack, res = ['JFK'], []
    while stack:
        destinations = graph[stack[-1]]
        if destinations:
            stack.append(heappop(destinations))  # While we visit the edge, we trim it off from the graph
        else:
            res.append(stack.pop())
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

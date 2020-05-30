""" There are n cities connected by m flights. Each fight starts from city u and arrives at v with a price w.
Now given all the cities and flights, together with starting city src and the destination dst, your task is to find the
cheapest price from src to dst with up to k stops. If there is no such route, output -1. """

from collections import defaultdict
from heapq import heappop, heappush
import unittest2 as unittest


def find_cheapest_price(flights, src, dst, K):
    """ Dijkstra's algorithm using priority queue.
        The key difference with the classic Dijkstra's algorithm is that we don't maintain the global optimal distance
        to each node, i.e. ignore below optimization:
            distance ← dist[u] + length(u, v)
            if distance < dist[v]: ...
        Because there could be routes whose length is shorter but pass more stops, and those routes don't necessarily
        constitute the best route in the end. To deal with this, rather than maintain the optimal routes with 0..K
        stops for each node, the solution simply puts all possible routes into the priority queue, so that all of them
        has a chance to be processed. It returns the first qualified route, and it's easy to prove this must be the
        best route. The reason for this is that Dijkstra's (and this modified Dijkstra's) always selects greedily, as
        in it always picks the node with the lowest cost off the top of the priority queue. This means when we pop the
        'dst' node off the heap, we have the lowest cost to that node since we always pick the lowest place to go, and
        obviously the distance from original source to current node (which is 'dst') is less than K. If we still have
        stops left (stops > 0), we put its neighbor into the priority queue, so each city in the priority queue must be
        within the stops limit.
        This question is a little different from the Dijkstra's problem in the sense that there's a trade-off between
        lower price and fewer stops.
        Heap entries take the form of (cost, node, stops). 'cost' is the accumulated cost, 'node' is the current node's
        location, 'stops' is stop times left as we only have at most K stops.
    Time complexity: O(E + N logN), E is the number of edges and N is number of nodes
    Space complexity: O(N), graph and heap store at most N number of entries
    """
    graph = defaultdict(list)
    for source, destination, cost in flights:
        graph[source].append((destination, cost))
    heap = [(0, src, K + 1)]
    while heap:
        total_cost, node, stops = heappop(heap)
        if node == dst:
            return total_cost
        if stops:
            for neighbor, cost in graph[node]:
                heappush(heap, (total_cost + cost, neighbor, stops - 1))
    return -1


class Test(unittest.TestCase):
    data = [([[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1, 200),
            ([[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0, 500)]

    def test_find_cheapest_price(self):
        for test_flights, test_src, test_dst, test_k, result in self.data:
            self.assertEqual(result, find_cheapest_price(test_flights, test_src, test_dst, test_k))


if __name__ == '__main__':
    unittest.main()

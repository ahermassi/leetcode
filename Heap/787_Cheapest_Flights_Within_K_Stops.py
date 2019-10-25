""" There are n cities connected by m flights. Each fight starts from city u and arrives at v with a price w.
Now given all the cities and flights, together with starting city src and the destination dst, your task is to find the
cheapest price from src to dst with up to k stops. If there is no such route, output -1. """

from collections import defaultdict
from heapq import heappop, heappush
import unittest2 as unittest


def find_cheapest_price(flights, src, dst, K):
    """ Dijkstra's algorithm using priority queue (heap).
        Here, 'K' limited the time we can visit a single node that it won't go into an infinite loop.
        Heap entries take the form of (cost, node, stops). 'cost' is the accumulated cost, 'node' is the current node's
        location, 'stops' is stop times left as we only have at most K stops.
        Once 'stops' is used up (stops == 0), we no longer push that node to our queue. Once a popped node is our
        destination, we get our lowest valid cost.
        For Dijkstra, there is no need to maintain a best cost for each node since it's kind of greedy search. It
        always chooses the lowest cost node for next search. So the previous searched node always has a lower cost and
        has no chance to be updated. The first time we pop our destination from our queue, we have found the lowest
        cost to our destination.
    Time complexity: O(E + NlogN), E is the number of edges and N is number of nodes
    Space complexity: O(N), graph and heap store at most N number of entries
    """
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))
    heap = [(0, src, K + 1)]
    while heap:
        cost, node, stops = heappop(heap)
        if node == dst:
            return cost
        if stops:
            for v, w in graph[node]:
                heappush(heap, (cost + w, v, stops - 1))
    return -1


class Test(unittest.TestCase):
    data = [([[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1, 200),
            ([[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0, 500)]

    def test_find_cheapest_price(self):
        for test_flights, test_src, test_dst, test_k, result in self.data:
            self.assertEqual(result, find_cheapest_price(test_flights, test_src, test_dst, test_k))


if __name__ == '__main__':
    unittest.main()

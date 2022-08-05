""" There are n cities connected by m flights. Each fight starts from city u and arrives at v with a price w.
Now given all the cities and flights, together with starting city src and the destination dst, your task is to find the
cheapest price from src to dst with up to k stops. If there is no such route, output -1. """

from collections import defaultdict
from heapq import heappop, heappush
import unittest2 as unittest


def find_cheapest_price(flights, src, dst, k):
    """ Dijkstra's algorithm using priority queue.

        If we forget about the part where the number of stops is limited, then the problem simply becomes the shortest
        path problem on a weighted graph. We can treat this as a graph problem where:

            - The cities can be treated as nodes in a graph
            - The connections between each of the cities can be treated as the edges
            - The cost of going from one city to another would be the weight of the edges in the graph.

        It's important to model the problem in a way that standard algorithms or their slight variations can be used f
        or the solutions.

        Whenever we have a problem where we're given a bunch of entities, and they have some sort of connections between
        them, more often than not it can be modeled as a graph problem. Once we've figured out that the question can be
        modeled as a graph problem, we then need to think about the various aspects of a graph i.e.
        directed vs undirected, weighted vs unweighted, cyclic vs acyclic. These aspects will help define the algorithm
        that we can consider for solving the problem at hand.

        For example, a standard rule of thumb that is followed for solving the shortest path problems is that we mostly
        use breadth-first search for unweighted graphs and use Dijkstra's algorithm for weighted graphs. An implied
        condition to apply Dijkstra's algorithm is that the weights of the graph must be positive. If the graph has
        negative weights and can have negative weighted cycles, we would have to employ another algorithm called
        Bellman Ford. The point here is that the properties of the graph and the goal define the kind of algorithms
        we might be able to use.

        If we don't consider the part where the number of stops is limited, this problem becomes a standard shortest
        path problem in a weighted graph with positive weights and hence, it becomes a prime candidate for Dijkstra's.
        As we all know, Dijkstra's uses a min-heap (priority queue) as the main data structure for always picking out
        the node which can be reached in the shortest amount of time/cost/weight from the current point starting all
        the way from the source. That approach as it is won't work out for this problem.

        First, we need to keep track of the number of stops taken to reach a node (city), in addition to the shortest
        path from the source node. This is important because if at any point we find that we have exhausted k stops, we
        can't progress any further from that node because the number of stops is limited.

        According to Dijkstra's algorithm (without modification), once a node has been processed i.e., once a node is
        popped from the min-heap, we never consider that node again in some other node's neighbors i.e., we never add
        it again to the heap down the line. This is because of the greedy nature of the algorithm. When a node is
        removed from the heap, it is guaranteed that the distance from the source at that point is the shortest.

        The thing we need to modify here is that we need to reconsider a node if the distance from the source is shorter
        than what we have recorded. So we won't change the min-heap's priority which is to pick nodes with the shortest
        distance from the source. However, if we ever encounter a node that has already been processed before but the
        number of stops from the source is less than what was recorded before, we will add it to the heap so that it
        gets considered again. That's the only change we need to make Dijkstra's compliant with the limitation on the
        number of stops.

            - Initialize a min-heap or a priority queue. Let's call it 'heap' for this algorithm.

            - Next, we need to convert the input into an adjacency list format. So, we will process the given input and
               build an adjacency list out of it.

            - Add (0, source, k+1) into the heap. The first value represents the current shortest distance/lowest cost
               from the source and the last value represents the number of stops left that we can make from this node.

            - We continue processing the nodes until either of the following conditions is met:
                    * We reach the destination node
                    * We exhaust the heap which would mean we were not able to reach the destination at all

            - At each step, we remove a node from the heap. This would represent the node with the shortest distance/lowest
               cost from the source amongst the ones in the heap.

            - We check if number of stops left is greater than the number of stops for the current node. If that is not
               the case, then it means the currently considered path from the source to the node is slightly expensive
               than a previous path and has more stops and hence, it should not be considered.

            - Otherwise, we iterate over all the current node's neighbors which we can obtain from the adjacency list.
               For each neighbor, we push it into the heap with updated distance and number of stops

        The key difference with the classic Dijkstra's algorithm is that we don't maintain the global optimal distance
        to each node, i.e. ignore below optimization:

            distance ← dist[u] + length(u, v)
            if distance < dist[v]: ...

        Because there could be routes whose lengths are shorter but pass more stops, and those routes don't necessarily
        constitute the best route in the end. To deal with this, rather than maintaining the optimal routes with 0...K
        stops for each node, the solution simply puts all possible routes into the priority queue, so that all of them
        have a chance of being processed. The solution simply returns the first qualified route.

        The reason for this is that Dijkstra's (and this modified Dijkstra's) always selects greedily, as in it always
        picks the node with the lowest cost off the top of the priority queue. This means when we pop the 'dst' node
        off the heap, we have the lowest cost to that node since we always pick the lowest place to go, and obviously
        the route from original source to current node (which is 'dst') used at most k stops.

        This question is a little different from the Dijkstra's problem in the sense that there's a trade-off between
        lower price and fewer stops. Heap entries take the form of (cost, node, stops_left). 'cost' is the accumulated
        cost, 'node' is the current node's location, and 'stops_left' is stop times left as we can only make at most
        k stops.

    Time complexity: O(E + N logN), where E is the number of edges and N is number of nodes. The time complexity is
    mainly dominated by the number of times we pop and push into the heap. We will process each node (city) at least
    once, and for each city popped from the queue, we iterate over its adjacency list and can potentially add all its
    neighbors to the heap.
    Space complexity: O(N), graph and heap store at most N entries
    """
    n = len(flights)
    graph = defaultdict(list)
    for source, destination, cost in flights:
        graph[source].append((destination, cost))
    heap = [(0, src, k + 1)]  # There are k stops allowed, which means we can move k+1 times
    visited = [0] * n  # Track the number of moves it takes to reach a node
    while heap:
        total_cost, node, stops_left = heappop(heap)
        if node == dst:
            return total_cost
        if visited[node] >= stops_left:
            # The current path took more moves to reach the node than some previous paths. Unlike Dijkstra which
            # updates only if the distance is shorter, a node should be updated here if (i) distance is shorter (ii)
            # fewer number of moves If current remaining stops is less than a previous remaining stops visited[node],
            # there is no need to visit this node as it has higher cost but fewer remaining sops. Therefore,
            # no way it could be better than before.
            continue
        visited[node] = stops_left
        for neighbor, cost in graph[node]:
            heappush(heap, (total_cost + cost, neighbor, stops_left - 1))
    return -1


class Test(unittest.TestCase):
    data = [([[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1, 200),
            ([[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0, 500)]

    def test_find_cheapest_price(self):
        for test_flights, test_src, test_dst, test_k, result in self.data:
            self.assertEqual(result, find_cheapest_price(test_flights, test_src, test_dst, test_k))


if __name__ == '__main__':
    unittest.main()

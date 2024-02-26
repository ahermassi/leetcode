""" There are n cities connected by m flights. Each fight starts from city u and arrives at v with a price w.
Now given all the cities and flights, together with starting city src and the destination dst, your task is to find the
cheapest price from src to dst with up to k stops. If there is no such route, output -1. """

from collections import defaultdict, deque
from heapq import heappop, heappush
import unittest2 as unittest


def find_cheapest_price_v1(flights, src, dst, k):
    """ We can treat this as a graph problem where:

         - Cities can be thought of as nodes in a graph
         - The connections between each of the cities can be treated as the edges
         - The cost of going from one city to another would be the weight of the edges in the graph.

        The problem is to find the shortest path from a source to a destination with a constraint of k stops.

        Breadth-first search is a good algorithm to use if we want to find the shortest path in an unweighted graph.
        The property of BFS is that the first time a node is reached during the traversal, it is reached at the minimum
        distance from the source.

        The same cannot be said for a weighted graph. For a weighted graph, a path having more edges does not
        necessarily mean the path is more expensive. Thus, we cannot employ a normal breadth-first search for weighted
        graphs.

        A breadth-first search has no way of knowing if the discovery of a particular node would give us the cheapest
        path to that node. The only possible way for BFS (or DFS) to find the shortest path in a weighted graph is to
        search the entire graph and keep recording the minimum distance from the source to the destination node.

        However, this problem limits the number of stops to k. As a result, we need not search the paths with lengths
        greater than (k + 1). A breadth-first search can be used for this problem because the number of levels to be
        explored by the algorithm is bounded by k.

        In this approach, we perform a level-order iteration over the nodes. We explore all the nodes at the current
        level before moving on to the nodes at the next level. The current level would correspond to the number of stops
        that is limited by k. When we move from one level to the next, we increase the stops by 1. We are allowed a
        maximum of k stops, which means we could go up to a maximum of (k + 1) levels from the source node, trying to
        reach the destination at the minimum price.

        We can maintain a costs array which stores the minimum price to reach each node. When we want to move to a node,
        we only consider edges where the total price after traversing the edge is less than the currently calculated
        costs[node]. This optimization helps avoid TLE.

            - Create an adjacency list where graph[a] contains all the neighbors of node a and the corresponding price
               it takes to move to a neighbor.

            - Initialize costs array, storing the minimum price to reach a node from the source node. Initialize it with
               large values.

            - Initialize a queue storing {node, total cost} pairs. Initially, the queue should have only (src, 0).

            - Perform BFS until the queue is empty or k >= 0 (alternatively, we can create a variable to keep track of
               the number of BFS "layers" if we don't want to modify the input parameter k):

                    * Iterate over all the nodes at a particular level. This will be done by starting a nested loop and
                       visiting all the nodes currently present in the queue.

                    * At each pair {node, total cost}, iterate over all the neighbors of the node. For each neighbor,
                       check if costs[neighbor] is greater than total cost + the price of the edge. If it is, then
                       update cost[neighbor] and push (neighbor, costs[neighbor]) to the queue.

                    * After iterating over all the nodes at the current level, decrement k. We visited all the nodes at
                    the current level and are ready to visit the next level of nodes.

            - Once we reach a condition where either the queue is empty or k < 0, we have our answer as costs[dst].
            If costs[dst] hasn't changed from the initial large value, then we never reached it, so return -1.

    Time complexity: O(V + E*k), where E is the number of flights and V is the number of cities. Depending on
    improvements in the shortest distance for each node, we may process each edge multiple times. However, the maximum
    number of times an edge can be processed is limited to k because that is the number of levels the BFS runs. In the
    worst case, this takes O(E*k) time. We also need O(E) to initialize the adjacency list and O(V) to initialize the
    costs array.
    Space complexity: O(V + E*k), we process at most E*k edges, so the queue takes up O(E*k) space in the worst case. We
    also need O(E) space for the adjacency list and O(V) space for the costs array.
    """
    n = len(flights)
    graph = defaultdict(list)
    for source, destination, cost in flights:
        graph[source].append((destination, cost))
    costs = [float('inf')] * n
    costs[src] = 0
    queue = deque([(src, 0)])
    while queue and k >= 0:
        size = len(queue)
        for _ in range(size):
            node, total_cost = queue.popleft()
            for neighbor, cost in graph[node]:
                if costs[neighbor] > total_cost + cost:
                    costs[neighbor] = total_cost + cost
                    queue.append((neighbor, costs[neighbor]))
        k -= 1
    return costs[dst] if costs[dst] != float('inf') else -1


def find_cheapest_price_v2(flights, src, dst, k):
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

# Video explanation: https://www.youtube.com/watch?v=5eIK3zUdYmE


def find_cheapest_price_v3(flights, src, dst, k):
    """ Bellman-Ford

         Like Dijkstra's algorithm, Bellman-Ford proceeds by relaxation, in which approximations to the correct distance
         are replaced by better ones until they eventually reach the solution. In both algorithms, the approximate
         distance to each vertex is always an overestimate of the true distance and is replaced by the minimum of its
         old value and the length of a newly found path.

         However, Dijkstra's algorithm uses a priority queue to greedily select the closest vertex that has not yet been
         processed, and performs this relaxation process on all of its outgoing edges; by contrast, the Bellman-Ford
         algorithm simply relaxes all the edges and does this∣V∣−1 times, where ∣V∣ is the number of vertices in the
         graph. In each of these repetitions, the number of vertices with correctly calculated distances grows, from
         which it follows that eventually, all vertices will have their correct distances. This method allows the
         Bellman-Ford algorithm to be applied to a wider class of inputs than Dijkstra.

         The term "relax an edge" simply means that for a given edge U -> V we check if dU+Weight(U,V) <dV, where dU and
         dV represent the shortest path distances of these nodes from the source right now. To relax an edge means to
         see if the shortest distance can be updated or not.

         An important part to understanding the Bellman Ford's working is that at each step, the relaxations lead to the
         discovery of new shortest paths to nodes. After the first iteration over all the vertices, the algorithm finds
         out all the shortest paths from the source to nodes which can be reached with one hop (one edge). That makes
         sense because the only edges we'll be able to relax are the ones that are directly connected to the source as
         all the other nodes have their shortest distances set to infinity initially.

        Similarly, after the (K+1)th step, Bellman-Ford will find the shortest distances for all the nodes that can be
        reached from the source using a maximum of K stops. Isn't that what the question asks us to do? If we run
        Bellman-Ford for K+1 iterations, it will find out the shortest paths of length K or less, and it will find all
        such paths. We can then check if our destination node was reached or not and if it was, then the value for that
        node would be our shortest path.

        Another important thing to note about this algorithm is that we don't need to build an adjacency list.
        The algorithm simply iterates over the edges of the graph and that information is already available in the
        input.

            - We have a loop that does K + 1 iterations. The plus one is because we need to find the cheapest flight
               route with at most K stops in between. That translates to K + 1 edges at most.

            - In each iteration, we loop over all the edges in the graph and try to relax each one of them. Again, note
               that the edges or the flights are already given to us in the input and don't need to build any kind of
               adjacency list or matrix structure which is otherwise standard for other graph algorithms.

            - After K + 1 iterations, we check if the destination has been reached or not. If it's been discovered, then
               the distance at that point will be the shortest using at most K + 1 edges.

            - We use an array to store the current shortest distances of each node from the source. This is possible
               because the number of nodes is not big, and we don't need to use a dictionary here. However, a
               single array is not sufficient here because any values updated in a particular iteration cannot be used
               to update other values in the same iteration. Thus, we need another distance array which will store
               values of the previous iteration. So, we essentially use 2 arrays of size V, and we swap between them in
               each iteration i.e.
                        Iteration-0 ----
                        Array-1 is the main array
                        Array-2 becomes the previous array
                        Iteration-1 ----
                        Array-2 is the main array
                        Array-1 becomes the previous array

    Time complexity: O(K * E),  we have K+1 iterations and in each iteration we go over all the edges in the graph
    Space complexity: O(V), occupied by the two distance arrays
    """
    n = len(flights)
    prev_cost = [float('inf')] * n
    prev_cost[src] = 0
    for _ in range(k + 1):
        cur_cost = prev_cost[:]
        for source, destination, cost in flights:
            if prev_cost[source] + cost < cur_cost[destination]:
                cur_cost[destination] = prev_cost[source] + cost
        prev_cost = cur_cost
    return prev_cost[dst] if prev_cost[dst] != float('inf') else -1


class Test(unittest.TestCase):
    data = [([[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1, 200),
            ([[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0, 500)]

    def test_find_cheapest_price(self):
        for test_flights, test_src, test_dst, test_k, result in self.data:
            self.assertEqual(result, find_cheapest_price_v1(test_flights, test_src, test_dst, test_k))
            self.assertEqual(result, find_cheapest_price_v2(test_flights, test_src, test_dst, test_k))
            self.assertEqual(result, find_cheapest_price_v3(test_flights, test_src, test_dst, test_k))


if __name__ == '__main__':
    unittest.main()

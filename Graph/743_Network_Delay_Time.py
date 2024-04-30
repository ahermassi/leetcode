""" There are N network nodes, labelled 1 to N.
Given times, a list of travel times as directed edges times[i] = (u, v, w), where u is the source node, v is the target
node, and w is the time it takes for a signal to travel from source to target.
Now, we send a signal from a certain node K. How long will it take for all nodes to receive the signal? If it is
impossible, return -1 """

from collections import defaultdict, deque
from heapq import heappop, heappush
import unittest2 as unittest


def network_delay_time_v1(times, n, k):
    """ Depth-First Search.

         It is possible for a node to receive signals from multiple adjacent nodes at different times. The timestamp at
         which a node receives the signal is the time that the first signal reaches the node.

         Therefore, the problem boils down to finding the time required for each node to receive the signal, and the
         answer will be the maximum time required by any of the nodes. Why maximum? Because we need to find the time at
         which all nodes receive the signal, so the timestamp at which the last node receives the signal is the answer.

         In this approach, we simulate the signal and send it through the nodes as per the problem description to find
         the answer. Starting from node k, the signal will travel to the adjacent nodes along the directed edges. We
         track the signal movement with respect to time in a depth-first search manner.

        Start the DFS at vertex=k. At each vertex, we need to traverse all the adjacent nodes to the current node.
        For each adjacent node X, we update its timestamp to be the sum of the timestamp of the current node and the
        time it takes to traverse the edge from the current node to node X. Then, start a DFS from node X.

        As discussed before, there can be multiple signals received at a particular node, and we are only interested
        in the time that the first signal reached the node. Hence, we start a DFS only if the timestamp of a node X is
        greater than what it would be if it was reached from its parent vertex. This is because if the opposite is true,
        it means that node X received a signal before the current signal could reach it.

        There is a trick that can reduce the execution time. Instead of traversing adjacent nodes arbitrarily, we can
        traverse them in increasing order of their travel time. Although this will increase the time complexity of the
        algorithm, it will increase the probability of finding the fastest time path first. Hence, there could be fewer
        DFS calls and hence better execution time.

        Sorting is effective because we are likely to be able to reduce the number of the unnecessary DFS calls.
        In general, it is more likely to get the minimum time to reach one node if we start from the lowest cost.
        Keep in mind that every time we find a better (faster) path to reach the node, we need to call DFS again from
        the node.

            - Create an adjacency list such that graph[a] contains pairs (b, time). Here, time denotes the time required
               for the signal to travel from a to b.

            - For all nodes, initialize signal_received_at as a large value to signify that, so far, no signal has been
               received. Furthermore, initialize signal_received_at[k] = 0.

            - Start DFS from node k. For each recursive call:

                    * Sort the edges connecting to every node in graph[node] in increasing order of their travel time.
                    * Start a DFS from each of the adjacent nodes using the updated timestamp if it leads to a shorter
                       signal travel time, and set signal_received_at[adjacent_node] to signal_received_at[node] + edge_weight.

            - Find the maximum value in the array signal_received_at. If any value in signal_received_at is still the
               large value we initialized the array with, then return -1 as that node is not reachable from k.
               Otherwise, return the maximum value in the array.

        Summary:

        When visiting a node while t time has elapsed, if this is currently the fastest signal at this node, let's
        broadcast signals from this node. To speed things up, at each visited node we'll consider signals exiting the
        node that are faster first, by sorting the edges.

    Time complexity: O(N^N + E * logE), where N is the number of nodes and E is the length of times. We can only fully
    visit each node up to N-1 times, one per each other node. Also, we sort the edges corresponding to each node.
    Space complexity: O(N + E), building the adjacency list will take O(E) space and the runtime stack for DFS can have
    at most N active functions calls
    """

    def dfs(vertex):
        # Broadcast the signal to adjacent nodes
        for time, neighbor in sorted(graph[vertex]):
            # signal_received_at[vertex] + time = time when signal reaches the neighbor node
            # Only start a DFS from the neighbor node if it could receive a faster signal from the current node
            if signal_received_at[vertex] + time < signal_received_at[neighbor]:
                # Fastest signal time for the neighbor node so far
                signal_received_at[neighbor] = signal_received_at[vertex] + time
                dfs(neighbor)

    graph = defaultdict(list)
    for a, b, time in times:
        graph[a].append((time, b))  # The edge is (time, b) so we can sort by time
    signal_received_at = [float('inf')] * (n + 1)  # signal_received_at[node] = the earliest time signal reached node
    signal_received_at[0] = 0  # Node 0 doesn't exist
    signal_received_at[k] = 0  # It takes no time for the signal to travel from and to node k
    dfs(k)
    return max(signal_received_at) if max(signal_received_at) != float('inf') else -1


# Video explanation: https://www.youtube.com/watch?v=EaphyqKU4PQ
# Excellent Dijkstra's explanation: https://www.youtube.com/watch?v=pVfj6mxhdMw
def network_delay_time_v2(times, n, k):
    """ Dijkstra's Algorithm.

         As mentioned earlier, our objective is to find the fastest path from node k to every other node. This is a
         typical use case for the Single Source Shortest Path (SSSP) algorithm. Hence, in this approach, we use
         Dijkstra's algorithm to find the fastest path to every node from node k.

         We start with node k and then iterate over every adjacent node. In the previous approach, we broadcast the
         signal from visited nodes using DFS. However, in this approach, we use a priority queue to traverse the nodes
         in increasing order of the time required to reach them. Therefore, at each iteration, we visit the node with
         the shortest required travel time. This will help us find the fastest time path first.

             - Create an adjacency list such that graph[a] contains pairs (b, time). Here, time denotes the time
                required for the signal to travel from a to b.

             - For all the nodes, initialize signal_received_at as a large value to signify that, so far, no signal has
                been received. Furthermore, initialize signal_received_at[k] = 0.

             - Initialize a priority queue with the pair starting node k and its distance 0. While the priority queue
                is not empty:

                     * Pop the top node from the priority queue.
                     * Then, traverse all outgoing edges connected to the current node. Add an adjacent node to the
                        priority queue using the updated timestamp only if it leads to a shorter signal travel time, and
                        set signal_received_at[adjacent_node] to signal_received_at[node] + edge_weight.

             - Find the maximum value in the array signal_received_at. If any value in signal_received_at is still the
                large value we initialized the array with, then return -1 as that node is not reachable from k.
                Otherwise, return the maximum value in the array.

         The algorithm is based on repeatedly making the candidate move that has the least travel distance.
         We use a priority queue to store all the nodes we encounter and their distances from node k using a tuple
         (distance to k, node).

         The priority queue prioritizes neighbors with shorter distances. That means that if a node gets added twice
         (but one distance is larger than the other), the shorter distance will be polled first. Then, it will have been
         visited and even if we come across it again it just gets skipped. Also, since the nodes are added in closest to
         furthest and there are no negative distances, we don't have to worry about a case where a larger distance is
         added first and then a shorter distance version comes along (for same node). When a node is added, it is
         guaranteed to be the next closest unvisited node.

    Time complexity: O(E logV), where V is the number of vertices and E is the number of total edges in the given
    network. The heap size can grow up to E, since we're just dumping all the neighbors into it. Thus, push and pop
    operations on the priority queue take O(logE) time. The value of E can be at most V * (V−1). Therefore, O(logE) is
    equivalent to O(log V^2), which in turn is equivalent to O(2logV). Hence, the time complexity for priority queue
    operations equals O(logV). Although the number of vertices in the priority queue could be equal to E, we visit each
    vertex only once. If we encounter a vertex a second time, then it is guaranteed this vertex had its distance from
    node k set to a shorter distance at an earlier iteration, and we can continue to the next vertex in the priority
    queue. Hence, in total E edges are traversed and for each edge, there could be one priority queue insertion
    operation.
    Space complexity: O(N+ E), graph and heap store at most E entries, signal_received_at takes O(N) space
    """
    graph = defaultdict(list)
    for a, b, time in times:
        graph[a].append((b, time))
    signal_received_at = [float('inf')] * (n + 1)
    signal_received_at[0] = 0
    signal_received_at[k] = 0
    queue = [(0, k)]
    while queue:
        travel_time, vertex = heappop(queue)
        for neighbor, time in graph[vertex]:
            if travel_time + time < signal_received_at[neighbor]:
                # If traveling to the neighbor node doesn't result in a shorter signal time, we can skip.
                # If we arrive at a node, we're sure we got here in the least amount of time because we use a min heap.
                signal_received_at[neighbor] = travel_time + time
                heappush(queue, (signal_received_at[neighbor], neighbor))
    return max(signal_received_at) if max(signal_received_at) != float('inf') else -1


def network_delay_time_v3(times, n, k):
    """ Slight improvement of the previous solution.

         In fact, we don't have to pop all the nodes from the heap. We can terminate early when we have visited all the
         nodes along the shortest path from the source node.

    Time complexity: O(E logV)
    Space complexity: O(N + E)
    """
    graph = defaultdict(list)
    for a, b, time in times:
        graph[a].append((b, time))
    signal_received_at = [float('inf')] * (n + 1)
    signal_received_at[0] = 0
    signal_received_at[k] = 0
    queue = [(0, k)]
    visited = 1  # Start at 1 since the source node k was "visited" (its shortest distance was figured out)
    while queue:
        travel_time, vertex = heappop(queue)
        for neighbor, time in graph[vertex]:
            if travel_time + time < signal_received_at[neighbor]:
                signal_received_at[neighbor] = travel_time + time
                heappush(queue, (signal_received_at[neighbor], neighbor))
                visited += 1
                if visited == n:
                    break
    return max(signal_received_at) if max(signal_received_at) != float('inf') else -1


def network_delay_time_v4(times, n, k):
    """ This is the standard Dijkstra's algorithm using a regular queue.

    Time complexity: O(V^2 + E), where V is the number of vertices and E is the number of edges
    Space complexity: O(V + E), the size of the graph is O(E) and the size of the queue is O(V),
    signal_received_at takes O(V) space
    """
    graph = defaultdict(list)
    for a, b, time in times:
        graph[a].append((b, time))
    signal_received_at = [float('inf')] * (n + 1)
    signal_received_at[0] = signal_received_at[k] = 0
    queue = deque([(0, k)])
    while queue:
        travel_time, vertex = queue.popleft()
        for neighbor, time in graph[vertex]:
            if travel_time + time < signal_received_at[neighbor]:
                signal_received_at[neighbor] = travel_time + time
                queue.append((signal_received_at[neighbor], neighbor))
    return max(signal_received_at) if max(signal_received_at) != float('inf') else -1


class Test(unittest.TestCase):
    data = [([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2, 2)]

    def test_network_delay_time(self):
        for test_times, test_n, test_k, result in self.data:
            self.assertEqual(result, network_delay_time_v1(test_times, test_n, test_k))
            self.assertEqual(result, network_delay_time_v2(test_times, test_n, test_k))
            self.assertEqual(result, network_delay_time_v3(test_times, test_n, test_k))
            self.assertEqual(result, network_delay_time_v4(test_times, test_n, test_k))


if __name__ == '__main__':
    unittest.main()

""" There are N network nodes, labelled 1 to N.
Given times, a list of travel times as directed edges times[i] = (u, v, w), where u is the source node, v is the target
node, and w is the time it takes for a signal to travel from source to target.
Now, we send a signal from a certain node K. How long will it take for all nodes to receive the signal? If it is
impossible, return -1 """

from collections import defaultdict, deque
from heapq import heappop, heappush
import unittest2 as unittest


def network_delay_time_v1(times, N, K):
    """ DFS. Let's record the time time[node] when the signal reaches the node. If some signal arrived earlier, we
        don't need to broadcast it anymore. Otherwise, we should broadcast the signal.
        We'll maintain time[node], the earliest that we arrived at each node. When visiting a node while t time has
        elapsed, if this is the currently fastest signal at this node, let's broadcast signals from this node.
        To speed things up, at each visited node we'll consider signals exiting the node that are faster first, by
        sorting the edges. Sorting is effective because we are likely to be able to reduce the number of the
        unnecessary calls to dfs(). In general, it is more likely to get the minimum time to reach one node if we start
        from the lowest cost. Keep in mind that every time we find a better (faster) path to reach the node, we need to
        call dfs() again from the node.
        We visit each node at some time, and if that time is better than the fastest time we've reached this node, we
        travel along outgoing edges in sorted order.
    Time complexity: O(N^N + E * logE), where E is the length of times. We can only fully visit each node up to N-1
    times, one per each other node. Plus, we have to explore every edge and sort them.
    Space complexity: O(N + E), the size of the graph (O(E), plus the size of the implicit call stack in DFS (O(N))
    """

    def dfs(node, cur_time):
        if time[node] <= cur_time:  # We arrived at this node earlier than this in the past
            return
        time[node] = cur_time
        for t, neighbor in sorted(graph[node]):
            dfs(neighbor, cur_time + t)

    graph = defaultdict(list)
    for source, destination, time in times:
        graph[source].append((time, destination))  # The edge is (time, destination) so we can sort on time later on
    time = {i: float('inf') for i in range(1, N + 1)}  # time[i] = the earliest (least amount of time) we've reached i
    dfs(K, 0)
    return max(time.values()) if max(time.values()) != float('inf') else -1


def network_delay_time_v2(times, N, K):
    """ Dijkstra's algorithm using priority queue (heap). The algorithm is based on repeatedly making the candidate
        move that has the least distance traveled.
        We use a priority queue to store all the nodes we encounter and their distances to K using a tuple
        (distance to K, node). For every node we visit, if its distance to K is determined, we don't need to look at it
        anymore because we always pop the nearest one to K in the priority queue, so we can be sure that the distance
        is the shortest. Otherwise, we keep on exploring its neighbors. [4]
        If we don't visit every node we return -1, else we return the node which takes the longest time to reach.
    Time complexity: O(E logE), since heap might store E number of edges and each operation takes logE
    Space complexity: O(E), graph and heap store at most E number of entries
    """
    graph = defaultdict(dict)
    for source, destination, time in times:
        graph[source][destination] = time
    time, heap = {}, [(0, K)]
    while heap:
        cur_time, node = heappop(heap)
        if node in time:
            continue
        time[node] = cur_time  # If we arrive at a node, we're sure we got here in the least amount of time since we
        # use a min heap
        for neighbor, t in graph[node].items():
            heappush(heap, (cur_time + t, neighbor))  # The min heap is sorted in ascending order of time
    return max(time.values()) if len(time) == N else -1


def network_delay_time_v3(times, N, K):
    """ Slight improvement of the previous solution. In fact, we don't have to pop all the elements from the heap, and
        we can terminate early when N = 0, since when N = 0 we have visited all the nodes along the shortest path from
        the source node.
    Time complexity: O(E logE)
    Space complexity: O(E)
    """
    graph = defaultdict(dict)
    for source, destination, time in times:
        graph[source][destination] = time
    time, heap = {}, [(0, K)]
    while heap:
        cur_time, node = heappop(heap)
        if node in time:
            continue
        time[node] = cur_time
        N -= 1  # Improvement
        if not N:
            return max(time.values())
        for neighbor, t in graph[node].items():
            heappush(heap, (cur_time + t, neighbor))
    return -1


def network_delay_time_v4(times, N, K):
    """ This is the standard Dijkstra's algorithm using a normal queue.
    Time complexity: O(N^2 + E), where E is the length of times
    Space complexity: O(N + E), the size of the graph (O(E)) plus the size of the queue (O(N)) and hash map
    """
    graph = defaultdict(dict)
    for source, destination, time in times:
        graph[source][destination] = time
    time = {i: float('inf') for i in range(1, N + 1)}
    queue = deque([(0, K)])
    while queue:
        cur_time, node = queue.popleft()
        if cur_time < time[node]:
            time[node] = cur_time
            for neighbor, t in graph[node].items():
                queue.append((cur_time + t, neighbor))
    return max(time.values()) if max(time.values()) != float('inf') else -1


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

""" There are N network nodes, labelled 1 to N.
Given times, a list of travel times as directed edges times[i] = (u, v, w), where u is the source node, v is the target
node, and w is the time it takes for a signal to travel from source to target.
Now, we send a signal from a certain node K. How long will it take for all nodes to receive the signal? If it is
impossible, return -1 """

from collections import defaultdict
import unittest2 as unittest


def network_delay_time_v1(times, N, K):
    """ DFS. Let's record the time time[node] when the signal reaches the node. If some signal arrived earlier, we
        don't need to broadcast it anymore. Otherwise, we should broadcast the signal.
        We'll maintain time[node], the earliest that we arrived at each node. When visiting a node while t time has
        elapsed, if this is the currently-fastest signal at this node, let's broadcast signals from this node.
        To speed things up, at each visited node we'll consider signals exiting the node that are faster first, by
        sorting the edges.
    """

    def dfs(node, t):
        if t >= time[node]:  # We've arrived at i earlier than this in the past
            return
        time[node] = t
        for u, v in sorted(graph[node]):
            dfs(v, t + u)

    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((w, v))  # Note that the edge is (time, destination) so we can sort on times later on
    time = {i: float('inf') for i in range(1, N + 1)}  # time[i] == the earliest (least amount of time) we've reached i
    dfs(K, 0)
    return max(time.values()) if max(time.values()) != float('inf') else -1


class Test(unittest.TestCase):
    data = [([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2, 2)]

    def test_network_delay_time(self):
        for test_times, test_n, test_k, result in self.data:
            self.assertEqual(result, network_delay_time_v1(test_times, test_n, test_k))


if __name__ == '__main__':
    unittest.main()

""" Read description on Leetcode """

from heapq import heappush, heappop
import unittest2 as unittest


def assign_bikes_v1(workers, bikes):
    """ Since the range of distance is [0, 2000] (because each x and y coordinate is <= 1000), it's reasonable to use
        bucket sort. Basically, it's to put each pair into the bucket representing its distance. Eventually, we can
        loop through each bucket from lower distance.
    Time complexity: O(N * M), where N is the number of workers and M is the number of bikes
    Space complexity: O(N * M), as we have N * M pairs of distances
    """
    distances = [[] for _ in range(2001)]
    for i, (a, b) in enumerate(workers):
        for j, (c, d) in enumerate(bikes):
            distance = abs(a - c) + abs(b - d)
            distances[distance].append((i, j))  # distance[i]: list of pairs (worker,bike) whose Manhattan distance is i
    res = [-1] * len(workers)
    used_bikes = set()
    for i in range(len(distances)):  # Looping through 'distances' array guarantees we pick the shortest distance first
        for worker, bike in distances[i]:
            if res[worker] == -1 and bike not in used_bikes:
                res[worker] = bike
                used_bikes.add(bike)
    return res


def assign_bikes_v2(workers, bikes):
    """ Heap solution. TLE
        Initiate a priority queue of bike and worker pairs. The heap order should be Distance ASC, WorkerIndex ASC,
        Bike ASC.
        Loop through all workers and bikes, calculate their distance, and then throw it to the queue.
        Initiate a set to keep track of the bikes that have been assigned.
        Initiate a result array and fill it with -1. (unassigned)
        Poll every possible pair from the priority queue and check if the person already got his bike or the bike has
        been assigned.
        Early exit when everyone gets their bike.
        The reason of TLE is the huge number of elements in the heap which can go up to N * M, with push/pop operations
        that take O(log(N*M)).
    Time complexity: O(log(N*M)), as the heap can have at most N * M elements
    Space complexity: O(N *M) for the heap
    """
    heap = []
    for i, (a, b) in enumerate(workers):
        for j, (c, d) in enumerate(bikes):
            distance = abs(a - c) + abs(b - d)
            heappush(heap, (distance, i, j))
    res, used_bikes = [-1] * len(workers), set()
    while len(used_bikes) < len(workers):
        distance, worker, bike = heappop(heap)
        if res[worker] == -1 and bike not in used_bikes:
            res[worker] = bike
            used_bikes.add(bike)
    return res


class Test(unittest.TestCase):
    data = [([[0, 0], [2, 1]], [[1, 2], [3, 3]], [1, 0]),
            ([[0, 0], [1, 1], [2, 0]], [[1, 0], [2, 2]], [2, 1])]

    def test_search(self):
        for test_workers, test_bikes, result in self.data:
            self.assertEqual(result, assign_bikes_v1(test_workers, test_bikes))


if __name__ == '__main__':
    unittest.main()

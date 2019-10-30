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
    Time complexity: O(N*M log(N*M)), as the heap can have at most N * M elements
    Space complexity: O(N * M) for the heap
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


def assign_bikes_v3(workers, bikes):
    """ Heap solution.
        For each worker, create a sorted list of distances to each bike. The elements of the list are tuples (distance,
        worker, bike).
        For each worker, add the tuple with the shortest distance to the heap.
        Until each worker has a bike, pop the smallest distance from the heap.
        If this bike is not used, update the result for this worker, else add the next closest tuple for this worker to
        the heap.
    Time complexity: O(N*M (log N + log M)) == O(N*M log(N*M)). For each worker, making list of distances to each bike
    is O(N * M). For each worker, sort the list of distances is O(N (M log M)), which dominates making the lists above.
    There is one distance on the heap for each worker, so each pop or push is O(log M).
    In the worst case where the closest bike on the heap is always used, there may be O(N * M) pops, so O((N*M) log M))
    for the heap. So in the best case the first bike on the heap is always free and there will be O(N) pops.
    So O(N log N) for the heap and overall O(N (M log M + log N))
    Space complexity: TODO
    """
    n = len(workers)
    heap, distances = [], [[] for _ in range(n)]  # distances[i] is tuple of (distance, worker, bike) for each worker i
    for i, (a, b) in enumerate(workers):
        for j, (c, d) in enumerate(bikes):
            distance = abs(a - c) + abs(b - d)
            distances[i].append((distance, i, j))
        distances[i].sort(reverse=True)  # Reverse so we can pop the smallest distance we construct the heap
        # At the end of each iteration 'i', distance[i] is a list of (distance, worker, bike) for worker 'i'
    for distance in distances:
        heappush(heap, distance.pop())  # Smallest distance for each worker, so we get a heap of size n = len(workers)
    res, used_bikes = [-1] * n, set()
    while len(used_bikes) < n:
        distance, worker, bike = heappop(heap)
        if bike not in used_bikes:
            res[worker] = bike
            used_bikes.add(bike)
        else:
            heappush(heap, distances[worker].pop())  # Bike used, so add next closest bike
    return res


class Test(unittest.TestCase):
    data = [([[0, 0], [2, 1]], [[1, 2], [3, 3]], [1, 0]),
            ([[0, 0], [1, 1], [2, 0]], [[1, 0], [2, 2]], [2, 1])]

    def test_search(self):
        for test_workers, test_bikes, result in self.data:
            self.assertEqual(result, assign_bikes_v1(test_workers, test_bikes))


if __name__ == '__main__':
    unittest.main()

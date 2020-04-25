""" Read description on Leetcode """

from heapq import heappush, heappop
import unittest2 as unittest


def assign_bikes_v1(workers, bikes):
    """ Since the range of distances is [0, 1998] (because each x and y coordinate is >= 0 and < 1000), it's reasonable
        to use bucket sort. Basically, it's to put each pair into the bucket representing its distance. Eventually, we
        can loop through each bucket from lower distance.
        Note that when pushing back (worker_id, bike_id) into the distances array, the worker with smaller id will be
        pushed first, because we are iterating from worker_id 0 to the (len(workers) - 1). The case for bike_id is
        similar. In the assignment part, for the same Manhattan distance, we always have workers with smaller id be
        assigned first.
    Time complexity: O(N * M), where N is the number of workers and M is the number of bikes
    Space complexity: O(N * M), as we have N * M pairs of distances
    """
    distances = [[] for _ in range(1999)]
    for i, (x, y) in enumerate(workers):
        for j, (a, b) in enumerate(bikes):
            distance = abs(x - a) + abs(y - b)
            distances[distance].append((i, j))  # distance[d]: list of pairs (worker,bike) whose Manhattan distance is d
    res, used_bikes = [-1] * len(workers), set()
    for pairs in distances:  # Looping through 'distances' array guarantees we pick the shortest distance first
        for worker, bike in pairs:
            if res[worker] == -1 and bike not in used_bikes:
                res[worker] = bike
                used_bikes.add(bike)
    return res


def assign_bikes_v2(workers, bikes):
    """ Heap solution. TLE
        Initiate a priority queue of (bike,worker) pairs. The heap order should be distance ascending, worker index
        ascending, bike index ascending.
        Loop through all workers and bikes, calculate their distance, and then add it to the queue.
        Initiate a set to keep track of the bikes that have been assigned.
        Initiate a result array and fill it with -1. (unassigned)
        Poll every possible pair from the priority queue and check if the person already got his bike or the bike has
        been assigned.
        Early exit when everyone gets their bike.
        The reason of TLE is the huge number of elements in the heap which can go up to (N * M), with push/pop
        operations that take O(log(N * M)).
    Time complexity: O(N * M log(N * M)), as the heap can have at most N * M elements
    Space complexity: O(N * M), for the heap
    """
    heap, res, len_workers = [], [-1] * len(workers), len(workers)
    used_bikes = set()
    for i, (x, y) in enumerate(workers):
        for j, (a, b) in enumerate(bikes):
            distance = abs(x - a) + abs(y - b)
            heappush(heap, (distance, i, j))
    while len(used_bikes) < len_workers:
        _, worker, bike = heappop(heap)
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
    Time complexity: O(N * M (log N + log M)) == O(N * M log(N * M)). For each worker, making list of distances to each
    bike is O(N * M). Sorting the lists of distances is O(N * (M logM)), which dominates creating the above lists.
    There is one distance on the heap for each worker, so each pop or push is O(logM).
    In the worst case where the closest bike on the heap is always used, there may be O(N * M) pops, so O((N * M) logM))
    for the heap. So in the best case the first bike on the heap is always free and there will be O(N) pops.
    So O(N logN) for the heap and overall O(N (M logM + logN))
    Space complexity: TODO
    """
    n = len(workers)
    heap, distances = [], [[] for _ in range(n)]  # distances[i] is a tuple (distance, worker, bike) for each worker i
    for i, (x, y) in enumerate(workers):
        for j, (a, b) in enumerate(bikes):
            distance = abs(x - a) + abs(y - b)
            distances[i].append((distance, i, j))
        distances[i].sort(reverse=True)  # Reverse so we can pop the smallest distance as we construct the heap
        # At the end of each iteration i, distance[i] is a list of (distance, worker, bike) for worker i
    for distance in distances:
        heappush(heap, distance.pop())  # Smallest distance for each worker, so we get a heap of size n = len(workers)
    res, used_bikes = [-1] * n, set()
    while len(used_bikes) < n:
        _, worker, bike = heappop(heap)
        if bike not in used_bikes:
            res[worker] = bike
            used_bikes.add(bike)
        else:
            heappush(heap, distances[worker].pop())  # Bike used, so add next closest bike
    return res


class Test(unittest.TestCase):
    data = [([[0, 0], [2, 1]], [[1, 2], [3, 3]], [1, 0]),
            ([[0, 0], [1, 1], [2, 0]], [[1, 0], [2, 2]], [2, 1])]

    def test_assign_bikes(self):
        for test_workers, test_bikes, result in self.data:
            self.assertEqual(result, assign_bikes_v1(test_workers, test_bikes))


if __name__ == '__main__':
    unittest.main()

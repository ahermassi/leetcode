""" We have a list of points on the plane.  Find the K closest points to the origin (0, 0).
(Here, the distance between two points on a plane is the Euclidean distance.)
You may return the answer in any order.  The answer is guaranteed to be unique (except for the order that it is in.) """

from heapq import heappushpop, heappush


def k_closest_v1(points, K):
    """ We maintain a max-heap with size K. Then for each point, we add it to the heap. Once the size of the heap is
        greater than K, we are supposed to extract one from the max heap to ensure the size of the heap is always K.
        Thus, the max heap is always maintaining top K smallest elements from the first one to current one. Once the
        size of the heap is over its maximum capacity, it will exclude the maximum element in it, since it can not be
        the proper candidate anymore.
        Since Python's standard heap is a min heap, push negative values to make it a max heap.
    Time complexity: O(N * logK): inserting an item to a heap of size k takes O(logK) time, and we do this for each item
    in points. So runtime is O(N * logK) where N is the length of points.
    Space complexity: O(K) for the heap
    """
    heap = []
    for x, y in points:
        d = x * x + y * y
        if len(heap) == K:
            heappushpop(heap, (-d, x, y))
        else:
            heappush(heap, (-d, x, y))
    return [[b, c] for a, b, c in heap]



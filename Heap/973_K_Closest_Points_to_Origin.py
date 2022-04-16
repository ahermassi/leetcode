""" We have a list of points on the plane.  Find the K closest points to the origin (0, 0).
(Here, the distance between two points on a plane is the Euclidean distance.)
You may return the answer in any order.  The answer is guaranteed to be unique (except for the order that it is in.) """

from heapq import heappush, heappop
from random import randint


def k_closest_v1(points, K):
    """ While we must iterate over all elements in the points array, we only need to keep track of the K closest points
        encountered so far. We could therefore choose to store them in a separate data structure. In order to keep this
        data structure capped at K elements, we will need to keep track of the point that is the farthest away from the
        origin and thus the next point to be removed when a closer point is found.

        We maintain a max-heap with size K. Then for each point, we add it to the heap. Once the size of the heap is
        greater than K, we are supposed to extract one from the max heap to ensure the size of the heap is always K.
        Thus, the max heap is always maintaining top K smallest elements from the first one to current one. Once the
        size of the heap is over its maximum capacity, it will exclude the maximum element in it, since it can not be
        the proper candidate anymore. At the end of iteration, we would only be left with K smallest elements
        (since we popped off larger distanced elements whenever number of elements in heap exceeded K).
        Since Python's standard heap is a min heap, push negative values to make it a max heap.
        Note that another way to use heap would be to construct a min-heap and pop the min elements k times.

    Time complexity: O(N logK): inserting an item to a heap of size K takes O(logK) time, and we do this for each item
    in points. So runtime is O(N logK) where N is the length of points.
    Space complexity: O(K) for the heap
    """
    heap = []
    for x, y in points:
        distance = (x ** 2 + y ** 2) ** 0.5
        heappush(heap, (-distance, x, y))
        if len(heap) > K:
            heappop(heap)
    return [[x, y] for d, x, y in heap]


def k_closest_v2(points, K):
    """ This solution is based on quick sort, we can also call it quick select. In the quick sort, we will always
        choose a pivot to compare with other elements.
        Partition in quick select picks a pivot (either randomly or first/last element). Then it rearranges the array
        in a way that all elements less than the pivot are on left side of pivot and others on right. It then returns
        index of the pivot element.
        Now here we are finding kth smallest element. After partition cases are:
            1- K == pivot, then we have already found kth smallest. This is because the way partition is working.
                There are exactly (k - 1) elements that are smaller than the kth smallest element.
            2- K < pivot, then kth smallest is on the left side of pivot.
            3- K > pivot, then kth smallest is on the right side of pivot. To find it, we actually have to find
                (k - pivot)th smallest number to the right.
    Time complexity: the average time complexity is O(N) , but just like quick sort, in the worst case, this solution
    would be degenerated to O(N^2)
    Space complexity: O(N) where N is the length of points
    """

    def partition(left, right):
        pivot_index = randint(left, right)  # Select a random pivot index between left and right, so that even when
        # the worst case input would be provided the algorithm wouldn't be affected
        pivot = points[pivot_index]
        points[pivot_index], points[right] = points[right], points[pivot_index]
        pivot_distance = distance(pivot[0], pivot[1])
        i = j = left  # i will keep track of the 'tail' of the section of items less than the pivot so that
        # at the end we can 'sandwich' the pivot between the section less than it and the section greater than it.
        # j will scan for us. All the elements before i (excluding i) are less than or equal to the pivot
        while j < right:
            if distance(points[j][0], points[j][1]) <= pivot_distance:  # If this point's distance from origin is less
                # than the pivot's distance, it needs to be moved to the section of items less than the pivot
                points[i], points[j] = points[j], points[i]  # Execute the swap
                i += 1
            j += 1
        points[i], points[right] = points[right], points[i]  # Bring the pivot back after the section of items less
        # than the pivot. i keeps the tail of this section
        return i  # Return the pivot's final resting position

    distance = lambda x, y: x * x + y * y
    left, right = 0, len(points) - 1
    while left <= right:
        pivot = partition(left, right)
        if pivot == K:
            break
        if pivot < K:
            left = pivot + 1
        else:
            right = pivot - 1
    return points[:K]


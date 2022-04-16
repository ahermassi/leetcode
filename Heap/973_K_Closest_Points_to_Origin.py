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
    """ This solution is based on QuickSort, we can also call it QuickSelect. In the QuickSort, we will always
        choose a pivot to compare with other elements. This solution is a modified version of QuickSort meant
        to be used when we need to find K (or Kth) smallest (or largest) elements (based on some comparator)
        but NOT IN ANY PARTICULAR ORDER.

        A typical QuickSelect function starts with two pointers (left, right) that define the entire range of indices
        in the given array. The function will iteratively apply a partitioning helper function (partition()) which will
        return the index of the borderline between the two subsequent partitions.

        Inside the partition() helper function, the first step is to find a suitable pivot value. The efficiency of the
        QuickSelect algorithm relies heavily upon picking a good pivot candidate; the closer the pivot is to the
        median value, the more likely each successive partitioning is to suitably narrow the range of values.

        After choosing a pivot value, the partition function will swap the values of the elements in the range until
        it is partitioned into two sides with values less than the pivot value on one side and the remaining values
        on the other. Like finding the pivot, there are multiple methods available to accomplish this, but we'll use
        a basic version in which we start with pointers at left end of its range and move inward, swapping elements
        with values less than the pivot value to the left side.

        Now here we are finding Kth smallest element. After partition cases are:

            1- K == pivot, then we have already found Kth smallest. This is because the way partition is working.
                There is exactly (K - 1) elements that are smaller than the Kth smallest element.
            3- pivot < K, then we now have 'pivot' elements which are closest to origin (although they aren't sorted in
                 any particular order) but we still need some more elements to get K points in total. Thus, we iterate
                 again and partition the array from indices [pivot+1, right] till we find K elements (by getting pivot at
                 Kth index)
            2- pivot > K, then we now have more than K elements with us that are closest to origin. But we are sure
                 that any element to the right of pivot won't be ever in our answer. So we iterate again and partition
                 just the range [left, pivot-1] till we find K elements.

    Time complexity: the average time complexity is O(N) because it halves (roughly) the remaining elements
    needing to be processed at each iteration. This results in N + N/2 + N/4 + N/8 + ... + ... = 2N total processes,
    yielding an average time complexity of O(N). But just like QuickSort, in the worst case, there's still a chance
    (although very low) that we choose the worst pivot at each partition and this leads to
    N + N-1 + N-2 + ... + 1 = N^2 total iterations leading to time complexity of O(N^2)
    Space complexity: O(1)
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
                points[i], points[j] = points[j], points[i]  # Perform the swap
                i += 1
            j += 1
        points[i], points[right] = points[right], points[i]  # Bring the pivot back after the section of items less
        # than the pivot. i keeps the tail of this section
        return i  # Return the pivot's final resting position

    distance = lambda x, y: x * x + y * y
    n = len(points)
    left, right = 0, n - 1
    pivot = n
    while pivot != n :
        pivot = partition(left, right)
        if pivot == K:
            break
        if pivot < K:
            left = pivot + 1
        else:
            right = pivot - 1
    return points[:K]
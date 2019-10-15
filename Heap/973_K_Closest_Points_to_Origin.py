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
    return [[x, y] for dist, x, y in heap]

# Review the algorithm and fix a bug


def k_closest_v2(points, K):
    """ This solution is based on quick sort, we can also call it quick select. In the quick sort, we will always
        choose a pivot to compare with other elements.
        Partition in quick select picks a pivot (either randomly or first/last element). Then it rearranges the list
        in a way that all elements less than pivot are on left side of pivot and others on right. It then returns
        index of the pivot element.
        Now here we are finding kth smallest element. After partition cases are:
            1- k == pivot. Then you have already found kth smallest. This is because the way partition is working.
                There are exactly k - 1 elements that are smaller than the kth element.
            2- k < pivot. Then kth smallest is on the left side of pivot.
            3- k > pivot. Then kth smallest is on the right side of pivot. And to find it you actually have to find
                k-pivot smallest number on right.
    Time complexity: the average time complexity is O(N) , but just like quick sort, in the worst case, this solution
    would be degenerated to O(N^2)
    Space complexity: O(N) where N is the length of points
    """

    def partition(left, right):
        pivot = left
        temp = points[pivot]
        while left < right and dist(pivot) <= dist(right):
            right -= 1
        points[left] = points[right]
        while left < right and dist(left) <= dist(pivot):
            left += 1
        points[right] = points[left]
        points[left] = temp
        return left

    dist = lambda i: points[i][0] ** 2 + points[i][1] ** 2
    left, right = 0, len(points) - 1
    while left <= right:
        mid = partition(left, right)
        if mid == K - 1:
            return points[:K]
        if mid < K - 1:
            left = mid + 1
        else:
            right = mid - 1



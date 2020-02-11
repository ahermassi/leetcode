""" Given a max-heap, represented as an array A, design an algorithm that computes the k largest elements stored in
the max-heap. You cannot modify the heap. """

from heapq import heappush, heappop


def k_largest_in_binary_heap(A, k):
    """ The brute-force algorithm is to perform k extract-max operations. The time complexity is O(k logN),where N is
        the number of elements in the heap. Note that this algorithm entails modifying the heap.
        The following algorithm is based on the insight that the heap has partial order information.
        Specifically, a parent node always stores value greater than or equal to the values stored at its children.
        Therefore, the root, which is stored in A[0], must be one of the k largest elements. In fact, it is the largest
        element. The second largest element must be the larger of the root's children, which are A[1] and A[2]. This is
        the index we continue processing from.
        The ideal data structure for tracking the index to process next is a data structure which supports fast
        insertions and fast extract-max, i.e., a max heap. So our algorithm is to create a max heap of candidates,
        initialized to hold the index 0, which serves as a reference to A[0]. The indices in the candidates max heap
        are ordered according to corresponding value in A. We then iteratively perform k extract-max operations from
        the candidates max heap. Each extraction of an index i is followed by inserting the indices of i's left child,
        2i + 1, and right child, 2i + 2, to the candidates heap, assuming these children exist.
    Time complexity: O(K logK), the total number of insertion and extract-max operations is O(K)
    Space complexity: O(K)
    """
    res, candidates_heap, n = [], [], len(A)
    heappush(candidates_heap, (-A[0], 0))  # The largest element in A is at index 0
    for _ in range(k):
        val, index = heappop(candidates_heap)
        res.append(-val)
        left_index = 2 * index + 1
        if left_index < n:
            heappush(candidates_heap, (-A[left_index], left_index))
        right_index = 2 * index + 2
        if right_index < n:
            heappush(candidates_heap, (-A[right_index], right_index))
    return res

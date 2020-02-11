""" Design an efficient algorithm that takes a sorted array of distinct integers, and returns an index i such that the
element at index i equals i. """


def search_entry_equal_to_its_index(A):
    """ Note that the difference between an entry and its index increases by at least 1 as we iterate through A.
        Observe that if A[i] > i, then no entry after i can satisfy the given criterion. This is because each element
        in the array is at least 1 greater than the previous element. For the same reason, if A[i] < i, no entry before
        i can satisfy the given criterion.
        The above observations can be directly used to create a binary search type algorithm for finding an i such
        that A[i] = i. A slightly simpler approach is to search the secondary array B whose ith entry is A[i] - i
        for 0, which is just ordinary binary search. We do not need to actually create the secondary array, we can
        simply use A[i] - i wherever B[i] is referenced.
        For the example A = [-2, 0, 2, 3, 6, 7, 9], the secondary array B is B = [-2, -1, 0, 0, 2, 2, 3].
        Binary search for 0 returns the desired result, i.e., either index 2 or 3.
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(A) - 1
    while left <= right:
        mid = (left + right) // 2
        difference = A[mid] - mid
        if difference == 0:
            return mid
        if difference > 0:
            right = mid - 1
        else:
            left = mid + 1
    return -1

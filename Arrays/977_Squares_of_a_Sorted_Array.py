""" Given an array of integers A sorted in non-decreasing order, return an array of the squares of each number,
also in sorted non-decreasing order. """

from collections import deque
import unittest2


def sorted_squares_v1(A):
    """ This is the most straightforward way, using sorted() built-in.
    Time complexity: O(N logN) for the Tim sort
    Space complexity: O(N) for the new created list
    """
    return sorted([i ** 2 for i in A])


def sorted_squares_v2(A):
    """ Use two pointers, one at each end, to iteratively collect the larger square to a list. However, collecting the
        larger square in a list with list's append results in elements sorted in descending order. To circumvent this,
        we need to append to the left of the list.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    result = deque()
    l, r = 0, len(A) - 1
    while l <= r:
        left, right = abs(A[l]), abs(A[r])
        if left > right:
            result.appendleft(left ** 2)
            l += 1
        else:
            result.appendleft(right ** 2)
            r -= 1
    return list(result)


def sorted_squares_v3(A):
    """ Use two pointers, but this time without a deque. Instead, add the larger square from the back of the result
    list, denoted by the index i
    Time complexity: O(N)
    Space complexity: O(1)
    """
    res = [0] * len(A)
    left, right = 0, len(A) - 1
    i = len(A) - 1
    while left <= right:
        if abs(A[right]) >= abs(A[left]):
            res[i] = A[right] ** 2
            right -= 1
        else:
            res[i] = A[left] ** 2
            left += 1
        i -= 1
    return res


def sorted_squares_v4(A):
    """ Sorting in-place and then calculating squares
    Time complexity: O(N logN) for Timsort
    Space complexity: O(1) since first sorting is in-place
     """
    A.sort(key=abs)
    for i in range(len(A)):
        A[i] = A[i] ** 2
    return A


class Test(unittest2.TestCase):
    test_data = [-7, -3, 0, 2, 4, 6]

    def test_sorted_squares(self):
        self.assertEqual([0, 4, 9, 16, 36, 49], sorted_squares_v3(self.test_data))


if __name__ == '__main__':
    unittest2.main()


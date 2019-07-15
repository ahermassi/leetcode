""" Given an array of integers A sorted in non-decreasing order, return an array of the squares of each number,
also in sorted non-decreasing order. """
from collections import deque
import unittest2


def sorted_squares_v1(A):
    """ 
    :param A: List[int]
    :return: List[int]
    This is the most straightforward way, using sorted() built-in.
    Time complexity: O(N log N) for the Timsort
    Space complexity: O(N) for the new created list
    """
    return sorted([i ** 2 for i in A])


def sorted_squares_v2(A):
    """ Use two pointers, one at each end, to iteratively collect the larger square
    to a list. However, collecting the larger square in a list with list's append, results in elements sorted in
    descending order. To circumvent this, we need to append to the left of the list.
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


class Test(unittest2.TestCase):
    test_data = [-7, -3, 0, 2, 4, 6]

    def test_sorted_squares(self):
        self.assertEqual([0, 4, 9, 16, 36, 49], sorted_squares_v2(self.test_data))


if __name__ == '__main__':
    unittest2.main()


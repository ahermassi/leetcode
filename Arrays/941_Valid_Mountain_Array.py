""" Given an array A of integers, return true if and only if it is a valid mountain array. """

import unittest2 as unittest


def valid_mountain_array_v1(A):
    """ If we walk along the mountain from left to right, we have to move strictly up, then strictly down.
        Walk up from left to right until we can't: that has to be the peak. We should ensure the peak is not the first
        or last element. Then, we walk down. If we reach the end, the array is valid, otherwise it is not.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    i = 0
    while i < len(A) - 1 and A[i] < A[i + 1]:
        i += 1
    if i == 0 or i == len(A) - 1:
        return False
    while i < len(A) - 1 and A[i] > A[i + 1]:
        i += 1
    return i == len(A) - 1


def valid_mountain_array_v2(A):
    """ Two people climb from left and from right separately. If they are climbing the same mountain, they will meet at
        the same point.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(A)
    left, right = 0, n - 1
    while left < n - 1 and A[left] < A[left + 1]:
        left += 1
    while right > 0 and A[right - 1] > A[right]:
        right -= 1
    return 0 < left == right < n - 1


class Test(unittest.TestCase):
    data = [([2, 1], False),
            ([3, 5, 5], False),
            ([0, 3, 2, 1], True)
            ]

    def test_valid_mountain_array(self):
        for test_array, result in self.data:
            self.assertEqual(result, valid_mountain_array_v1(test_array))
            self.assertEqual(result, valid_mountain_array_v2(test_array))


if __name__ == '__main__':
    unittest.main()

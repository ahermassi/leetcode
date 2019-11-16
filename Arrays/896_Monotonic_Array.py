""" An array is monotonic if it is either monotone increasing or monotone decreasing.
An array A is monotone increasing if for all i <= j, A[i] <= A[j].  An array A is monotone decreasing if for all
i <= j, A[i] >= A[j].
Return true if and only if the given array A is monotonic. """

import unittest2 as unittest


def is_monotonic_v1(A):
    """ To perform this check in one pass, we want to remember if it is monotone increasing or monotone decreasing.
        If it is either monotone increasing or monotone decreasing, then A is monotonic.
        We initially assume that the array is neither increasing nor decreasing.
        While traversing an array, as long as a number is found to be greater than the number behind it, then
        'increasing' will be assigned the value True. Similarly, as long as a number is less than the number behind it,
        'decreasing' will be assigned True. If at any time the array becomes 'increasing' and 'decreasing'
        simultaneously, then it can't be monotonic.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    increasing = decreasing = False
    n = len(A)
    for i in range(n - 1):
        if A[i] < A[i + 1]:
            increasing = True
        elif A[i] > A[i + 1]:
            decreasing = True
        if increasing and decreasing:
            return False
    return True


class Test(unittest.TestCase):
    data = [([6, 5, 4, 4], True),
            ([1, 2, 2, 3], True),
            ([1, 3, 2], False)
            ]

    def test_is_monotonic(self):
        for test_array, result in self.data:
            self.assertEqual(result, is_monotonic_v1(test_array))


if __name__ == '__main__':
    unittest.main()

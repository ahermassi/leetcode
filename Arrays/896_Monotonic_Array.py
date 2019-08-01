""" An array is monotonic if it is either monotone increasing or monotone decreasing.
An array A is monotone increasing if for all i <= j, A[i] <= A[j].  An array A is monotone decreasing if for all
i <= j, A[i] >= A[j].
Return true if and only if the given array A is monotonic. """

import unittest2 as unittest


def is_monotonic_v1(A):
    """ The idea is to start searching for the index that sets the tone of the array. This is to account for cases
    where the array starts with a sequence of equal values, say [1, 1, 1, 1, 2, 3]. Once that index found, set the
    boolean flag 'increasing' accordingly. From there, iterate and watch for the condition that contradicts the boolean.
    Time complexity: O(N) where N is the length of A
    Space complexity: O(1)
    """
    if len(A) <= 2:
        return True
    i = 0
    while i < len(A) - 1 and A[i] == A[i + 1]:
        i += 1
    if i == len(A) - 1:
        return True
    if A[i] < A[i + 1]:
        increasing = True
    else:
        increasing = False
    for j in range(i + 1, len(A) - 1):
        if (increasing and A[j] > A[j + 1]) or (not increasing and A[j] < A[j + 1]):
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

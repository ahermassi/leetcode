import unittest2 as unittest


def peak_index_in_mountain_array_v1(A):
    """ The mountain increases until it doesn't. The point at which it stops increasing is the peak.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    for i in range(len(A)):
        if A[i] > A[i + 1]:
            return i


def peak_index_in_mountain_array_v2(A):
    """ Recursive binary search. The idea is that 2 conditions invalidate a mountain array:
        A[peak_index - 1] > A[peak_index]
        A[peak_index + 1] > A[peak_index]
    Time complexity: O(log N)
    Space complexity: O(log N)
    """

    def find_peak_index(A, left, right):
        if left == right:
            return left
        mid = (left + right) // 2
        if A[mid - 1] > A[mid]:
            return find_peak_index(A, left, mid - 1)
        elif A[mid + 1] > A[mid]:
            return find_peak_index(A, mid + 1, right)
        return mid

    return find_peak_index(A, 0, len(A) - 1)


class Test(unittest.TestCase):
    data = [([0, 1, 0], 1),
            ([0, 2, 1, 0], 1)
            ]

    def test_peak_index_in_mountain_array_(self):
        for test_array, result in self.data:
            self.assertEqual(result, peak_index_in_mountain_array_v2(test_array))


if __name__ == '__main__':
    unittest.main()

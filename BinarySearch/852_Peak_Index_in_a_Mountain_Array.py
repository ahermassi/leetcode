import unittest2 as unittest


def peak_index_in_mountain_array_v1(A):
    """ The mountain increases until it doesn't. The point at which it stops increasing is the peak.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    for i in range(len(A)):
        if A[i] > A[i + 1]:
            return i


class Test(unittest.TestCase):
    data = [([0, 1, 0], 1),
            ([0, 2, 1, 0], 1)
            ]

    def test_two_sum(self):
        for test_array, result in self.data:
            self.assertEqual(result, peak_index_in_mountain_array_v1(test_array))


if __name__ == '__main__':
    unittest.main()

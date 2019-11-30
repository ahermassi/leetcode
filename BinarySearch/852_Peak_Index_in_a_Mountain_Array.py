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
    """ Binary Search.
        Define left and right pointers and compute mid for each iteration. When A[mid + 1]< A[mid] , indicating the
        numbers are still increasing, so the peak shall occur on the right side of mid , hence we update left pointer.
        Otherwise, it indicates peak shall occur on the left side of mid , we update the right pointer. Eventually,
        two pointers meet and the peak index is located.
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(A) - 1
    while left <= right:
        mid = (left + right) // 2
        if A[mid + 1] > A[mid]:
            left = mid + 1
        else:
            right = mid - 1
    return left


class Test(unittest.TestCase):
    data = [([0, 1, 0], 1),
            ([0, 2, 1, 0], 1)
            ]

    def test_peak_index_in_mountain_array_(self):
        for test_array, result in self.data:
            self.assertEqual(result, peak_index_in_mountain_array_v1(test_array))
            self.assertEqual(result, peak_index_in_mountain_array_v2(test_array))


if __name__ == '__main__':
    unittest.main()

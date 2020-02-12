""" Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:
Integers in each row are sorted from left to right.
The first integer of each row is greater than the last integer of the previous row. """

import unittest2 as unittest


def search_matrix(matrix, target):
    """ We could notice that the input matrix n x m could be considered as a sorted array of length n x m.
        Sorted array is a perfect candidate for the binary search because the element index in this virtual array (for
        sure we're not going to construct it for real) could be easily transformed into the row and column in the
        initial matrix.
            row = idx // m and col = idx % m
    Time complexity: O(log(mn)) = O(log(m) + log(n))
    Space complexity: O(1)
    """
    if not matrix:
        return False
    n, m = len(matrix), len(matrix[0])
    left, right = 0, n * m - 1
    while left <= right:
        mid = (left + right) // 2
        row, col = mid // m, mid % m
        if matrix[row][col] == target:
            return True
        if matrix[row][col] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False


class Test(unittest.TestCase):
    data = [([
                 [1, 3, 5, 7],
                 [10, 11, 16, 20],
                 [23, 30, 34, 50]
             ], 3, True),
        ([
             [1, 3, 5, 7],
             [10, 11, 16, 20],
             [23, 30, 34, 50]
         ], 13, False)
    ]

    def test_search_matrix(self):
        for test_matrix, test_target, result in self.data:
            self.assertEqual(result, search_matrix(test_matrix, test_target))


if __name__ == '__main__':
    unittest.main()

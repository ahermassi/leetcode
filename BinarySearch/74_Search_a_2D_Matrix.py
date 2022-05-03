""" Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:
Integers in each row are sorted from left to right.
The first integer of each row is greater than the last integer of the previous row. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=FOa55B9Ikfg

def search_matrix_v1(matrix, target):
    """ We notice that the input matrix n x m could be considered as a sorted array of length n x m.

        Sorted array is a perfect candidate for the binary search because the element index in this virtual array could
        be easily transformed into the row and column in the original matrix:

            row = idx // m
            col = idx % m

    Another way to took at it is: Let's say we have a matrix M with 4 rows and 3 columns. When we want to access
    M[2][1], the way the memory address is calculated is 2*3+1 = 7. So, we are just reversing the calculation, where row
    number is given by 7/3 = 2, and column is the offset in that row so for 7th element it is 7%3 = 1.

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

# Video explanation: https://www.youtube.com/watch?v=Ber2pi2C0j0


def search_matrix_v2(matrix, target):
    """ We can also perform two binary searches. The first binary search helps us locate the row that could contain
        the target value. The second is a regular binary search on that row to check if the target value exists.

    Time complexity: O(log(n) + log(m))
    Space complexity: O(1)
    """
    n, m = len(matrix), len(matrix[0])
    top_row, bottom_row = 0, n - 1
    while top_row <= bottom_row:
        mid_row = (top_row + bottom_row) // 2
        if target < matrix[mid_row][0]:
            bottom_row = mid_row - 1
        elif target > matrix[mid_row][-1]:
            top_row = mid_row + 1
        else:
            break
    if top_row > bottom_row:
        return False
    search_row = (top_row + bottom_row) // 2
    left, right = 0, m - 1
    while left <= right:
        mid = (left + right) // 2
        if matrix[search_row][mid] == target:
            return True
        if matrix[search_row][mid] < target:
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
            self.assertEqual(result, search_matrix_v1(test_matrix, test_target))
            self.assertEqual(result, search_matrix_v2(test_matrix, test_target))


if __name__ == '__main__':
    unittest.main()

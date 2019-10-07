""" Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:
Integers in each row are sorted in ascending from left to right.
Integers in each column are sorted in ascending from top to bottom. """

import unittest2 as unittest


def search_matrix_v1(matrix, target):
    """ We can partition a sorted two-dimensional matrix into four sorted sub matrices, two of which might contain
        target and two of which definitely do not.
        Base Case:
            For a sorted two-dimensional array, there are two ways to determine in constant time whether an arbitrary
            element target can appear in it. First, if the array has zero area, it contains no elements and therefore
            cannot contain target. Second, if target is smaller than the array's smallest element (found in the
            top-left corner) or larger than the array's largest element (found in the bottom-right corner), then it
            definitely is not present.
        Recursive Case:
            If the base case conditions have not been met, then the array has positive area and target could
            potentially be present. Therefore, we seek along the matrix's middle column for an index row such that
            matrix[row-1][mid] < target < matrix[row][mid] (obviously, if we find target during this process, we
            immediately return true). The existing matrix can be partitioned into four sub matrices around this index;
            the top-left and bottom-right sub matrices cannot contain target (via the argument outlined in Base Case
            section), so we can prune them from the search space. Additionally, the bottom-left and top-right
            submatrice are sorted two-dimensional matrices, so we can recursively apply this algorithm to them.
    Time complexity: O(N log N)
    Space complexity: O(log N), use of recursion means that we will use memory proportional to the height of its
    recursion tree. Because this approach discards half of matrix on each level of recursion (and makes two recursive
    calls), the height of the tree is bounded by logN.
    """

    def search_submatrix(left, right, up, down):
        if left > right or up > down:
            return False
        if target < matrix[up][left] or target > matrix[down][right]:  # Top-left corner element is always the
            # smallest of the matrix, and the bottom-right element is always the biggest
            return False
        mid = (left + right) // 2
        row = up
        while row <= down and matrix[row][mid] <= target:
            if matrix[row][mid] == target:
                return True
            row += 1
        return search_submatrix(left, mid - 1, row, down) or search_submatrix(mid + 1, right, up, row - 1)

    if not matrix:
        return False
    return search_submatrix(0, len(matrix[0]) - 1, 0, len(matrix) - 1)


class Test(unittest.TestCase):
    data = [([
  [1,   4,  7, 11, 15],
  [2,   5,  8, 12, 19],
  [3,   6,  9, 16, 22],
  [10, 13, 14, 17, 24],
  [18, 21, 23, 26, 30]
], 5, True),
        ([
  [1,   4,  7, 11, 15],
  [2,   5,  8, 12, 19],
  [3,   6,  9, 16, 22],
  [10, 13, 14, 17, 24],
  [18, 21, 23, 26, 30]
], 20, False)
            ]

    def test_search_matrix(self):
        for test_matrix, test_target, result in self.data:
            self.assertEqual(result, search_matrix_v1(test_matrix, test_target))


if __name__ == '__main__':
    unittest.main()
""" Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:
Integers in each row are sorted in ascending from left to right.
Integers in each column are sorted in ascending from top to bottom. """

import unittest2 as unittest


def search_matrix_v1(matrix, target):
    """ We can partition a sorted two-dimensional matrix into four sorted sub matrices, two of which might contain
         target and two of which definitely do not.

        Base Case:
            For a sorted two-dimensional array, there are two ways to determine in constant time whether an arbitrary
            target element can appear in it. First, if the array has zero area, it contains no elements and therefore
            cannot contain target. Second, if target is smaller than the array's smallest element (found in the
            top-left corner) or larger than the array's largest element (found in the bottom-right corner), then it
            definitely is not present.

        Recursive Case:
            If the base case conditions are not met, then the array has positive area and target could potentially be
            present. Therefore, we seek along the matrix's MIDDLE column for an index row such that:

                    matrix[row-1][mid] < target < matrix[row][mid]

            (obviously, if we find target during this process, we immediately return true).
            The existing matrix can be partitioned into four sub matrices around this index; the top-left and
            bottom-right sub matrices cannot contain target (via the argument outlined in the base case), so we can
            prune them from the search space. Additionally, the bottom-left and top-right sub matrices are sorted
            two-dimensional matrices, so we can recursively apply this algorithm on them.

    Time complexity: O(N logN)
    Space complexity: O(logN), use of recursion means that we will use memory proportional to the height of its
    recursion tree. Because this approach discards half of matrix on each level of recursion (and makes two recursive
    calls), the height of the tree is bounded by logN.
    """

    def search_submatrix(top, bottom, left, right):
        if top > bottom or left > right:
            return False
        if target < matrix[top][left] or target > matrix[bottom][right]:
            # Top-left corner element is always the smallest of the matrix, and the bottom-right element is always
            # the biggest
            return False
        mid = (left + right) // 2
        row = top
        # Locate a row such that matrix[row-1][mid] <= target < matrix[row][mid]
        while row <= bottom and matrix[row][mid] <= target:
            if matrix[row][mid] == target:
                return True
            row += 1
        return search_submatrix(top, row - 1, mid + 1, right) or search_submatrix(row, bottom, left, mid - 1)

    n, m = len(matrix), len(matrix[0])
    return search_submatrix(0, n - 1, 0, m - 1)


# Watch: https://youtu.be/FOa55B9Ikfg?t=945

def search_matrix_v2(matrix, target):
    """ In any search problem, the basic motive is to reduce the decision space progressively. The more aggressively
        the search space is pruned, the more efficient the algorithm.

        If we stand on the bottom-left (or top-right) corner of the matrix and look diagonally, it's kind of like a
        BST. We can go through this matrix to find the target like how we traverse the BST.

        Because the rows and columns of the matrix are sorted (from left-to-right and top-to-bottom, respectively), we
        can prune O(M) or O(N) elements when looking at any particular value.

        First, we initialize a (row, col) pointer to the bottom-left of the matrix. Then, until we find target and
        return True (or the pointer points to a (row, col) that lies outside the dimensions of the matrix), we do the
        following:

        If the currently-pointed-to value is larger than target, we can move one row up. Otherwise, if the
        currently-pointed-to value is smaller than target, we can move one column right. It is not too tricky to see
        why doing this will never prune the correct answer; because the rows are sorted from left-to-right, we know
        that every value to the right of the current value is larger. Therefore, if the current value is already larger
        than target, we know that every value to its right will also be too large. A very similar argument can be made
        for the columns, so this manner of search will always find target in the matrix (if it is present).

        To reduce decision space means to eliminate certain portion completely from search in the future. Here, due to
        the property of rows and columns being sorted, we can verify that we can use the given properties to reduce the
        search space only if we begin at bottom-left corner or top-right corner. This is because at only those two
        starting positions, we would be able to exercise decisions to reduce our decision/search space in both
        directions, i.e.:

            - If we start at bottom-left corner, we can go right to get elements in increasing order and up to get
               elements in decreasing order.
            - If we start at top-right corner, we can go left to get elements in decreasing order and down to get
               elements in increasing order.

        We can't have both choices if we start at top-left or bottom-right corners.

    Time complexity: O(N + M), the key to the time complexity analysis is noticing that, on every iteration (during
    which we do not return True), either 'row' or 'col' is decremented/incremented exactly once. Because 'row' can only
    be decremented N times and col can only be incremented M times before causing the while loop to terminate, the loop
    cannot run for more than (N + M) iterations.
    Space complexity: O(1)
    """
    if not matrix:
        return False
    n, m = len(matrix), len(matrix[0])
    row, col = n - 1, 0
    while row >= 0 and col < m:
        if matrix[row][col] == target:
            return True
        if matrix[row][col] < target:
            col += 1
        else:
            row -= 1
    return False


def search_matrix_v3(matrix, target):
    """ This time, we initiate a search from the top-right corner.
    Time complexity: O(N + M)
    Space complexity: O(1)
    """
    if not matrix:
        return False
    n, m = len(matrix), len(matrix[0])
    row, col = 0, m - 1
    while row < n and col >= 0:
        if matrix[row][col] == target:
            return True
        if matrix[row][col] < target:
            row += 1
        else:
            col -= 1
    return False


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
            self.assertEqual(result, search_matrix_v2(test_matrix, test_target))
            self.assertEqual(result, search_matrix_v3(test_matrix, test_target))


if __name__ == '__main__':
    unittest.main()

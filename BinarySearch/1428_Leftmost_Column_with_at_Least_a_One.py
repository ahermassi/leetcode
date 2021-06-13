""" A row-sorted binary matrix means that all elements are 0 or 1 and each row of the matrix is sorted in
non-decreasing order.

Given a row-sorted binary matrix binary_matrix, return the index (0-indexed) of the leftmost column with a 1 in it.
If such an index does not exist, return -1.

You can't access the Binary Matrix directly. You may only access the matrix using a BinaryMatrix interface:

BinaryMatrix.get(row, col) returns the element of the matrix at index (row, col) (0-indexed).
BinaryMatrix.dimensions() returns the dimensions of the matrix as a list of 2 elements [rows, cols], which means the
matrix is rows x cols.

Submissions making more than 1000 calls to BinaryMatrix.get will be judged Wrong Answer. Also, any solutions that
attempt to circumvent the judge will result in disqualification. """


def leftmost_column_with_one_v1(binary_matrix):
    """ Using binary search, find the index of the target element (first 1) in each row, and then return the
        minimum of those indexes. The row might be all 0's and we can detect this case by checking whether or not
        the last element in the search space is a 1.
    Time complexity: O(N * logM), where N is be the number of rows and M is the number of columns
    Space complexity: O(1)
    """

    def find_leftmost_one(i):
        if binary_matrix.get(i, m-1) == 0:  # If last element is a 0 then there is no 1 in the entire row
            return float('inf')
        left, right = 0, m - 1
        while left < right:
            mid = (left + right) // 2
            if binary_matrix.get(i, mid) == 0:
                left = mid + 1
            else:
                right = mid
        return left

    res = float('inf')
    n, m = binary_matrix.dimensions()
    for i in range(n):
        res = min(res, find_leftmost_one(i))
    return res if res != float('inf') else -1


def leftmost_column_with_one_v2(binary_matrix):
    """ Using the information that the rows are sorted, we can start searching from the right top corner
        (1st row, last column. Every time we get a 1, as the row is sorted in non-decreasing order, there is a chance
        of finding 1 in the left column with a smaller column index, so we go to previous column in the same row.
        If we get a 0, there is no chance that in this row we can find a 1, so we go to next row as we know that the
        leftmost 1 can't be to the left of this 0.
        This idea is similar to 240- Search a 2D Matrix II.
    Time complexity: O(N + M), at each step we're moving 1 step left or 1 step down. Therefore, we'll always finish
    looking at either one of the M rows or N columns. Therefore, we'll stay in the grid for at most (N + M) steps
    Space complexity: O(1)
    """
    res = float('inf')
    n, m = binary_matrix.dimensions()
    row, col = 0, m - 1
    while row < n and col >= 0:
        if binary_matrix.get(row, col) == 0:
            row += 1
        else:
            res = min(res, col)
            col -= 1
    return res if res != float('inf') else -1


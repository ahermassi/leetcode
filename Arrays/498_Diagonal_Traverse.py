""" Given a matrix of M x N elements (M rows, N columns), return all elements of the matrix in diagonal order. """

from collections import defaultdict
import unittest2 as unittest


def find_diagonal_order_v1(matrix):
    """ This approach simply and plainly does what the problem statement asks us to do. It's pure simulation. However,
        in order to implement this simulation, we need to understand the walking patterns inside the array.
        We need to figure out two things for each diagonal:
            1- The direction in which we want to process it's elements
            2- The head or the starting point for the diagonal depending upon its direction
        The slightly tricky part is figuring out the head of the next diagonal. The good part is, we already know the
        end of the previous diagonal. We can use that information to figure out the head of the next diagonal.

        Next head to go DOWN: The general rule that we will be following when we want to find the head for an
        downwards going diagonal is that:
            If the tail of the previous diagonal lies in the last column of the matrix, the head of the next diagonal
            would be the node directly BELOW the tail. (1)
            Otherwise, the head would be the node to the RIGHT of the tail of the previous diagonal. (2)

        Next head to go UP: The general rule that we will be following when we want to find the head for an upwards
        going diagonal is that:
            If the tail of the previous diagonal lies in the last row of the matrix, the head of the next diagonal
            would be the node to the RIGHT of the tail. (3)
            Otherwise, the head would be the node directly BELOW the tail of the previous diagonal. (4)

        Notice that all values in the same diagonal share the same sum (i + j). The direction of going up right or
        going down left depends whether that sum is even (going up) or odd (going down).
        For each even or odd diagonal, there are three cases:
            1- There is room to go that direction
            2- there is no row space to go further but there is col space
            3- There is no col space to go further but there is row space
    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    n, m, res = len(matrix), len(matrix[0]), []
    row = col = 0
    for _ in range(n * m):
        res.append(matrix[row][col])
        if (row + col) % 2 == 0:  # Moving up
            if col == m - 1:  # (1) For last column, go below that cell to switch direction
                row += 1
            elif row == 0:  # (2)  For first row and non-last column, go to the right of that cell to switch direction
                col += 1
            else:  # Continue moving along the up diagonal
                row -= 1
                col += 1
        else:  # Moving down
            if row == n - 1:  # (3)  For last row, go to the right of that cell to switch direction
                col += 1
            elif col == 0:  # (4)  For first column and non-last row, go below that cell to switch direction
                row += 1
            else:  # Continue moving along the down diagonal
                row += 1
                col -= 1
    return res
    # Note: we can not change the order of the if/else, i.e, if we write something like this:
    # if (i + j) % 2 == 0:  # Moving up
    #     if i == 0:
    #         j += 1
    #     elif j == m - 1:
    #         i += 1
    # There will be a situation when we are at top-right corner (j = m - 1), in which case we can only go down. Thus,
    # we have to do j == m - 1 check. Otherwise, we would have indexOutOfBound error since we can't do j += 1
    # Same reasoning for the moving down if/else (bottom-left corner)


def find_diagonal_order_v2(matrix):
    """ In this solution, we use no direction checks. The key is to realize that the sum of indices on all diagonals
        are equal (same property used in the previous algorithm).
        We can loop through the matrix, store each element by the sum of its indices in a dictionary. We end up with
        a collection of all elements on shared diagonals. The zigzag can be achieved by reversing every diagonal whose
        index is even.
        Note that this solution is possible as of Python 3.6+ where dictionaries are ordered by key insertion time.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m = len(matrix), len(matrix[0])
    res = []
    diagonals = defaultdict(list)
    for i in range(n):
        for j in range(m):
            diagonals[i + j].append(matrix[i][j])
    for s, nums in diagonals.items():
        if s % 2 == 0:
            res.extend(nums[::-1])
        else:
            res.extend(nums)
    return res


class Test(unittest.TestCase):
    data = [([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 4, 7, 5, 3, 6, 8, 9]), ([[1, 2], [3, 4]], [1, 2, 3, 4])]

    def test_find_diagonal_order(self):
        for test_matrix, result in self.data:
            self.assertEqual(result, find_diagonal_order_v1(test_matrix))
            self.assertEqual(result, find_diagonal_order_v2(test_matrix))


if __name__ == '__main__':
    unittest.main()

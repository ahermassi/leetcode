""" Given a matrix of M x N elements (M rows, N columns), return all elements of the matrix in diagonal order. """

import unittest2 as unittest


def find_diagonal_order_v1(matrix):
    """ This approach simply and plainly does what the problem statement asks us to do. It's pure simulation. However,
        in order to implement this simulation, we need to understand the walking patterns inside the array.
        We need to figure out two things for each diagonal:
            1- The direction in which we want to process it's elements
            2- The head or the starting point for the diagonal depending upon its direction
        The slightly tricky part is figuring out the head of the next diagonal. The good part is, we already know the
        end of the previous diagonal. We can use that information to figure out the head of the next diagonal.
        Next head to go DOWN: The general rule that we will be following when we want to find the head for a
        downwards going diagonal is that:
            If the tail lies in the last column of the matrix, the head would be the node directly BELOW the tail. (1)
            Otherwise, the head would be the node to the RIGHT of the tail of the previous diagonal. (2)
        Next head to go UP: The general rule that we will be following when we want to find the head for an
        upwards going diagonal is that:
            If the tail lies in the last row of the matrix, the head would be the node RIGHT next to the tail. (3)
            Otherwise, the head would be the node directly BELOW the tail of the previous diagonal. (4)
        Notice that all values in the same diagonal share the same sum (i + j). The direction of going up right or
        going down left depends whether that sum is even (going up) or odd (going down).
    Time complexity: O(N * M)
    Space complexity: O(1)
    """
    if not matrix:
        return None
    n, m, res = len(matrix), len(matrix[0]), []
    i = j = 0
    for _ in range(n * m):
        res.append(matrix[i][j])
        if (i + j) % 2 == 0:  # Moving up
            if j == m - 1:  # (1) For last column, go below that cell to switch direction
                i += 1
            elif i == 0:  # (2)  For first row and non-last column, go to the right of that cell to switch direction
                j += 1
            else:  # Continue moving along the up diagonal
                i -= 1
                j += 1
        else:  # Moving down
            if i == n - 1:  # (3)  For last row, go to the right of that cell to switch direction
                j += 1
            elif j == 0:  # (4)  For first column and non-last row, go below that cell to switch direction
                i += 1
            else:  # Continue moving along the down diagonal
                i += 1
                j -= 1
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


class Test(unittest.TestCase):
    data = [([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 4, 7, 5, 3, 6, 8, 9]), ([[1, 2], [3, 4]], [1, 2, 3, 4])]

    def test_find_diagonal_order(self):
        for test_matrix, result in self.data:
            self.assertEqual(result, find_diagonal_order_v1(test_matrix))


if __name__ == '__main__':
    unittest.main()

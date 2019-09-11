""" Given a matrix of m x n elements (m rows, n columns), return all elements of the matrix in spiral order. """

import unittest2 as unittest


def spiral_order_v1(matrix):
    """ Take the first row plus the spiral order of the rotated remaining matrix.
        Here's how the matrix changes by always extracting the first row and rotating the remaining matrix
        counter-clockwise:
        |1 2 3|      |6 9|      |8 7|      |4|  =>  |5|  =>  ||
        |4 5 6|  =>  |5 8|  =>  |5 4|  =>  |5|
        |7 8 9|      |4 7|
        Now look at the first rows we extracted:
        |1 2 3|      |6 9|      |8 7|      |4|      |5|
        Those concatenated are the desired result.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    res = []
    while matrix:
        res.extend(matrix.pop(0))
        matrix = list(zip(*matrix))[::-1]
    return res


class Test(unittest.TestCase):
    data = [([[
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ],
        [1, 2, 3, 6, 9, 8, 7, 4, 5]]),
        ([
             [1, 2, 3, 4],
             [5, 6, 7, 8],
             [9, 10, 11, 12]
         ], [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7])]

    def test_spiral_order(self):
        for test_array, result in self.data:
            self.assertEqual(result, spiral_order_v1(test_array))


if __name__ == '__main__':
    unittest.main()

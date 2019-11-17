""" Given a non-negative integer num_rows, generate the first num_rows of Pascal's triangle. """

import unittest2 as unittest


def generate(num_rows):
    """ The jth entry in the ith row is 1 if j=0 or j=i, otherwise it is the sum of (j-1)th and jth entries in the
        (i-1)th row.
    Time complexity: O(num-rows ** 2), since each element takes O(1) time to compute
    Space complexity: O(1)
    """
    pascal = [[1] * (i + 1) for i in range(num_rows)]  # Prepares num_rows rows [1], [1, 1], [1, 1, 1], etc
    for i in range(1, num_rows):
        for j in range(1, i):
            pascal[i][j] = pascal[i - 1][j - 1] + pascal[i - 1][j]  # Each number is sum of two numbers directly above
    return pascal


class Test(unittest.TestCase):
    data = [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1]
    ]

    def test_generate(self):
        self.assertEqual(self.data, generate(5))


if __name__ == '__main__':
    unittest.main()

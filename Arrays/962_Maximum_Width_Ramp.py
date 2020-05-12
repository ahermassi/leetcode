""" Given an array A of integers, a ramp is a tuple (i, j) for which i < j and A[i] <= A[j].  The width of such a ramp
is j - i.
Find the maximum width of a ramp in A.  If one doesn't exist, return 0. """

import unittest2 as unittest


def max_width_ramp_v1(A):
    """ For every index i such as A[i] = v, let's write the indices i in sorted order of their values v.
        For [7, 2, 5, 4], indices array would be [1, 3, 2, 0]. Now these indices are in increasing order of elements.
        Then, whenever we read an index i, we know there was a ramp of width (i - min(previously_read_indices)). We can
        keep track of the minimum of all indices previously read as 'min_index'.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    indices = list(range(len(A)))
    indices.sort(key=lambda i: A[i])
    min_index, res = float('inf'), 0
    for cur_index in indices:
        res = max(res, cur_index - min_index)
        min_index = min(min_index, cur_index)
    return res


class Test(unittest.TestCase):
    data = [([6, 0, 8, 2, 1, 5], 4), ([9, 8, 1, 0, 1, 9, 4, 0, 4, 1], 7)]

    def test_max_width_ramp(self):
        for test_A, result in self.data:
            self.assertEqual(result, max_width_ramp_v1(test_A))


if __name__ == '__main__':
    unittest.main()

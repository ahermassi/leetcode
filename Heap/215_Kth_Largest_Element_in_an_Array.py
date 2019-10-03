""" Find the kth largest element in an unsorted array. Note that it is the kth largest element in the sorted order,
not the kth distinct element. """

import unittest2 as unittest


def find_kth_largest_v1(nums, k):
    """ The naive solution would be to sort an array first and then return kth element from the end.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    return sorted(nums)[-k]


class Test(unittest.TestCase):
    data = [([3, 2, 1, 5, 6, 4], 2, 5), ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4)]

    def test_top_k_frequent(self):
        for test_array, test_k, result in self.data:
            self.assertEqual(result, find_kth_largest_v1(test_array, test_k))


if __name__ == '__main__':
    unittest.main()

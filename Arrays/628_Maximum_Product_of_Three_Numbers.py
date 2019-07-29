""" Given an integer array, find three numbers whose product is maximum and output the maximum product. """

import unittest2 as unittest


def maximum_product_v1(nums):
    """ Start by sorting nums. But, we can note that the product will be maximum only if all the numbers in nums
    array are positive. But, in the given problem statement, negative elements could exist as well. Thus, it could
    also be possible that two negative numbers lying at the left extreme end could also contribute to lead to a larger
    product if the third number in the triplet being considered is the largest positive number in the numsnums array.
    Time complexity: O(N log N) for Timsort
    Space complexity: O(log N) fir Timsort
    """
    nums.sort()
    return max(nums[-1] * nums[-2] * nums[-3], nums[0] * nums[1] * nums[-1])


class Test(unittest.TestCase):
    data = [([1, 2, 3], 6),
            ([1, 2, 3, 4], 24)
            ]

    def test_two_sum(self):
        for test_array, result in self.data:
            self.assertEqual(result, maximum_product_v1(test_array))


if __name__ == '__main__':
    unittest.main()

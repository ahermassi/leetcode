""" Given an integer array, find three numbers whose product is maximum and output the maximum product. """

import unittest2 as unittest


def maximum_product_v1(nums):
    """ Start by sorting nums. We can notice that the product will be maximum only if all the numbers in nums array
        are positive. But, in the given problem statement, negative elements could exist as well. Thus, it could
        also be possible that two negative numbers lying at the left extreme end could also lead to a larger product if
        the third number in the triplet being considered is the largest positive number in the nums array.
    Time complexity: O(N logN)
    Space complexity: O(N), for the sort
    """
    nums.sort()
    return max(nums[-1] * nums[-2] * nums[-3], nums[0] * nums[1] * nums[-1])


def maximum_product_v2(nums):
    """ We need not necessarily sort nums array to find the maximum product. Instead, we can only find the required 2
        smallest values (min1 and min2) and the three largest values (max1, max2, max3) in the nums array by iterating
        over the array only once. At the end, we can find out the largest value out of (min1 × min2 × max1) and
        (max1 × max2 × max3) to find the required maximum product.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    max1, max2, max3, min1, min2 = float('-inf'), float('-inf'), float('-inf'), float('inf'), float('inf')
    for num in nums:
        if num > max1:
            max1, max2, max3 = num, max1, max2
        elif num > max2:
            max2, max3 = num, max2
        elif num > max3:
            max3 = num
        if num < min1:
            min1, min2 = num, min1
        elif num < min2:
            min2 = num
    return max(min1 * min2 * max3, max1 * max2 * max3)


class Test(unittest.TestCase):
    data = [([1, 2, 3], 6),
            ([1, 2, 3, 4], 24)
            ]

    def test_maximum_product(self):
        for test_array, result in self.data:
            self.assertEqual(result, maximum_product_v1(test_array))
            self.assertEqual(result, maximum_product_v2(test_array))


if __name__ == '__main__':
    unittest.main()

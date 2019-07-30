""" Given an integer array, find three numbers whose product is maximum and output the maximum product. """

import heapq
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


def maximum_product_v2(nums):
    """ We need not necessarily sort nums array to find the maximum product. Instead, we can only find the required 2
    smallest values (min1 and min2) and the three largest values (max1, max2, max3)in the mums array,
    by iterating over the nums array only once.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    max1, max2, max3, min1, min2 = float('-Inf'), float('-Inf'), float('-Inf'), float('Inf'), float('Inf')
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


def maximum_product_v3(nums):
    """ Use heapq module to get the 2 smallest and 3 largest elements.
    Time complexity: O(N). First, k items are heapified - that's an O(k log k) operation. Then, n-k items are added
    into the heap with heapreplace - that's n-k O(log k) operations, or O((n-k) log k). Add those up, you get
    O(n log k). In this case k is constant and doesn't scale with n, so this usage is O(n).
    """
    a = heapq.nsmallest(2, nums)
    b = heapq.nlargest(3, nums)
    return max(a[0] * a[1] * b[0], b[0] * b[1] * b[2])


class Test(unittest.TestCase):
    data = [([1, 2, 3], 6),
            ([1, 2, 3, 4], 24)
            ]

    def test_two_sum(self):
        for test_array, result in self.data:
            self.assertEqual(result, maximum_product_v1(test_array))
            self.assertEqual(result, maximum_product_v2(test_array))
            self.assertEqual(result, maximum_product_v3(test_array))


if __name__ == '__main__':
    unittest.main()

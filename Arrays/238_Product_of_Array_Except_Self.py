""" Given an array nums of n integers where n > 1,  return an array output such that output[i] is equal to the
product of all the elements of nums except nums[i]. """

import unittest2 as unittest


def product_except_self_v1(nums):
    """ For every given index i, we will make use of the product of all the numbers to the left of it and multiply
    it by the product of all the numbers to the right. This will give us the product of all the numbers except the
    one at the given index i.
    Time complexity: O(N) where NN is the number of elements in the input array
    Space complexity: O(N)
    """
    a, b, output = [0] * len(nums), [0] * len(nums), [0] * len(nums)
    # For the element at index '0', there are no elements to the left, so a[0] would be 1
    # for the element at index 'length - 1', there are no elements to the right, so b[-1] would be 1
    a[0], b[-1] = 1, 1
    for i in range(1, len(nums)):
        a[i] = a[i - 1] * nums[i - 1]
    for i in reversed(range(len(nums) - 1)):
        b[i] = b[i + 1] * nums[i + 1]
    for i in range(len(nums)):
        output[i] = a[i] * b[i]
    return output


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4], [24, 12, 8, 6])]

    def test_product_except_self(self):
        for test_array, result in self.data:
            self.assertEqual(result, product_except_self_v1(test_array))


if __name__ == '__main__':
    unittest.main()

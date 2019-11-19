""" Given an array nums of n integers where n > 1,  return an array output such that output[i] is equal to the
product of all the elements of nums except nums[i]. """

import unittest2 as unittest


def product_except_self_v1(nums):
    """ For every given index i, we will make use of the product of all the numbers to the left of it and multiply
        it by the product of all the numbers to the right. This will give us the product of all the numbers except the
        one at the given index i.
    Time complexity: O(N), where N is the number of elements in the input array
    Space complexity: O(N)
    """
    n = len(nums)
    left, right = [0] * n, [0] * n
    # For the element at index 0, there are no elements to the left, so left[0] would be 1
    # For the element at index n-1, there are no elements to the right, so right[-1] would be 1
    left[0] = right[-1] = 1
    for i in range(1, n):
        left[i] = left[i - 1] * nums[i - 1]  # left[i] is the product of elements to the left of index i in nums
    for i in reversed(range(n - 1)):
        right[i] = right[i + 1] * nums[i + 1]  # right[i] is the product of elements to the right of index i in nums
    return [left[i] * right[i] for i in range(n)]


# Follow up: Could you solve it with constant space complexity? (The output array does not count as extra space for
# the purpose of space complexity analysis.)

def product_except_self_v2(nums):
    """ This approach is essentially an extension of the approach above. The only change in this approach is that we
    don't explicitly build the right (b) array from before. Instead, we simply use a variable p to keep track of the
    running product of elements to the right and we keep updating the answer array by doing a[i] = a[i] * p
    Time complexity: O(N) where NN is the number of elements in the input array
    Space complexity: O(1) since we don't use any additional array for our computations.
    """
    a = [0] * len(nums)
    a[0] = 1
    for i in range(1, len(nums)):
        a[i] = a[i - 1] * nums[i - 1]
    p = 1
    for i in reversed(range(len(nums) - 1)):
        p *= nums[i + 1]
        a[i] *= p
    return a


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4], [24, 12, 8, 6])]

    def test_product_except_self(self):
        for test_array, result in self.data:
            self.assertEqual(result, product_except_self_v1(test_array))
            self.assertEqual(result, product_except_self_v2(test_array))


if __name__ == '__main__':
    unittest.main()

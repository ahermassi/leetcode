""" Given a circular array (the next element of the last element is the first element of the array), print the Next
Greater Number for every element. The Next Greater Number of a number x is the first greater number to its
traversing-order next in the array, which means you could search circularly to find its next greater number. If it
doesn't exist, output -1 for this number. """

import unittest2 as unittest


def next_greater_elements_v1(nums):
    """ Similar to 496- Next Greater Element I.
        We can traverse circularly in the nums array by making use of the %(modulus) operator. For every element
        nums[i], we start searching in the num array(of length n) from the index ((i+1) % n) and look at the next
        (circularly) (n - 1) elements. For nums[i], we do so by scanning over nums[j], such that
        (i+1) % n ≤ j ≤ (i+n-1) % n, and we look for the first greater element found.
    Time complexity: O(N^2)
    Space complexity: O(1)
    """
    n = len(nums)
    res = [-1] * n
    for i in range(n):
        for j in range(1, n):  # We examine the remaining (n - 1) elements by wrapping around using %
            if nums[(i + j) % n] > nums[i]:
                res[i] = nums[(i + j) % n]
                break
    return res


class Test(unittest.TestCase):
    data = [([1, 2, 1], [2, -1, 2]), ([1, 1, 1, 1], [-1, -1, -1, -1])]

    def test_next_greater_elements(self):
        for test_nums, result in self.data:
            self.assertEqual(result, next_greater_elements_v1(test_nums))


if __name__ == '__main__':
    unittest.main()

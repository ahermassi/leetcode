""" Given a sorted array A of unique numbers, find the K-th missing number starting from the leftmost number of the
array. """

import unittest2 as unittest


def missing_element_v1(nums, k):
    """ Linearly scan the array and use a variable 'expected' to anticipate the next value we should encounter in the
        sorted order of elements.
            1- If the current value is different from what's expected, calculate the number of missing numbers between
               previous index and current index.
               If missing < k, update k and continue.
               Else, return previous index's value + k.
            2- Otherwise, set 'expected' to current value + 1 and continue
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, expected = len(nums), nums[0]
    for i in range(n):
        if nums[i] != expected:
            missing = nums[i] - expected
            if k > missing:
                k -= missing
            else:
                return nums[i - 1] + k
        expected = nums[i] + 1
    return nums[-1] + k


class Test(unittest.TestCase):
    data = [([4, 7, 9, 10], 1, 5), ([4, 7, 9, 10], 3, 8), ([1, 2, 4], 3, 6)]

    def test_missing_element(self):
        for test_nums, test_k, result in self.data:
            self.assertEqual(result, missing_element_v1(test_nums, test_k))


if __name__ == '__main__':
    unittest.main()

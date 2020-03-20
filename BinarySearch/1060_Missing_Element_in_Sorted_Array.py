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


def missing_element_v2(nums, k):
    """ We can replace the linear search by a binary search. The idea is to find the leftmost index such that the
        number of missing numbers until this index is smaller than or equal to k.
        Let 'missing' be the number of missing values in the entire array. Two cases need to be handled:
            1- missing < k, then return nums[-1] + k - missing
            2- missing >= k, then use binary search to find the index in the array where the kth missing number will be
               located. This index verifies:
                    nums[index] < missing number <= nums[index + 1]
               in which case return nums[index] + k
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    n = len(nums)
    missing = (nums[-1] - nums[0] + 1) - n
    if k > missing:
        k -= missing
        return nums[-1] + k
    left, right = 0, n - 1
    while left + 1 < right:  # This guarantees we stop when the interval length is 2 and 'left' is the sought index
        mid = (left + right) // 2
        missing = nums[mid] - nums[left] - (mid - left)
        # In fact, missing = number of values in the interval if no element was missing - interval length
        #                  = (nums[mid] - nums[left] + 1) - (mid - left + 1)
        #                  = nums[mid] - nums[left] - (mid - left)
        if missing < k:
            k -= missing
            left = mid
        else:
            right = mid  # When 'missing' is larger than k, then the index won't be located in [mid + 1, right]
    return nums[left] + k


class Test(unittest.TestCase):
    data = [([4, 7, 9, 10], 1, 5), ([4, 7, 9, 10], 3, 8), ([1, 2, 4], 3, 6)]

    def test_missing_element(self):
        for test_nums, test_k, result in self.data:
            self.assertEqual(result, missing_element_v1(test_nums, test_k))
            self.assertEqual(result, missing_element_v2(test_nums, test_k))


if __name__ == '__main__':
    unittest.main()

""" Given an array nums of n integers, are there elements a, b, c in nums such that a + b + c = 0? Find all unique
triplets in the array which gives the sum of zero.
Note:
The solution set must not contain duplicate triplets. """

import unittest2 as unittest


def three_sum(nums):
    """ The way to think about it is since it's 3 sum, there's only going to be 3 numbers. So to find the combinations
        of 3 numbers, we iterate over the list with the first pointer, and then try to find two extra numbers to sum
        to 0. If we sort the list, the right pointer will always be higher than the left pointer.
        We do not need to consider i after nums[i] > 0, since sum of 3 positives will be always greater than zero. [1]
        If the number is the same as the number before, then it is equivalent to repeating the previous calculation. [2]
        Now we calculate the total:
            If the total is less than zero, we need it to be larger, so we move the left pointer
            If the total is greater than zero, we need it to be smaller, so we move the right pointer
            If the total is zero, bingo! [5]
            We need to move the left and right pointers to the next different numbers, so we do not get repeating result
            [3], [4]
    Time complexity: O(N logN + (N^2)) ~= O(N^2)
    Space complexity: O(N), for the sort
    """
    nums.sort()
    n, res = len(nums), []
    for i in range(n - 2):
        if nums[i] > 0:  # [1]
            break
        if i > 0 and nums[i] == nums[i-1]:  # [2]
            continue
        left, right = i + 1, n - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                res.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]:  # [3]
                    left += 1
                while left < right and nums[right] == nums[right-1]:  # [4]
                    right -= 1
                left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return res


class Test(unittest.TestCase):
    data = [([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]])]

    def test_three_sum(self):
        for test_array, result in self.data:
            self.assertEqual(result, three_sum(test_array))


if __name__ == '__main__':
    unittest.main()

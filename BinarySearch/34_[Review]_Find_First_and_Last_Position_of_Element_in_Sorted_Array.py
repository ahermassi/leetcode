""" Given an array of integers nums sorted in ascending order, find the starting and ending position of a given target
value.
Your algorithm's runtime complexity must be in the order of O(log n).
If the target is not found in the array, return [-1, -1]. """

import unittest2 as unittest
from typing import List


def search_range(nums: List[int], target: int) -> List[int]:
    """
    Core idea
    ---------
    Treat both searches as boundary-finding problems.

    Canonical boundary search:

        F F F F T T T
                ^
            first True

    Use a half-open search interval [left, right):

        left = 0
        right = len(nums)

        while left < right:
            mid = (left + right) // 2

            if condition(mid):
                right = mid       # mid could be the first True, so keep it
            else:
                left = mid + 1    # mid is False, so eliminate it

        return left

    For the FIRST occurrence of target:
        Find the first index where nums[i] >= target.

        Example:
            nums   = [1, 2, 4, 4, 4, 7], target = 4
            >= 4   =  F  F  T  T  T  T
                           ^
                       first True

    For the LAST occurrence of target:
        Find the first index where nums[i] > target, then subtract 1.

        Example:
            nums  = [1, 2, 4, 4, 4, 7], target = 4
            > 4   =  F  F  F  F  F  T
                                    ^
                                first True

            first index > 4 = 5
            last index == 4 = 5 - 1 = 4

    Important:
    Binary search finds a BOUNDARY even when target is absent.
    Therefore, each helper verifies that its candidate actually equals target. If not, it returns -1.

    Time:  O(log n)
    Space: O(1)
    """

    def find_first_position() -> int:
        """
        Find the first index where nums[i] >= target.
        If that position actually contains target, it is the first occurrence. Otherwise, target does not exist.
        """
        left, right = 0, len(nums)

        while left < right:
            mid = (left + right) // 2

            if nums[mid] >= target:
                # mid satisfies the condition and could be the first valid position, so keep it.
                right = mid
            else:
                # nums[mid] < target, so mid cannot be the first occurrence.
                left = mid + 1

        # left may equal len(nums), so check bounds first.
        if left < len(nums) and nums[left] == target:
            return left

        return -1

    def find_last_position() -> int:
        """
        Find the first index where nums[i] > target.
        The position immediately before that boundary is the candidate for the last occurrence of target.
        """
        left, right = 0, len(nums)

        while left < right:
            mid = (left + right) // 2

            if nums[mid] > target:
                # mid could be the first element greater than target, so keep it.
                right = mid
            else:
                # nums[mid] <= target, so the boundary must be somewhere to the right of mid.
                left = mid + 1

        candidate = left - 1

        if candidate >= 0 and nums[candidate] == target:
            return candidate

        return -1

    return [find_first_position(), find_last_position()]


class Test(unittest.TestCase):
    data = [([5, 7, 7, 8, 8, 10], 8, [3, 4]), ([5, 7, 7, 8, 8, 10], 6, [-1, -1])]

    def test_search_range(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search_range(test_array, test_target))
            self.assertEqual(result, search_range(test_array, test_target))


if __name__ == '__main__':
    unittest.main()

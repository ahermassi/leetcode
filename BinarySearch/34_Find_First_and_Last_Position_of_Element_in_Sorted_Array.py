""" Given an array of integers nums sorted in ascending order, find the starting and ending position of a given target
value.
Your algorithm's runtime complexity must be in the order of O(log n).
If the target is not found in the array, return [-1, -1]. """

import unittest2 as unittest


def search_range_v1(nums, target):
    """ The problem can be simply broken down as two binary searches for the beginning and end of the range,
        respectively. The tricky part is handling left and right pointers when a match is found.
        Example:
                0  1  2  3  4  5  6  7  8  9  10 11 12
        nums = [1, 2, 2, 3, 4, 4, 5, 5, 5, 6, 7, 9, 9], target = 5

        left = 0, right = 12, mid = 6: notice here that nums[mid] == target. However, right = mid - 1. By doing that
        and narrowing down the search range, we're essentially locating the first element LESS than target, similar to
        bisect_left. When 'left' steps over 'right', nums[left] is the first occurrence of target.
        left = 0, right = 5, mid = 2
        left = 3, right = 5, mid = 4
        left = 5, right = 5, mid = 5
        left = 6, right = 5 -> return left = 6

        left = 0, right = 12, mid = 6: notice here that nums[mid] == target. However, left = mid + 1. By doing that
        and narrowing down the search range, we're essentially locating the first element GREATER than target, similar
        to bisect_right. When 'right' steps over 'left', nums[right] is the first occurrence of target.
        left = 7, right = 12, mid = 9
        left = 7, right = 8, mid = 7
        left = 8, right = 8, mid = 8
        left = 9, right = 8 -> return right = 8

    Time complexity: O(logN)
    Space complexity: O(1)
    """
    def binary_search_left():
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return left

    def binary_search_right():
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        return right

    left, right = binary_search_left(), binary_search_right()
    return [left, right] if left <= right else [-1, -1]


def search_range_v2(nums, target):
    """ The fundamental idea of binary search is to maintain a set of candidate solutions. To find the first index, if
        we see the element at index i equals 'target', although we do not know whether i is the first element equal to
        'target', we do know that no subsequent elements can be the first one. Therefore we remove all elements with
        index (i + 1) or more from the candidates.
        Let's apply the above logic to the array [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401], with target = 108.
        We start with all indices as candidates, i.e., with [0, 9].
        The midpoint index, 4 contains target. Therefore we can now update the candidate set to [0, 3], and record 4 as
        an occurrence of 'target'.
        The next midpoint is 1, and this index contains -10. We update the candidate set to [2,3].
        The value at the midpoint is 2, so we update the candidate set to [3, 3].
        Since the value at this midpoint is 108, we update the first seen occurrence of 'target' to 3.
        Now the interval is [3, 2], which is empty, terminating the search.
        The result is 3.
        Using the same logic, we can find the last occurrence index.
    Time complexity: O(logN)
    Space complexity: O(1)
    """

    def find_first_index():
        left, right, res = 0, len(nums) - 1, -1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
            if nums[mid] == target:
                res = mid
        return res

    def find_last_index():
        left, right, res = 0, len(nums) - 1, -1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
            if nums[mid] == target:
                res = mid
        return res

    return [find_first_index(), find_last_index()]


class Test(unittest.TestCase):
    data = [([5, 7, 7, 8, 8, 10], 8, [3, 4]), ([5, 7, 7, 8, 8, 10], 6, [-1, -1])]

    def test_search_range(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search_range_v1(test_array, test_target))
            self.assertEqual(result, search_range_v2(test_array, test_target))


if __name__ == '__main__':
    unittest.main()

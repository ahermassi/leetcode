""" Given an array of integers nums sorted in ascending order, find the starting and ending position of a given target
value.
Your algorithm's runtime complexity must be in the order of O(log n).
If the target is not found in the array, return [-1, -1]. """

import unittest2 as unittest


def search_range_v1(nums, target):
    """ The problem can be simply broken down into two binary searches for the beginning and end of the range,
         respectively. The tricky part is handling the left and right pointers when a match is found.

         Example:
                      0  1  2  3  4  5  6  7  8  9  10 11 12
        nums = [1, 2, 2, 3, 4, 4, 5, 5, 5, 6, 7,  9,  9], target = 5

        left = 0, right = 12, mid = 6: notice that nums[mid] == target. However, we set right = mid - 1. By doing that
        and narrowing down the search range, we're essentially locating the last/rightmost element LESS than target
        (let's call it X), similar to bisect_left. When 'left' steps over 'right', 'left' is at the index of the first
        element to the right of X, and by the definition of X that's the index of the first occurrence of target.
        left = 0, right = 5, mid = 2
        left = 3, right = 5, mid = 4
        left = 5, right = 5, mid = 5
        left = 6, right = 5 -> return left = 6

        left = 0, right = 12, mid = 6: notice that nums[mid] == target. However, we set left = mid + 1. By doing that
        and narrowing down the search range, we're essentially locating the first/leftmost element GREATER than target
        (let's call it Y), similar to bisect_right. When 'right' steps over 'left', 'right' is at the index of the first
        element to the left of Y, and by the definition of Y that's the index of the last occurrence of target.
        left = 7, right = 12, mid = 9
        left = 7, right = 8, mid = 7
        left = 8, right = 8, mid = 8
        left = 9, right = 8 -> return right = 8

    Time complexity: O(logN)
    Space complexity: O(1)
    """
    def find_first_position():
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return left

    def find_last_position():
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        return right

    left, right = find_first_position(), find_last_position()
    return [left, right] if left <= right else [-1, -1]


# Video explanation: https://youtu.be/4sQL7R5ySUU
def search_range_v2(nums, target):
    """ The fundamental idea of binary search is to maintain a set of candidate solutions. To find the first index, if
         we see the element at index i equals 'target', although we do not know whether i is the first element equal to
         'target', we do know that no subsequent element can be the first position. Therefore, we discard all elements
         beyond index (i + 1) from the set of candidates.

         Let's apply the above logic to the array [-14, -10, 2, 108, 108, 243, 285, 285, 285, 401], with target = 108.
         We start with all indices as candidates, i.e., with [0, 9].

         The mid index is 4, which contains target. Therefore, we can update the candidate set to [0, 3], and record 4
         as an occurrence of 'target'.

        The next midpoint is 1, and this index contains -10. We update the candidate set to [2,3].

        The value at the midpoint is 2, so we update the candidate set to [3, 3].

        Since the value at this midpoint is 108, we update the first seen occurrence of 'target' to 3.

        Now the interval is [3, 2], which is empty, terminating the search. The first position of target is 3.

        Using the same logic, we can find the last occurrence index.

    Time complexity: O(logN)
    Space complexity: O(1)
    """

    def find_first_position():
        left, right, index = 0, len(nums) - 1, -1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                if nums[mid] == target:
                    index = mid
        return index

    def find_last_position():
        left, right, index = 0, len(nums) - 1, -1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
                if nums[mid] == target:
                    index = mid
        return index

    return [find_first_position(), find_last_position()]


# def search_range_v3(nums, target):
#     """ We can use a single binary search helper method to find both first and last insertion positions of target.
#         Here, find_first_occurrence(target) is a simple binary search, telling the first index where we could insert a
#         number 'target' into 'nums' to keep it sorted. Thus, if 'nums' contains 'target', we can find the first
#         occurrence with find_first_occurrence(target). We do that, and if target isn't actually there, then we return
#         [-1, -1]. Otherwise, we ask find_first_occurrence(target + 1), which tells us the first index where we could
#         insert (target + 1), which of course is one index behind the last index containing target, so all we have left
#         to do is subtract 1.
#     Time complexity: O(logN)
#     Space complexity: O(1)
#     """
#
#     def find_first_occurrence(target):
#         left, right = 0, len(nums) - 1
#         while left <= right:
#             mid = (left + right) // 2
#             if nums[mid] < target:
#                 left = mid + 1
#             else:
#                 right = mid - 1
#         return left
#
#     left, right = find_first_occurrence(target), find_first_occurrence(target + 1) - 1
#     return [left, right] if left <= right else [-1, -1]


class Test(unittest.TestCase):
    data = [([5, 7, 7, 8, 8, 10], 8, [3, 4]), ([5, 7, 7, 8, 8, 10], 6, [-1, -1])]

    def test_search_range(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search_range_v1(test_array, test_target))
            self.assertEqual(result, search_range_v2(test_array, test_target))


if __name__ == '__main__':
    unittest.main()

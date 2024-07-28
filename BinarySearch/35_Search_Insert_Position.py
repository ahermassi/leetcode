""" Given a sorted array and a target value, return the index if the target is found. If not, return the index where
it would be if it were inserted in order.
You may assume no duplicates in the array. """

import unittest2 as unittest


# Video explanation: https://youtu.be/K-RYzDZkzCI
def search_insert_v1(nums, target):
    """ Based on the description of the problem, we can see that it could be a good match for binary search. Usually,
         within binary search, we compare the target value to the middle element of the array at each iteration.

            - If the target value is equal to the middle element, the job is done.
            - If the target value is less than the middle element, continue to search on the left by moving the right
               pointer: right = mid - 1.
            - If the target value is greater than the middle element, continue to search on the right by moving the
               left pointer: left = mid + 1.

        What if the target value is not found? In this case, the loop will stop when left > right and the proper
        position to insert the target is at the left index.

        Why return left? It boils down to analyzing the edge case where left == right, i.e. a one-element array.

        Example1: nums = [5], target = 3
        left = 0, right = 0, mid = 0; since target < nums[mid] --> right = mid - 1
                              [5]
                       ^      ^
                    r=-1   l=0
        left = 0 is the insertion index after which nums = [3, 5]

        Example2: nums = [5], target = 7
        left = 0, right = 0, mid = 0; since target > nums[mid] --> left = mid + 1
                              [5]
                               ^      ^
                             r=0   l=1
        left = 1 is the insertion index after which nums = [5, 7]

        In other words: in the case where we need to insert (target not found), left and right must have narrowed down
        to the same element - call it X. Following regular binary search, if we go left, meaning target is smaller than
        X, the algorithm changes right and leaves left untouched. This is desired, because left, untouched and used as
        insertion index, inserts the element to the left of X. On the other hand, if we go right, left is set to left+1,
        which indeed inserts target to the right of X.

    Time complexity: O(log N)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    # The invariant of the algorithm is: the desired index is between [left, right+1].
    # This is because if target < nums[0], the insertion index is 0; if target > nums[len(nums)-1], the insertion
    # index is len(nums)=right+1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    # (1) At this point, left > right, that is, left = right + 1
    # (2) From the invariant, we know that the index is between [left, right+1].
    # Following from (1), the index is between [left, right+1] = [left, left], which means that left is the desired
    # index. Therefore, we return left as the answer.
    return left


def search_insert_v2(nums, target):
    """ Similar to 278- First Bad Version.

         The problem can be stated as:

                Find the index of the first element greater than or equal to target

         Binary search can be used if we model the problem as a list of binary assertions (nums[index] >= target),
         resulting in a list of binary values [F, F, F, T, T], where 'F' means (nums[index] >= target == False) and 'T'
         means (nums[index] >= target == True). This list is sorted, and the problem boils down to finding the first 'T'
         assertion.

         Note that the initial range of possible indices includes len(nums) to account for the case where target is
         bigger than all the elements in nums array.

    Time complexity: O(log N)
    Space complexity: O(1)
    """
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return right
    # Contrast this to 278- First Bad Version solution.
    # left, right = 1, n
    # while left < right:
    #     mid = (left + right) // 2
    #     if not is_bad_version(mid):
    #         left = mid + 1
    #     else:
    #         right = mid
    # return right


class Test(unittest.TestCase):
    data = [([1, 3, 5, 6], 5, 2),
            ([1, 3, 5, 6], 2, 1),
            ([1, 3, 5, 6], 7, 4),
            ([1, 3, 5, 6], 0, 0)
            ]

    def test_search_insert(self):
        for test_array, target, result in self.data:
            self.assertEqual(result, search_insert_v1(test_array, target))
            self.assertEqual(result, search_insert_v2(test_array, target))


if __name__ == '__main__':
    unittest.main()

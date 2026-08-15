""" Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array
nums = [0,1,4,4,5,6,7] might become:

[4,5,6,7,0,1,4] if it was rotated 4 times.
[0,1,4,4,5,6,7] if it was rotated 7 times.
Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1],
a[2], ..., a[n-2]].

Given the sorted rotated array nums that may contain duplicates, return the minimum element of this array.

You must decrease the overall operation steps as much as possible. """

import unittest2 as unittest


def find_min(nums):
    """ LC 154 is the duplicates version of LC 153 - Find Minimum in Rotated Sorted Array.

        This uses the same boundary / candidate-convergence binary search template as LC 153.

        Why `while left < right`?

            [left, right] always contains at least one minimum.

            We are not doing an exact-match search where every remaining element
            needs to be inspected.

            Instead, we keep shrinking the candidate interval while making sure
            the minimum always remains inside it.

            Once left == right, exactly ONE candidate remains, so that index
            must contain the minimum.


        Compare nums[mid] with nums[right]:

        1- nums[mid] < nums[right]

            Example:

                [5, 6, 7, 0, 1, 2, 3]
                          M        R

            mid is already in the lower / sorted portion of the rotated array.
            Therefore, the minimum cannot be strictly to the right of mid.

            It must be either:
                - at mid
                - somewhere to the left of mid

            Since mid itself could be the minimum, we have to keep it:

                right = mid

            This follows the general binary search rule:

                If mid can still be the answer, do NOT discard it.


        2- nums[mid] > nums[right]

            Example:

                [4, 5, 6, 7, 0, 1, 2]
                          M        R

            mid is in the higher-valued portion of the array, while right is
            in the lower-valued portion.

            Therefore, the rotation point / minimum must be strictly to the
            right of mid.

            mid cannot be the minimum, so we can safely discard it:

                left = mid + 1

            This follows the general binary search rule:

                If mid definitely cannot be the answer, discard it.


        3- nums[mid] == nums[right]

            This is the only new case compared with LC 153.

            Duplicates destroy the directional information we normally get
            from comparing mid with right.

            Example:

                [2, 2, 2, 0, 1, 2]
                       M        R

            Since nums[mid] == nums[right], this comparison does not tell us
            which side contains the rotation / minimum.

            This is the same kind of ambiguity caused by duplicates in LC 81.

            However:

                nums[mid] == nums[right]

            so right is a duplicate of mid.

            Therefore, removing right cannot make us lose the minimum value:

                - If nums[right] is not the minimum, removing it is obviously safe.

                - If nums[right] IS a minimum value, nums[mid] has the same value,
                  so another copy of that minimum still remains in the search space.

            Therefore, we can safely peel one duplicate:

                right -= 1

            We cannot necessarily discard half of the array in this case because
            equality gives us no directional information.


        Relationship to LC 153:

            LC 153:

                nums[mid] < nums[right]
                    -> minimum is at mid or to the left
                    -> right = mid

                nums[mid] > nums[right]
                    -> minimum is strictly to the right
                    -> left = mid + 1

            LC 154 adds one case:

                nums[mid] == nums[right]
                    -> direction is ambiguous because of duplicates
                    -> safely remove one duplicate
                    -> right -= 1


        So LC 154 is simply:

            LC 153 boundary-search template
            +
            duplicate ambiguity from LC 81


        The recurring binary-search question is:

            "Can mid still be the answer?"

            - No:
                discard mid

            - Yes:
                keep mid

            - Cannot determine direction because of duplicates:
                safely peel a redundant duplicate and try again

    Time complexity: typical O(logN), we usually discard about half of the search space. Worst case O(N), many
    duplicates may repeatedly force us to do right -= 1 instead of discarding half of the array.
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < nums[right]:
            right = mid
        elif nums[mid] > nums[right]:
            left = mid + 1
        else:
            right -= 1
    return nums[left]


class Test(unittest.TestCase):
    data = [([3, 4, 5, 1, 2], 1), ([4, 5, 6, 7, 0, 1, 2], 0)]

    def test_find_min(self):
        for test_nums, result in self.data:
            self.assertEqual(result, find_min(test_nums))
            self.assertEqual(result, find_min(test_nums))


if __name__ == '__main__':
    unittest.main()

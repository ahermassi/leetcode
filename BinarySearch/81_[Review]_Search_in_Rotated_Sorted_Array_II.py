""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e., [0,0,1,2,2,5,6] might become [2,5,6,0,0,1,2]).
You are given a target value to search. If found in the array return true, otherwise return false.
This is a follow-up problem to Search in Rotated Sorted Array, where nums may contain duplicates. """

import unittest2 as unittest


def search(nums, target):
    """ This is the same exact-match rotated-array binary search as LC 33, with one extra case for duplicates.

        Template:
        - We are searching for an exact target, so we use `while left <= right`.
        - `[left, right]` represents the elements we still need to inspect.
        - If `left == right`, there is still one unchecked element, so we must run one more iteration.
        - We only stop when `left > right`, meaning there are no candidates left.

        At each step:

        1. Check `nums[mid]`.
           If `nums[mid] == target`, return True.

        2. Compare `nums[left]` with `nums[mid]` to determine which half is sorted.

           A) `nums[left] < nums[mid]`
              The left half is definitely sorted.

              If:
                  nums[left] <= target < nums[mid]

              then the target must be in the left half:
                  right = mid - 1

              Otherwise, discard that half:
                  left = mid + 1

           B) `nums[left] > nums[mid]`
              The rotation happened somewhere between left and mid, so the right half is definitely sorted.

              If:
                  nums[mid] < target <= nums[right]

              then the target must be in the right half:
                  left = mid + 1

              Otherwise:
                  right = mid - 1

        Why `mid +/- 1`?

        - When we move `left = mid + 1` or `right = mid - 1`, we have already
          checked `nums[mid] != target`, so mid cannot be the answer.
        - Therefore it is safe to discard mid entirely.

        3. The duplicate case: `nums[left] == nums[mid]`

           With distinct values, comparing left and mid always tells us which half is sorted.
           With duplicates, equality gives us no useful ordering information.

           For example:

               [1, 1, 1, 0, 1]
                L     M

           and:

               [1, 0, 1, 1, 1]
                L     M

           both have:
               nums[left] == nums[mid]

           but the rotation is on different sides of mid.

           Since we already checked that `nums[mid] != target`, and
           `nums[left] == nums[mid]`, we also know `nums[left] != target`.

           Therefore, `left` is safe to discard:

               left += 1

           We keep peeling duplicate values until the comparison with mid
           becomes informative again.

    Time complexity: O(logN) best case, O(N) worst case
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return True
        if nums[left] < nums[mid]:  # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        elif nums[left] > nums[mid]:  # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
        else:  # nums[left] == nums[mid]
            left += 1
    return False


class Test(unittest.TestCase):
    data = [
        ([2, 5, 6, 0, 0, 1, 2], 0, True),
        ([2, 5, 6, 0, 0, 1, 2], 3, False)
    ]

    def test_search(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search(test_array, test_target))


if __name__ == '__main__':
    unittest.main()

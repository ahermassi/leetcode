""" Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray
whose sum is greater than or equal to target. If there is no such subarray, return 0 instead. """

import unittest2 as unittest


# Refer to this thread for a summary of sliding windows techniques:
# https://leetcode.com/problems/minimum-window-substring/discuss/26808/Here-is-a-10-line-template-that-can-solve-most-'substring'-problems

# Video explanation: https://www.youtube.com/watch?v=aYqYMIqZx5s
def min_sub_array_len_v1(target, nums):
    """ Pattern: Variable-Size Sliding Window — Minimum Valid Window.

        Template:
        Expand the right boundary until the window satisfies the required condition.
        Once valid, shrink from the left while it remains valid, recording the answer
        before each shrink because we want the smallest valid window.

        For this problem, the window condition is:
            sum(window) >= target

        We maintain the sum of nums[left:right+1]. Each time right advances, we add
        nums[right]. Once the sum reaches target, the current window is a candidate.
        We then repeatedly remove nums[left] and advance left, updating the minimum
        length each time, until the sum falls below target.

        This sliding-window approach is valid because every number is positive:
        expanding the window can only increase the sum, and shrinking it can only
        decrease the sum. Therefore, the two pointers only need to move forward.

    Time complexity: O(N), each element can be visited at most twice, once by the right pointer and (at most) once by
    the left pointer.
    Space complexity: O(1)
    """
    n, res = len(nums), float('inf')
    left = right = cur_sum = 0
    while right < n:
        cur_sum += nums[right]
        while cur_sum >= target:
            res = min(res, right - left + 1)
            cur_sum -= nums[left]
            left += 1
        right += 1
    return res if res != float('inf') else 0


def min_sub_array_len_v2(target, nums):
    """ Alternative Pattern: Prefix Sum + Binary Search.

        The primary solution to this problem is the O(n) variable-size sliding-window
        template. This alternative is useful because it connects prefix sums with the
        binary-search boundary template.

        For a subarray [left:right], its sum can be computed from prefix sums. Since all
        nums are positive, the prefix sums are strictly increasing. That gives us a
        sorted/monotonic search space.

        For each right endpoint, we want the largest possible left endpoint whose
        subarray sum is still >= target, because that produces the shortest valid
        subarray ending at right. We can locate that boundary with binary search over
        the prefix sums.

        Pattern connection:
            positive nums
                -> increasing prefix sums
                -> monotonic search space
                -> binary search for a boundary

        This is slower than the sliding-window solution, so it is mainly useful as an
        example of recognizing when a prefix-sum array creates a binary-searchable
        search space.

        Let prefix[i] be the sum of nums[0:i]. Then:

        sum(nums[left:right]) = prefix[right] - prefix[left]

        For each possible 'left', we need the smallest 'right' such that:

            prefix[right] - prefix[left] >= target

        Rearranging:

            prefix[right] >= prefix[left] + target

        Since prefix is strictly increasing, this becomes a standard
        "find the first value >= target" binary search.

        The first prefix index satisfying that condition gives the shortest
        valid subarray starting at 'left'.


    Time complexity: O(N logN), the time required is O(N) for iteration over the array and O(logN) for finding the
    subarray for each index using binary search
    Space complexity: O(1)
    """

    n = len(nums)
    prefix = [0] * (n + 1)  # prefix[i] = sum of nums[0:i]
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    res = float("inf")
    for left in range(n):
        required = prefix[left] + target

        # Binary Search Template:
        # Find the first index 'right' where prefix[right] >= required.
        lo, hi = left + 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if prefix[mid] >= required:
                hi = mid
            else:
                lo = mid + 1
        if prefix[lo] >= required:
            res = min(res, lo - left)

    return 0 if res == float("inf") else res


class Test(unittest.TestCase):
    data = [(7, [2, 3, 1, 2, 4, 3], 2)]

    def test_min_sub_array_len(self):
        for test_sum, test_nums, result in self.data:
            self.assertEqual(result, min_sub_array_len_v1(test_sum, test_nums))
            self.assertEqual(result, min_sub_array_len_v2(test_sum, test_nums))


if __name__ == '__main__':
    unittest.main()

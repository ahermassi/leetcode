""" Given an array A of 0s and 1s, we may change up to K values from 0 to 1.
Return the length of the longest (contiguous) sub-array that contains only 1s. """

import unittest2 as unittest


def longest_ones_v1(nums, k):
    """ Pattern: Variable-Size Sliding Window — Longest Valid Window.

        General template:
            1. Expand the right boundary and update the window state.
            2. If the window becomes invalid, shrink from the left until the invariant
               is restored.
            3. Once valid again, update the maximum window length.

        For this problem, a window is valid if it contains at most k zeros, since those
        are exactly the elements we are allowed to flip to 1.

        Instead of counting zeros separately, we reuse k as the number of flips still
        available in the current window. When nums[right] is 0, we consume one flip:

            k -= 1

        If k becomes negative, the window contains too many zeros and is invalid.
        We then move left forward until a zero leaves the window, restoring one flip
        and making the window valid again.

        Once the shrinking loop finishes, nums[left:right+1] is the longest valid
        window ending at right, so we update the global maximum.

        This is the same longest-valid-window template as problems such as longest
        substring without repeating characters; only the validity condition changes:

            LC 3:    no duplicate characters
            LC 1004: at most k zeros

        Each element enters the window once and leaves it at most once.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, res = len(nums), 0
    left = right = 0
    while right < n:
        if nums[right] == 0:
            k -= 1
        while k < 0:
            # A negative k denotes we have consumed all allowed flips and the window has more than allowed zeros.
            # We need to advance the left pointer until the current window is valid again.
            if nums[left] == 0:
                k += 1
            left += 1
        res = max(res, right - left + 1)
        right += 1
    return res


def longest_ones_v2(nums, k):
    """ Pattern: Variable-Size Sliding Window — Longest Valid Window
        Optimization: Non-shrinking / monotonically growing window size.

        Start from the standard longest-valid-window template:

            expand right
            -> if the window becomes invalid, shrink left until valid again
            -> update the maximum valid length

        This version uses an additional observation specific to finding a MAXIMUM
        window length:

            Once we have already found a valid window of length L, we never care
            about constructing a valid window shorter than L again. Future work only
            needs to determine whether a window of length L + 1 (and later larger)
            is possible.

        The current window width therefore acts as the best length found so far.

        Each time right advances, the window temporarily grows by 1:
            - If it is valid, we have found a larger valid window, so we keep the
              increased size.
            - If it is invalid (k < 0), we advance left exactly once. Since right
              also advanced once, the window returns to its previous size instead
              of shrinking further.

        Unlike the standard sliding-window template, we do NOT require the carried
        window to always be valid. After shifting left once, it may still contain
        too many zeros. That is okay: we already know that its SIZE is achievable
        from an earlier valid window, so there is no reason to shrink below it.

        As right continues advancing, an invalid carried window shifts forward at
        the same size until enough zeros leave from the left. Once the constraint is
        restored, a future right expansion can increase the window size again.

        Thus, the window size never decreases:
            - left and right move together -> keep the current best size
            - only right moves            -> a larger valid size was found

        At the end, right - left represents the largest valid window SIZE found,
        even though [left, right) does not necessarily represent the actual longest
        valid window.

        This is an optimization of the standard longest-valid-window template, not
        a separate core template.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    left = right = 0
    while right < n:
        if nums[right] == 0:
            k -= 1
        if k < 0:
            # A negative k denotes we have consumed all allowed flips and the window more zeros than allowed, so
            # increment left pointer by 1 to maintain the window size.
            if nums[left] == 0:
                # If the left element to be thrown out is zero, we increment k
                k += 1
            # Regardless of whether we had a 1 or a 0 we can move left side by 1. If we keep seeing 1's, the
            # window still keeps moving as-is
            left += 1
        right += 1
    return right - left  # Not (right - left + 1) because 'right' is already outside the window


class Test(unittest.TestCase):
    data = [([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2, 6),
            ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3, 10)]

    def test_longest_ones(self):
        for test_A, test_K, result in self.data:
            self.assertEqual(result, longest_ones_v1(test_A, test_K))
            self.assertEqual(result, longest_ones_v2(test_A, test_K))


if __name__ == '__main__':
    unittest.main()

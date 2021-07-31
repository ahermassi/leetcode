""" Given an array A of 0s and 1s, we may change up to K values from 0 to 1.
Return the length of the longest (contiguous) sub-array that contains only 1s. """

import unittest2 as unittest


def longest_ones_v1(nums, K):
    """ We can use a simple sliding window approach to solve this problem. The solution is pretty intuitive. We keep
        expanding the window by moving the right pointer. When the window has reached the limit of 0's allowed, we
        contract (if possible) and save the longest window till now. The answer is the longest desirable window.
        Initialize two pointers. The two pointers help us to mark the left and right end of the window/sub-array with
        contiguous 1's.
        We use the right pointer to expand the window until the window/sub-array is desirable. i.e. number of 0's in
        the window are in the allowed range of [0, K].
        Once we have a window which has more than the allowed number of 0's, we can move the left pointer ahead one by
        one until we encounter 0 on the left too. This step ensures we are throwing out the extra zero.
        Note that using a 'while' loop means we always have a valid window, not only a window whose size is equal to
        the maximum size of a valid window.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, res = len(nums), 0
    left = right = 0
    while right < n:
        if nums[right] == 0:
            K -= 1  # If we include a zero in the window we reduce the value of K since K is the maximum zeros allowed
            # in a window.
        while K < 0:  # A negative K denotes we have consumed all allowed flips and window has more than allowed zeros.
            # We need to advance the left pointer until the current window is valid
            if nums[left] == 0:  # If the left element to be thrown out is zero we increase K
                K += 1
            left += 1
        res = max(res, right - left + 1)
        right += 1
    return res


def longest_ones_v2(nums, K):
    """ Same algorithm, but we can solve this problem a little efficiently. Since we have to find the MAXIMUM window
        (in terms of size), we never reduce the size of the window. We either increase the size of the window or keep
        it the same but never reduce the size. If the limit of zeros is reached, we contract only by one, thus we keep
        the window size the same.
        Take A = [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], K = 3 for example.
        We know the answer is 10 with sub-array from A[2] to A[11].
        Through the iteration, this sub-array would be found while right = 11 and left = 2.
        What happens next ?
        As we keep advancing 'right', we will find out that 'left' and 'right' keep adding 1 in every iteration, which
        makes the distance between 'left' and 'right' the same (and is the CURRENT best).
        The distance between 'left' and 'right' would change again if a longer sub-array exists. So in short:

            We are looking for a bigger window size. When we find one, we use this window to iterate till we find a
            larger one (if any). Increasing 'left' and 'right' by 1 allows the distance between 'left' and 'right' for
            the currently best found window to be preserved. Later on, only 'right' will expand if longer sub-array is
            found.
        So it's crucial to realize that this code does NOT find the max VALID window but rather the maximum size of a
        valid window (this size is preserved when 'left' and 'right' move forward together). So when the loop exits,
        'left' and 'right' do NOT represent the actual indexes of the longest VALID window.
        Example: nums = [1, 1, 1, 0, 0, 0, 0, 0], K = 2 . The maximum window's SIZE will get carried through until the
        loop terminates with right == 7 and left == 3.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    left = right = 0
    while right < n:
        if nums[right] == 0:
            K -= 1
        if K < 0:  # A negative K denotes we have consumed all allowed flips and window has more than allowed zeros,
            # thus increment left pointer by 1 to keep the window size same.
            if nums[left] == 0:  # If the left element to be thrown out is zero we increase K
                K += 1
            left += 1  # Regardless of whether we had a 1 or a 0 we can move left side by 1. If we keep seeing 1's, the
            # window still keeps moving as-is
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

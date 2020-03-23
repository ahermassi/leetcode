""" Given an array A of 0s and 1s, we may change up to K values from 0 to 1.
Return the length of the longest (contiguous) sub-array that contains only 1s. """

import unittest2 as unittest


def longest_ones_v1(A, K):
    """ We can use a simple sliding window approach to solve this problem. The solution is pretty intuitive. We keep
        expanding the window by moving the right pointer. When the window has reached the limit of 0's allowed, we
        contract (if possible) and save the longest window till now. The answer is the longest desirable window.
        Initialize two pointers. The two pointers help us to mark the left and right end of the window/sub-array with
        contiguous 1's.
        We use the right pointer to expand the window until the window/sub-array is desirable. i.e. number of 0's in
        the window are in the allowed range of [0, K].
        Once we have a window which has more than the allowed number of 0's, we can move the left pointer ahead one by
        one until we encounter 0 on the left too. This step ensures we are throwing out the extra zero.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, res = len(A), 0
    left = 0
    for right in range(n):
        if A[right] == 0:
            K -= 1  # If we include a zero in the window we reduce the value of K since K is the maximum zeros allowed
            # in a window.
        while K < 0:  # A negative K denotes we have consumed all allowed flips and window has more than allowed zeros.
            # We need to advance the left pointer until the current window is valid
            if A[left] == 0:  # If the left element to be thrown out is zero we increase K
                K += 1
            left += 1
        res = max(res, right - left + 1)
    return res


class Test(unittest.TestCase):
    data = [([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2, 6),
            ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3, 10)]

    def test_longest_ones(self):
        for test_A, test_K, result in self.data:
            self.assertEqual(result, longest_ones_v1(test_A, test_K))


if __name__ == '__main__':
    unittest.main()

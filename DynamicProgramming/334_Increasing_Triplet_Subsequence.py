""" Given an unsorted array return whether an increasing subsequence of length 3 exists or not in the array. """

import bisect
import unittest2 as unittest


def increasing_triplet_v1(nums):
    """ The main idea is to keep two values when checking all elements in the array: the minimum value until now
        'first_min' and the second minimum value 'second_min' from the minimum value's position until now. Then if we
        can find a third value that is larger than those two values at the same time, an increasing triplet
        sub-sequence must exist and we return true.
        first_min = so far best candidate of end element of a one-cell sub-sequence to form a triplet sub-sequence.
        second_min = so far best candidate of end element of a two-cell sub-sequence to form a triplet sub-sequence.
        'second_min' is the smallest value that has something before it that is even smaller, which is 'first_min'.
        Scanning from left to right, the numbers could lie in range [-----] for any first_min < second_min < third_value
            -----first_min< -----second_min< -----third_value
            a) If num is less than first_min: update first_min to num.
               Now the range for second_min can expand between new first_min and second_min (larger range)
            b) If num is between first_min and second_min and less than second_min: update second_min to num.
               Now the range for third_value can be any number greater than second_min (larger range)
            c) if num is greater than second_min: we've found 3 an increasing triplet sub-sequence and return true
        It's worth pointing out that the algorithm is similar to keeping an array 'increasing_sub_sequence' of size 3
        and updating first_min and second_min just like 300- Longest Increasing Sub-sequence's binary search solution.
        That algorithm's time complexity is O(N logK), where K is the length of the LIS. Here, K is no larger than 2,
        then O(N log2) ~= O(N).
        However, 'increasing_sub_sequence' here contains at most 2 elements, so one instant simplification is to
        replace the binary search or bisect.bisect_left() call with a simple if-else comparison.
        Example: nums = [9, 7, 10, 1, 8, 9], let sub = [first_min, second_min] = [float('inf), float('inf')]
        i = 0:    sub = [9, max]
        i = 1:    sub = [7, max]
        i = 2:    sub = [7, 10]
        i = 3:    sub = [1, 10]
        i = 4:    sub = [1, 8];
        i = 5:    sub[1] < 9, done.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    first_min = second_min = float('inf')
    for num in nums:
        if num <= first_min:
            first_min = num  # first_min = min so far
        elif num <= second_min:
            second_min = num  # second_min = min element **with a smaller element to the left**
        else:
            return True
    return False


def increasing_triplet_v2(nums):
    """ Using binary search as in 300- Longest Increasing Sub-sequence. This algorithm is still O(N), for the simple
    fact that the binary search is done over an array that has a constant size of 2, so the binary search is O(lg 2)
    which is constant, so O(1).
    Time complexity: O(N log2) ~= O(N)
    Space complexity: O(1)
    """
    increasing_sub_sequence = [float('inf')] * 2
    for num in nums:
        index = bisect.bisect_left(increasing_sub_sequence, num)
        if index >= 2:
            return True
        increasing_sub_sequence[index] = num
    return False


def increasing_k_subsequence(nums, k):
    """ Generalization for any k >= 0
    Time complexity: O(N logK)
    Space complexity: O(1)
    """
    increasing_sub_sequence = [float('inf')] * (k - 1)
    for num in nums:
        index = bisect.bisect_left(increasing_sub_sequence, num)
        if index >= k - 1:
            return True
        increasing_sub_sequence[index] = num
    return False


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5], True), ([5, 4, 3, 2, 1], False)]

    def test_increasing_triplet(self):
        for test_nums, result in self.data:
            self.assertEqual(result, increasing_triplet_v1(test_nums))
            self.assertEqual(result, increasing_triplet_v2(test_nums))
            self.assertEqual(result, increasing_k_subsequence(test_nums, 3))


if __name__ == '__main__':
    unittest.main()


""" Given a binary array, find the maximum length of a contiguous sub-array with equal number of 0 and 1. """

import unittest2 as unittest


def find_max_length(nums):
    """ The idea is inspired by 560- Sub array Sum Equals K.
        Let's have a variable 'acc' initially set to 0 and traverse through nums. Every time we meet a 0, we decrease
        'acc' by 1, and increase 'acc' by 1 when we meet 1. It's pretty easy to conclude that we have a contiguous
        sub-array with equal number of 0 and 1 when 'acc' equals 0.
        What if we have a sequence [0, 0, 0, 0, 1, 1]? The maximum length is 4, the count starting from 0 will equal
        -1, -2, -3, -4, -3, -2, and won't go back to 0 again. But wait, the longest sub-array with equal number of 0
        and 1 started and ended when count equals -2. We can easily understand that two points with the same count
        value indicates the sequence between these two points has equal number of 0 and 1.
        To find the maximum length, we need a hash map to store the value of 'acc' (as the key) and its associated
        index (as the value). We only need to save an 'acc' value and its index the first time, and when the same
        'acc' values appear again, we use the new index subtracting the old index to calculate the length of sub-array.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    prefix_sum = {0: -1}  # It means the sum is 0 initially, and because we haven't started looping, index = -1. This
    # initialization is necessary for the case when the whole array is a contiguous sub-array with equal 0s and 1s.
    # Example: nums = [0, 1], when i = 1, acc = -1 + 1 = 0, the length is i - (-1) = 1- (-1) = 2, so {0: -1} is needed.
    acc, res = 0, 0
    for i, num in enumerate(nums):
        acc += 1 if num else -1
        if acc in prefix_sum:
            res = max(res, i - prefix_sum[acc])
        else:
            prefix_sum[acc] = i
    return res


class Test(unittest.TestCase):
    data = [([0, 1], 2), ([0, 1, 0], 2)]

    def test_find_max_length(self):
        for test_nums, result in self.data:
            self.assertEqual(result, find_max_length(test_nums))


if __name__ == '__main__':
    unittest.main()


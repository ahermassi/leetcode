""" Given a binary array, find the maximum length of a contiguous sub-array with equal number of 0 and 1. """

import unittest2 as unittest


def find_max_length(nums):
    """ The idea is inspired from 560- Sub array Sum Equals K.
        We make use of a 'count' variable, which is used to store the relative number of ones and zeros encountered so
        far while traversing the array. The 'count' variable is incremented by one for every 1 encountered and the same
        is decremented by one for every 0 encountered.
        We start traversing the array from the beginning. If at any moment the 'count' becomes zero, it implies that
        we've encountered an equal number of zeros and ones from the beginning till the current index of the array i.
        Not only this, another point to be noted is that if we encounter the same 'count' twice while traversing the
        array, it means that the number of zeros and ones are equal between the indices corresponding to the equal
        'count' values. In other words, if we get the same sum value for two indices i and j, then all the elements
        within the range [i,j) or (i,j] have been neutralized.
        Thus, if we keep track of the indices corresponding to the same 'count' values that lie
        farthest apart, we can determine the size of the largest sub-array with equal number of zeros and ones easily.
        We use a hash map to store the entries in the form of (count, index). We make an entry for a 'count' in the
        map whenever the 'count' is encountered first, and later on use the corresponding index to find the length of
        the largest sub-array with equal number of zeros and ones when the same 'count' is encountered again.
        Example:
        What if we have a sequence [0, 0, 0, 0, 1, 1]? The maximum length is 4, the count starting from 0 will be equal
        -1, -2, -3, -4, -3, -2, and won't go back to 0 again. But wait, the longest sub-array with equal number of 0
        and 1 started and ended when count equals -2. We can easily understand that two points with the same count
        value indicates the sequence between these two points has equal number of 0 and 1.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    prefix_sum = {0: -1}  # It means the sum is 0 initially, and because we haven't started looping, index = -1. This
    # initialization is necessary for the case when the whole array is a contiguous sub-array with equal 0s and 1s.
    # Example: nums = [0, 1], when i=1, count = -1 + 1 = 0, the length is i - (-1) = 1- (-1) = 2, so {0: -1} is needed.
    # So {0: -1}  means that, before we loop the array, the sum is 0 initially and, because we haven't started the
    # loop, the index = -1.
    count, res = 0, 0
    for i, num in enumerate(nums):
        count += 1 if num else -1
        if count in prefix_sum:
            res = max(res, i - prefix_sum[count])
        else:
            prefix_sum[count] = i
    return res


class Test(unittest.TestCase):
    data = [([0, 1], 2), ([0, 1, 0], 2)]

    def test_find_max_length(self):
        for test_nums, result in self.data:
            self.assertEqual(result, find_max_length(test_nums))


if __name__ == '__main__':
    unittest.main()


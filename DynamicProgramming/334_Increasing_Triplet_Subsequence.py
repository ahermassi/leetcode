""" Given an unsorted array return whether an increasing subsequence of length 3 exists or not in the array. """

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
        It's worth pointing out that the algorithm is similar to keeping an array of size=3 and updating first_min and
        second_min just like 300- Longest Increasing Sub-sequence's binary search solution. Since we know the desired
        length of the array is 3, we do not need to use binary search to find the insertion index, so we can do it in
        constant time.

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


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5], True), ([5, 4, 3, 2, 1], False)]

    def test_increasing_triplet(self):
        for test_nums, result in self.data:
            self.assertEqual(result, increasing_triplet_v1(test_nums))


if __name__ == '__main__':
    unittest.main()

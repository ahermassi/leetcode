import unittest2 as unittest

""" Given an array of 2n integers, group these integers into n pairs of integer, say (a1, b1), (a2, b2), ..., (an,
bn) which makes sum of min(ai, bi) for all i from 1 to n as large as possible. """


def array_pair_sum(nums):
    """ Consider the smallest element x. It should be paired with the next smallest element, because min(x,
    anything) = x, and having bigger elements only helps you have a larger score. Thus, we should pair adjacent
    elements together in the sorted array.
    Time complexity: O(N log N) for Timsort
    Space complexity: O(1)
    """
    nums.sort()
    sum = 0
    for i in range(0, len(nums), 2):
        sum += nums[i]
    return sum
    # Can be rewritten to: return sum(sorted(nums)[::2]) which sorts the array and sums every other element


class Test(unittest.TestCase):
    data = [3, 2, 4, 1]

    def test_array_pair(self):
        self.assertEqual(4, array_pair_sum(self.data))


if __name__ == '__main__':
    unittest.main()

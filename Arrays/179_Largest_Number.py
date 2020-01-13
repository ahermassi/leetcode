""" Given a list of non negative integers, arrange them such that they form the largest number.
The result may be very large, so you need to return a string instead of an integer.
"""

import unittest2 as unittest


class CompareStrings(str):
    def __lt__(self, other):  # In python3, sort uses lt by default. If we don't override it, it will use the default lt
        return self + other < other + self


def largest_number(nums):
    """ To construct the largest number, we want to ensure that the most significant digits are occupied by the largest
        digits.
        First, we convert each integer to a string. Then, we sort the array of strings.
        For each pairwise comparison during the sort, we compare the numbers achieved by concatenating the pair in both
        orders.
        When we have 2 numbers (let's convert them into string), we'll face only 2 cases. For example:
        a = '9', b = '31'
        case1 =  a + b = '931'
        case2 = b + a = '319'
        Apparently, case1 is greater than case2 in terms of value. So, we should always put a in front of b.
        We can prove that this sorts into the proper order as follows:
        Assume that (without loss of generality), for some pair of integers a and b, our comparator dictates that a
        should precede b in sorted order. This means that a⌢b > b⌢a (where ⌢ represents concatenation). For the sort
        to produce an incorrect ordering, there must be some c for which b precedes c and cc precedes a. This is a
        contradiction because a⌢b > b⌢a and b⌢c > c⌢b implies a⌢c > c⌢a. In other words, our custom comparator
        preserves transitivity, so the sort is correct.
        Once the array is sorted, the most 'significant' number will be at the front. There is a minor edge case that
        comes up when the array consists of only zeroes, so if the most significant number is 0, we can simply
        return 0. Otherwise, we build a string out of the sorted array and return it.
    Time complexity: O(N logN), where N is the length of nums. Let K be the max length of a string, then comparing two
    strings will take O(K) and sorting will take O(N logN). Therefore, the overall runtime is dominated by the
    complexity of sort.
    Space complexity: O(N), we allocate O(N) additional space to store the sorted nums
    """
    nums = sorted(map(str, nums), key=CompareStrings, reverse=True)
    return ''.join(nums) if nums[0] != '0' else '0'


class Test(unittest.TestCase):
    data = [([10, 2], '210'), ([3, 30, 34, 5, 9], '9534330')]

    def test_largest_number(self):
        for test_nums, result in self.data:
            self.assertEqual(result, largest_number(test_nums))


if __name__ == '__main__':
    unittest.main()

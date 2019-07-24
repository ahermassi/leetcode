""" Given a non-empty array of integers, every element appears twice except for one. Find that single one.
Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory
"""

import unittest2 as unittest


def single_number_v1(nums):
    """ Iterate through all elements in nums. Try if hash table has the key for pop. If not, set up key/value pair.
    In the end, there is only one element in hash table, so use popitem to get it.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    count = {}
    for i in nums:
        try:
            count.pop(i)
        except KeyError:
            count[i] = 1
    return count.popitem()[0]


class Test(unittest.TestCase):
    data = [([2, 2, 1], 1), ([4, 1, 2, 1, 2], 4)]

    def test_single_number_v1(self):
        for test_array, result in self.data:
            self.assertEqual(result, single_number_v1(test_array))


if __name__ == '__main__':
    unittest.main()

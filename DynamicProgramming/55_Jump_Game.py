""" Given an array of non-negative integers, you are initially positioned at the first index of the array.
Each element in the array represents your maximum jump length at that position.
Determine if you are able to reach the last index. """

import unittest2 as unittest


def can_jump_v1(nums):
    """ Idea is to work backwards from the last index. Keep track of the smallest index 'last_pos' that can "jump" to
        the last index. Check whether the current index i can jump to this smallest index.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    last_pos = n - 1
    for i in reversed(range(n)):
        if i + nums[i] >= last_pos:
            last_pos = i
    return last_pos == 0


class Test(unittest.TestCase):
    data = [([2, 3, 1, 1, 4], True), ([3, 2, 1, 0, 4], False)]

    def test_can_jump(self):
        for test_array, result in self.data:
            self.assertEqual(result, can_jump_v1(test_array))


if __name__ == '__main__':
    unittest.main()

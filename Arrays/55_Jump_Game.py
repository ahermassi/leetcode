""" Given an array of non-negative integers, you are initially positioned at the first index of the array.
Each element in the array represents your maximum jump length at that position.
Determine if you are able to reach the last index. """

import unittest2 as unittest


def can_jump_v1(nums):
    """ The idea is to work backwards from the last index and keep track of the smallest index 'last_pos' that can jump
        to the last index. Check whether the current index i can jump to this smallest index.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    last_pos = n - 1  # (last_pos = i) means 'from index i, we can jump and reach the end of array'
    for i in reversed(range(n-1)):
        if i + nums[i] >= last_pos:  # If I can jump to last_pos, I'm going to be the new last_pos
            last_pos = i
    return last_pos == 0  # This means from index 0 we can jump and reach the end of array


def can_jump_v2(nums):
    """ We want to know whether we can reach the end from the starting index. 'farthest_reach' variable indicates the
        farthest position that can be reached from any index i, initialized to 0. As we iterate through the array, we
        track the farthest index we know we can advance to. The farthest we can advance from index i is (i + nums[i]).
        As soon as 'farthest_reach' is greater than or equal to the last index, we know we can reach the last position.
        If at any moment we arrive at an index that is strictly greater than 'farthest_reach', we return False.
        Otherwise, we update 'farthest_reach' to the maximum between 'farthest_reach' and (i + nums[i]) which indicates
        the farthest index that the can be reached from the current position.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    farthest_reach, last_index = 0, len(nums) - 1
    for i, v in enumerate(nums):
        if farthest_reach < i:  # If previous farthest_reach is smaller than i, it means we cannot reach location i,
            # thus return false.
            return False
        if farthest_reach >= last_index:
            return True
        farthest_reach = max(farthest_reach, i + v)


class Test(unittest.TestCase):
    data = [([2, 3, 1, 1, 4], True), ([3, 2, 1, 0, 4], False)]

    def test_can_jump(self):
        for test_array, result in self.data:
            self.assertEqual(result, can_jump_v1(test_array))
            self.assertEqual(result, can_jump_v2(test_array))


if __name__ == '__main__':
    unittest.main()

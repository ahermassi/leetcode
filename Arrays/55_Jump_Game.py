""" Given an array of non-negative integers, you are initially positioned at the first index of the array.
Each element in the array represents your maximum jump length at that position.
Determine if you are able to reach the last index. """

import unittest2 as unittest


def can_jump_v1(nums):
    """ We want to know whether we can reach the end from the starting index. 'farthest_reachable_index' indicates the
         farthest position that can be reached from any index i, initialized to 0.

         As we iterate over the array, we track the farthest index we know we can advance to. The farthest we can
         reach from index i is (i + nums[i]). As soon as 'farthest_reachable_index' is greater than or equal to the
          last index, we know we can reach the last position.

         If at any moment we arrive at an index that is strictly greater than 'farthest_reachable_index', i.e. that is
         not reachable, we return False. Otherwise, we update 'farthest_reachable_index' to the maximum between
         'farthest_reachable_index' and (i + nums[i]) which indicates the farthest index that can be reached from the
         current position.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    farthest_reachable_index, last_index = 0, len(nums) - 1
    for i, num in enumerate(nums):
        # If i falls beyond farthest_reachable_index, it means we cannot reach index i, thus return false.
        if i > farthest_reachable_index:
            return False
        if farthest_reachable_index >= last_index:
            return True
        farthest_reachable_index = max(farthest_reachable_index, i + num)


# Video explanation: https://www.youtube.com/watch?v=Yan0cv2cLy8
def can_jump_v2(nums):
    """ We call a position in the array a 'good index' if starting at that position, we can reach the last index.
         Otherwise, that index is called a 'bad index'. The problem then reduces to whether or not index 0 is a
         'good index'.

        The idea is to work backwards from the last index and keep track of the smallest 'last_good_index' that can
        jump to the last index. At each iteration, we check whether the current index can jump to this smallest index.

        Iterating right-to-left, for each position we check if there is a potential jump that reaches a 'good' index
        (currPosition + nums[currPosition] >= last_good_index). If we can reach a 'good' index, then our position is
        itself 'good'. Also, this new 'good' position will be the new leftmost 'good' index. Iteration continues until
        the beginning of the array.

        If index 0 is a 'good' index, then we can reach the last index from the first position.

        Thinking process:

        Last index can trivially reach to last index. How can we reach the last index (we will call it last_position)
        from a preceding index?
        If we have a preceding index i in nums which has jump count nums[i] which satisfies i+nums[i] >= last_position,
        we know that index i is good enough to be treated as the last index because all we need to do now is to get to
        index i. So, we're going to treat this index as a new last_position.

        If we have indices which are like sinkholes, those with 0 as jump and every other preceding index can only jump
        to that sinkhole, our last_position will not be updated anymore because i+nums[i] >= last_position will not be
        satisfied at that sinkhole and every other preceding index cannot satisfy the condition since their jumps are
        not big enough.

        If we have barriers, those indices with 0 as jump, but the preceding indices contain jumps which can go beyond
        those barriers, i+nums[i] >= last_position will be satisfied and last_position will be updated.
        E.g. nums=[3,2,2,0,4] # Here 0 is just a barrier since the index before that 0 can jump *over* that barrier.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    last_good_index = n - 1  # (last_good_index = i) means 'from index i, we can jump and reach the end of array'
    for i in reversed(range(n)):
        if i + nums[i] >= last_good_index:
            # If I can jump to last_good_index, I'm going to be the new last_good_index
            last_good_index = i
    return last_good_index == 0  # This means from index 0 we can jump and reach the end of the array


def can_jump_v3(nums):
    """ Backtracking (brute force) for the sake of completeness. TLE.

        This is the inefficient solution where we try every single jump pattern that takes us from the first position to
        the last. We start from the first position and jump to every index that is reachable. We repeat the process
        until last index is reached. When stuck, backtrack.

        We can add memoization (cache results based on indices) to this solution to become Top-Down Dynamic Programming.

    Time complexity: O(N^N)
    Space complexity: O(N), recursion requires additional memory for the stack frames
    """

    def dfs(index):
        if index >= n - 1:
            return True
        farthest_reach = index + nums[index]
        for i in range(index + 1, farthest_reach + 1):
            if dfs(i):
                return True
        return False

    n = len(nums)
    return dfs(0)


class Test(unittest.TestCase):
    data = [([2, 3, 1, 1, 4], True), ([3, 2, 1, 0, 4], False)]

    def test_can_jump(self):
        for test_array, result in self.data:
            self.assertEqual(result, can_jump_v1(test_array))
            self.assertEqual(result, can_jump_v2(test_array))
            self.assertEqual(result, can_jump_v3(test_array))


if __name__ == '__main__':
    unittest.main()

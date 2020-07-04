""" Given an unsorted array of integers, find the length of the longest consecutive elements sequence.
Your algorithm should run in O(n) complexity. """

import unittest2 as unittest


def longest_consecutive_v1(nums):
    """ Because a sequence could start at any number in nums, we can exhaust the entire search space by building as
        long a sequence as possible from every number.
        First, turn the input into a set of numbers. Then, go through the numbers. If the number 'num' is the start of
        a streak (i.e., num-1 is not in the set), then test next_num = num+1, num+2, num+3, ... and stop at the first
        number not in the set. The length of the streak is then simply (next_num - num), and we update our global best
        with that.
        Intuition: We only attempt to build sequences from numbers that are not already part of a longer sequence.
        This is accomplished by first ensuring that the number that would immediately precede the current number in a
        sequence is not present, as that number would necessarily be part of a longer sequence.
    Time complexity: O(N), although the time complexity appears to be quadratic due to the while loop nested within the
    for loop, closer inspection reveals it to be linear. Because the while loop is reached only when 'num' marks the
    beginning of a sequence (i.e. num-1 is not present in nums), the while loop can only run for N iterations throughout
    the entire runtime of the algorithm, so we only start counting up from elements who have no predecessor.
    This means that despite looking like O(N^2) complexity, the nested loops actually run in O(N + N) = O(N) time.
    For example, nums = [6, 5, 4, 3, 2, 1] only the value 1 is valid for the loop, and that is O(N).
    For example, nums =  [100, 99, 98, ..., 1] (i.e. an array in reverse order):
    100 operations to add each element in the array to the set
    100 operations checking whether n - 1 exists in the set
    Once We get to 1, 100 operations to see if 1+ {1, 2, 3, ..., 100} exists in the set
    This is essentially 3N operations, which is expressed as O(N).
    In other words, We go through everything once to build the set (this is O(N)), and we go through everything once
    again looking for sequences (also O(N)), and then we find a sequence of length N (also O(N)).
    Space complexity: O(N)
    """
    if not nums:
        return 0
    nums, res = set(nums), 1
    for num in nums:
        if num - 1 not in nums:
            next_num = num + 1
            while next_num in nums:
                next_num += 1
            res = max(res, next_num - num)
    return res


class Test(unittest.TestCase):
    data = [([100, 4, 200, 1, 3, 2], 4)]

    def test_longest_consecutive(self):
        for test_nums, result in self.data:
            self.assertEqual(result, longest_consecutive_v1(test_nums))


if __name__ == '__main__':
    unittest.main()

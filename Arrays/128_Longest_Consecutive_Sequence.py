""" Given an unsorted array of integers, find the length of the longest consecutive elements sequence.
Your algorithm should run in O(n) complexity. """

import unittest2 as unittest


# Video explanation: https://youtu.be/P6RZZMu_maU
def longest_consecutive_v1(nums):
    """ Because a sequence could start at any number in nums, we can exhaust the entire search space by building as
        long a sequence as possible from every number.

        We consider each number in nums, attempting to count as high as possible from that number using only numbers in
        nums. After it counts too high (i.e. current number refers to a number that nums does not contain), it records
        the length of the sequence if it is larger than the current best.

        To allow for O(1) lookups, we first turn the input into a hash set of numbers. Then, go through the set.
        If the current number 'num' is the start of a streak (i.e., num-1 is not in the set), then test
        next_num = num+1, num+2, num+3, ... and stop at the first number not in the set. The length of the streak is
        then (next_num - num), and we update our global best to that.

        Intuition: We only attempt to build sequences from numbers that are not already part of a longer sequence.
        This is accomplished by first ensuring that the number that would immediately precede the current number in a
        sequence is not present, as that number would necessarily be part of a longer sequence.

    Time complexity: O(N), every number is processed only twice. Although the time complexity appears to be quadratic
    due to the while loop nested within the for loop, closer inspection reveals it to be linear. Because the while loop
    is reached only when 'num' marks the beginning of a sequence (i.e. num-1 is not present in nums), the while loop can
    only run for N iterations throughout the entire runtime of the algorithm, so we only start counting up from elements
    who have no predecessor. This means that despite looking like O(N^2) complexity, the nested loops actually run in
    O(N + N) = O(N) time.
    For example, nums = [6, 5, 4, 3, 2, 1] only the value 1 is valid for the loop, and that is O(N).
    For example, nums =  [100, 99, 98, ..., 1] (i.e. an array in reverse order):
    100 operations to add each element in the array to the set.
    100 operations checking whether n - 1 exists in the set.
    Once we get to 1, 100 operations to see if 1+ {1, 2, 3, ..., 100} exists in the set.
    This is essentially 3N operations, which is expressed as O(N).
    In other words, we go through every number once to build the set (this is O(N)), and we go through every number once
    again looking for sequences (also O(N)), and then we find a sequence of length N (also O(N)).
    Space complexity: O(N)
    """
    nums = set(nums)
    res = 0
    for num in nums:
        if num - 1 in nums:
            continue
        sequence_start = num
        while num in nums:
            num += 1
        res = max(res, num - sequence_start)
    return res


def longest_consecutive_v2(nums):
    """ Similar to the previous approach.

        We need to find the longest consecutive sequence in linear time. We can do this if we insert all the elements
        of nums into a hashset. Once we have inserted all the elements, we can just iterate over the hashset to find
        the longest consecutive sequence involving the current element (let's call it num) under iteration.

        This can simply be done by iterating over elements that immediately preceded or follow num as long as we keep
        finding them in the set. Each time we will also delete those elements from set to ensure we only visit them once.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    nums_set, res = set(nums), 0
    for num in nums:
        prev_num = num - 1
        while prev_num in nums_set:
            nums_set.remove(prev_num)
            prev_num -= 1
        next_num = num + 1
        while next_num in nums_set:
            nums_set.remove(next_num)
            next_num += 1
        res = max(res, next_num - prev_num - 1)
    return res


def longest_consecutive_v3(nums):
    """ Keep track of the sequence length and store that in the boundary points of the sequence.

        Whenever a new element 'num' is encountered, do two things:

            1- See if (num - 1) and (num + 1) exist in the map, and if so, it means there is an existing sequence next
               to 'num' (preceding and/or following it). Variables 'left' and 'right' will be the length of those two
               sequences, while 0 means there is no sequence and 'num' will be the boundary point later.
               Store (left + right + 1) as the associated value to key 'num' into the map.
            2- Use 'left' and 'right' to locate the other end of the sequences to the left and right of 'num',
               respectively, and replace the value with the new length.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    part_of_sequence_length, res = {}, 0
    for num in nums:
        if num not in part_of_sequence_length:
            left = part_of_sequence_length.get(num - 1, 0)
            right = part_of_sequence_length.get(num + 1, 0)
            length = left + right + 1  # Length of the sequence 'num' is part of
            part_of_sequence_length[num] = length
            res = max(res, length)
            # Extend the length to the boundary(s) of the sequence. Will do nothing if 'num' has no neighbors
            part_of_sequence_length[num - left] = length
            part_of_sequence_length[num + right] = length
    return res


class Test(unittest.TestCase):
    data = [([100, 4, 200, 1, 3, 2], 4)]

    def test_longest_consecutive(self):
        for test_nums, result in self.data:
            self.assertEqual(result, longest_consecutive_v1(test_nums))
            self.assertEqual(result, longest_consecutive_v2(test_nums))
            self.assertEqual(result, longest_consecutive_v3(test_nums))


if __name__ == '__main__':
    unittest.main()

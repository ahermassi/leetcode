""" Given a sequence of n integers a1, a2, ..., an, a 132 pattern is a subsequence ai, aj, ak such that i < j < k and
ai < ak < aj. Design an algorithm that takes a list of n numbers as input and checks whether there is a 132 pattern in
the list. """

import unittest2 as unittest


def find_132_pattern(nums):
    """ We need to search for a sub-sequence (s1, s2, s3) such that s1 < s3 < s2 .
        Suppose we want to find a 123 sequence with s1 < s2 < s3, we just need to find s3, followed by s2 and s1.
        Now if we want to find a 132 sequence with s1 < s3 < s2, we need to switch up the order of searching. We want
        to first find s2, followed by s3, then s1.
        More precisely, we keep track of highest value of s3 for each valid (s3 < s2) pair while searching for a valid
        s1 candidate to the LEFT. Once we encounter any number on the left that is smaller than the largest s3 we have
        seen so far, we know we found a valid sequence, since s1 < s3 implies s1 < s2.
        The idea is to start from end and search for valid (s3 < s2) pairs and remember the largest valid s3 value.
        Using a stack will be effective for this purpose. A number becomes a candidate for s3 if there is any number on
        the left bigger than it.
        As we scan from right to left, we can easily keep track of the largest s3 value of all (s2 , s3) candidates
        encountered so far. Hence, each time we compare nums[i] with the largest candidate for s3 within the interval
        nums[i+1]...nums[n-1], we are effectively asking the question: Is there any 132 sequence with s1 = nums[i]?
        Therefore, if the function returns false, there must be no 132 sequence.
            1- Have a stack, each time we store a new number, we first pop out all numbers that are smaller than that
               number. The numbers that are popped out become candidate for s3.
            2- We keep track of the maximum of such s3
            3- Once we encounter any number smaller than s3, we know we found a valid sequence since s1 < s3 implies
               s1 < s2
        The key points are:
            - Keep the value of s3 as big as possible
            - Use a 'sorted' stack to maintain the candidates of s2 and s3
            - The numbers in the stack are s2 and the number that popped out is the maximum s3. So the last thing to do
              is to maintain the order of the stack.
        From end to start, if we find nums[i] is less than the maximum element that is smaller than another, then we
        can say we found the pattern.
        Pretty much we are only storing one item in the stack, which is our ideal candidate for s2 (number that needs
        to be the largest). If we find a number that is bigger than what we THOUGHT was our ideal candidate for s2, we
        pop out our stack and store the value in s3 (mid value number), then we store the new ideal candidate for s2 in
        the stack. At the next iteration, if nums[i] is actually less than s3, then we are done.
        Example: nums = [9, 11, 8, 9, 10, 7, 9]
        i = 6, nums = [9, 11, 8, 9, 10, 7, 9], S2 candidate = 9, S3 candidate = None, Stack = [9]
        i = 5, nums = [ 9, 11, 8, 9, 10, 7, 9 ], S2 candidate = 7, S3 candidate = None, Stack = [9, 7]
        i = 4, nums = [ 9, 11, 8, 9, 10, 7, 9 ], S2 candidate = 10, S3 candidate = 9, Stack = [10]
        i = 3, nums = [ 9, 11, 8, 9, 10, 7, 9 ], S2 candidate = 10, S3 candidate = 9, Stack = [10, 9]
        i = 2, nums = [ 9, 11, 8, 9, 10, 7, 9 ], S2 candidate = 10, S3 candidate = 9, Stack = [10,9]
        We have 8 < S3 = 9, sequence (8, 10, 9) found
    Time complexity: O(N), each item is pushed and popped once at most
    Space complexity: O(N)
    """
    s3 = float('-inf')
    stack = []
    for num in nums[::-1]:
        if num < s3:
            return True
        while stack and stack[-1] < num:
            s3 = stack.pop()  # The maximum candidate for s3 is always the recently popped number from the stack,
            # because if we encounter any entry smaller than the current candidate, the function would already have
            # returned.
        stack.append(num)
    return False


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4], False), ([3, 1, 4, 2], True), ([-1, 3, 2, 0], True)]

    def test_find_132_pattern(self):
        for test_nums, result in self.data:
            self.assertEqual(result, find_132_pattern(test_nums))


if __name__ == '__main__':
    unittest.main()
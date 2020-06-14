""" A message containing letters from A-Z is being encoded to numbers using the following mapping:

'A' -> 1
'B' -> 2
...
'Z' -> 26
Given a non-empty string containing only digits, determine the total number of ways to decode it.
"""

import unittest2 as unittest

# Watch: https://www.youtube.com/watch?v=YcJTyrG3bZs


def num_decodings_v1(s):
    """ Top-down, recursive. TLE. The logic is similar to 70- Climbing Stairs.
        The most important point to understand in this problem is that, at any given step, when we are trying to decode
        a string of numbers it can either be a single digit decode e.g. 1 to 'A' or a double digit decode e.g. 25 to
        'Y'. As long as it's a valid decoding, we move ahead to decode the rest of the string.
        The sub-problem could be thought of as number of ways decoding a substring.
        What helps to crack the problem is to think why there would be many ways to decode a string. The reason is
        simple since at any given point we either decode using two digits or single digit. This choice while decoding
        can lead to different combinations.
        Recursively decompose the string using a decoding pointer 'index'. At every point of the recursion, we can make
        2 decisions:
            1- Decode one character out: valid if current character at 'index' is between 1 and 9
            2- Decode two characters out: valid if s[index:index+2] is between 10 and 26
        If at any point the decoding is possible, we recurse on the rest of the string.
        This leads to multiple paths to decoding the entire string. If a given path leads to the end of the string,
        this means we could successfully decode the string. If at any point in the traversal we encounter digits which
         cannot be decoded, we backtrack from that path.
    Time complexity: O(2^N)
    Space complexity: O(N)
    """

    def dfs(index):
        if index >= n:  # Nothing left to decompose, so this is a valid decomposition
            return 1
        one = two = 0
        if s[index] != '0':  # Current character is between 1 and 9
            one = dfs(index + 1)
        if 10 <= int(s[index:index + 2]) <= 26:  # Current character is between 10 and 26
            two = dfs(index + 2)
        return one + two

    n = len(s)
    return dfs(0)


def num_decodings_v2(s):
    """ Recursion + memoization.
    Time complexity: O(N), memoization helps in pruning the recursion tree and hence decoding for an index only once
    Space complexity: O(N), the dictionary used for memoization would take the space equal to the length of the string.
    There would be an entry for each index value. The recursion stack would also be equal to the length of the string.
    """

    def dfs(index):
        if index >= n:  # Nothing left to decompose, so this is a valid decomposition
            return 1
        if index in memo:
            return memo[index]
        total_decompositions = 0
        if s[index] != '0':  # Current character is between 1 and 9
            total_decompositions += dfs(index + 1)
        if 10 <= int(s[index:index + 2]) <= 26:  # Current character is between 10 and 26
            total_decompositions += dfs(index + 2)
        memo[index] = total_decompositions
        return total_decompositions

    n, memo = len(s), {}
    return dfs(0)


def num_decodings_v3(s):
    """ Let dp[i] be the number of ways to parse the first i characters of s, or the number of ways to decode a string
        of length i. The basic concept is to build up the number of ways to get to state i from all the previous states
        less than i. We set dp[0] to 1 because there is only 1 way to decode an empty string. We can then build up the
        number of ways to decode starting from the first value and work our way to the end.
            dp[i] = dp[i-1] + dp[i-2]
        Which is not always true for this decode ways problem. Only when the decode is possible we add the results of
        the previous indices.
        We check if valid single digit decode is possible. This just means the character at index s[i-1] is non-zero
        since we do not have a decoding for zero. If the valid single digit decoding is possible, then we add dp[i-1]
        to dp[i] since all the ways up to (i-1)th character now lead up to ith character too.
        We check if valid two digit decode is possible. This means the substring s[i-2:i] is between 10 to 26. If the
        valid two digit decoding is possible, then we add dp[i-2] to dp[i].
    Time complexity: O(N)
    Space complexity: O(N)
    """
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]  # One step jump. We only need to ensure that s[i-1] (current character) is not equal to
            # zero, since only zero does not have a mapping to an alphabet and rest of the digits from 1 through 9 do
            # in fact have a mapping.
            # At this step, we're like saying "does it make sense to split the string into whatever came before me and
            # myself ?", which is only possible if current value is different from 0 so it can have a mapping.
            # Example: s = '271'; dp[0] = 1; dp[1] = 1 as there is only one way to decode '2'; dp[2] += dp[1] because
            # current value is '7' which is different from '0', so it can join the gang: dp[2] = 1 means there is 1 way
            # to decode first 2 characters at this point: 2 7
        if i - 2 >= 0 and '10' <= s[i - 2: i] <= '26':
            dp[i] += dp[i - 2]  # Two-step jump. At this stage, we're like saying "does it make sense to split the
            # string into (myself + previous character) and whatever came before ?", which is only possible if value of
            # (myself + previous character) is >= 10 and <= 26 so it can have a mapping. Now continuing with same
            # example: We're at dp[2] and current value is '7'. Look back one character: '27'. dp[2] += dp[0] is not
            # possible because 27 is not <= 26, so splitting the string into '27' and whichever came before that (empty
            # string in this case) is not a viable option.
    return dp[-1]


class Test(unittest.TestCase):
    data = [('12', 2), ('226', 3)]

    def test_num_decodings(self):
        for test_string, result in self.data:
            self.assertEqual(result, num_decodings_v1(test_string))
            self.assertEqual(result, num_decodings_v2(test_string))
            self.assertEqual(result, num_decodings_v3(test_string))


if __name__ == '__main__':
    unittest.main()
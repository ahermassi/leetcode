""" A message containing letters from A-Z is being encoded to numbers using the following mapping:

'A' -> 1
'B' -> 2
...
'Z' -> 26
Given a non-empty string containing only digits, determine the total number of ways to decode it.
 """

import unittest2 as unittest


def num_decodings(s):
    """ Let dp[i] = the number of ways to parse the first i characters of s, or the number of ways to decode a string
    of length i
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not s:
        return 0
    dp = [0] * (len(s) + 1)
    dp[0] = 1
    for i in range(1, len(s) + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1] # One step jump. We only need to ensure that s[i-1] is not equal to zero, since only zero
            # does not have a mapping to an alphabet and rest of the digits from 1 through 9 do in fact have a mapping.
            # At this step, we're like saying "does it make sense to split the string into whatever came before me and
            # myself ?", which is only possible if current value is different from 0 so it can have a mapping.
            # Example: s = '271'; dp[0] = 1; dp[1] = 1 as there is only one way to decode '2'; dp[2] += dp[1] because
            # current value is '7' which is different from '0', so it can join the gang: 1 way to decode: 2 7
        if len(s[i - 2: i]) == 2 and '10' <= s[i - 2: i] <= '26':
            dp[i] += dp[i - 2]  # Two steps jump. At this step, we're like saying "does it make sense to split the
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
            self.assertEqual(result, num_decodings(test_string))


if __name__ == '__main__':
    unittest.main()
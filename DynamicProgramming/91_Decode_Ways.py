""" A message containing letters from A-Z is being encoded to numbers using the following mapping:

'A' -> 1
'B' -> 2
...
'Z' -> 26
Given a non-empty string containing only digits, determine the total number of ways to decode it.
 """

import unittest2 as unittest


def num_decodings_v1(s):
    """ Let dp[i] = the number of ways to parse the first i characters of s.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not s:
        return 0
    dp = [0] * (len(s) + 1)
    dp[0] = 1
    for i in range(1, len(s) + 1):
        if s[i - 1] != '0':  # One step jump. We only need to ensure that s[i-1] is not equal to zero, since only zero
            # does not have a mapping to an alphabet and rest of the digits from 1 through 9 do in fact have a mapping.
            dp[i] += dp[i - 1]
        if len(s[i - 2: i]) == 2 and '10' <= s[i - 2: i] <= '26':  # Two steps jump
            dp[i] += dp[i - 2]
    return dp[-1]


class Test(unittest.TestCase):
    data = [('12', 2), ('226', 3)]

    def test_num_decodings(self):
        for test_string, result in self.data:
            self.assertEqual(result, num_decodings_v1(test_string))


if __name__ == '__main__':
    unittest.main()
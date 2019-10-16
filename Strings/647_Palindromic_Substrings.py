"""" Given a string, your task is to count how many palindromic substrings in this string.
The substrings with different start indexes or end indexes are counted as different substrings even they consist of
same characters. """

import unittest2 as unittest


def count_substrings_v1(s):
    """ Expand Around Center. Same as 5- Longest Palindromic Substring
        We observe that a palindrome mirrors around its center. Therefore, a palindrome can be expanded from its center.
        There are two cases of palindromes: even and odd length.
    Time complexity: O(N ** 2), since expanding a palindrome around its center could take O(N)
    Space complexity: O(1)
    """

    def palindrome_at(i, j):
        count = 0
        while i >= 0 and j < n and s[i] == s[j]:
            count += 1
            i -= 1
            j += 1
        return count

    res, n = 0, len(s)
    for i in range(n):
        res += palindrome_at(i, i)
        res += palindrome_at(i, i + 1)
    return res


def count_substrings_v2(s):
    """ Bottom-up Dynamic Programming.
        We observe how we can avoid unnecessary re-computation while validating palindromes. Consider the case "ababa".
        If we already knew that "bab" is a palindrome, it is obvious that "ababa" must be a palindrome since the two
        left and right end letters are the same.
        We define dp[i][j] as following:
        dp[i][j] is True is substring s[i:j + 1] is palindrome
        Therefore:
        dp[i][j] = (s[i] == s[j]) AND (dp[i+1][j-1])
        This yields a straight forward DP solution, which we first initialize the one letter palindromes, and work our
        way up finding all two letters palindromes, and so on...
    Time complexity: O(N ** 2)
    Space complexity: O(N ** 2) to store dp array
    """
    n, res = len(s), 0
    dp = [[False] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = True
        res += 1
    for i in reversed(range(n)):
        for j in range(i + 1, n):
            if s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                res += 1
    return res


class Test(unittest.TestCase):
    data = [('abc', 3), ('aaa', 6)]

    def test_count_substrings(self):
        for test_string, result in self.data:
            self.assertEqual(result, count_substrings_v1(test_string))
            self.assertEqual(result, count_substrings_v2(test_string))


if __name__ == '__main__':
    unittest.main()
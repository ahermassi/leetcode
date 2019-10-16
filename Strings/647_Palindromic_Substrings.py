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


class Test(unittest.TestCase):
    data = [('abc', 3), ('aaa', 6)]

    def test_count_substrings(self):
        for test_string, result in self.data:
            self.assertEqual(result, count_substrings_v1(test_string))


if __name__ == '__main__':
    unittest.main()
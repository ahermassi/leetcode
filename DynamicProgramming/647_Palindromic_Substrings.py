"""" Given a string, your task is to count how many palindromic substrings in this string.
The substrings with different start indexes or end indexes are counted as different substrings even they consist of
same characters. """

import unittest2 as unittest


def count_substrings_v1(s):
    """ Expand Around Center. Same as 5- Longest Palindromic Substring.

        There are two types of palindromes: Odd and even length palindromes.
        Odd length palindromes have a single character in the middle. Even length palindromes have two characters
        that constitute the middle, both of which are same. e.g. 'noon' with two middle characters 'o'.

        Palindromes are compositionally homogeneous around their center. In layman's terms, smaller palindromes make up
        larger palindromes. If we take the palindrome "eve" and surround it with the character 'l', we get a larger
        palindrome "level". Conversely, if we removed the starting and ending characters from "eve', we'd be left with
        the smaller, single-character palindrome "v".

        Let's take the string 'lever' as another example: If we choose the character 'v' as the center, we can see that
        the palindromes 'v and 'eve' are possible. However, the final expansion 'lever' is not a palindrome (the first
        and last characters don't match).

        Palindromes are like onions, you remove the boundary characters, and you're left with another, smaller
        palindrome.

        We choose all possible centers for potential palindromes:

            - Every single character in the string is a center for possible odd-length palindromes
            - Every pair of consecutive characters in the string is a center for possible even-length palindromes

        For every center, we can expand around it as long as we get palindromes (i.e. the first and last characters
        should match).

    Time complexity: O(N^2), since expanding a palindrome around its center could take O(N). Each center can
    potentially expand to the length of the string, so time spent on each center is linear on average. The number of
    possible palindromic centers is 2N−1: there are N single character centers and N−1 consecutive character pairs as
    centers.
    Space complexity: O(1)
    """

    def palindromes_at(left, right):
        palindromes = 0
        while left >= 0 and right < n and s[left] == s[right]:
            palindromes += 1
            left -= 1
            right += 1
        return palindromes

    res, n = 0, len(s)
    for i in range(n):
        odd_palindromes = palindromes_at(i, i)
        even_palindromes = palindromes_at(i, i + 1)
        res += odd_palindromes + even_palindromes
    return res


def count_substrings_v2(s):
    """ Bottom-up Dynamic Programming.
        This problem displays two, necessary characteristics of a dynamic programming problem:
            1- Optimal substructure: Remember that larger palindromes are made of smaller palindromes. Congratulation,
               we have discovered a substructure to our problem! Knowing that a string is made up of a palindrome helps
               us determine if the string itself is a palindrome. Here's an example: for the string 'axbobxa', the
               first and the last characters match, so it's a potential palindrome. If we knew already that its
               substring 'xbobx' is also a palindrome, there wouldn't be a need for any further checks.
               But is this substructure optimal? Yes! Since the optimal result for a string relies only on the optimal
               result for just one sub-problem, and has to do just one check for the boundary characters (in constant
               time), this is an optimal substructure. We cannot get this result by checking fewer than one sub-problem
               (it wouldn't be a substructure anymore) or doing the boundary characters check faster (it's already
               constant time!).
            2- Overlapping sub-problems: While checking all substrings of a large string for palindromicity, we might
               need to check some smaller substrings for the same, repeatedly. If we store the result of processing
               those smaller substrings, we can reuse those while processing larger substrings.
               Here's an example: for the string 'axbobx'", the substring 'bob' needs to checked for the substring
               'xbobx' and the string 'axbobxa'. In fact, to check all three of these strings, the single character
               string 'o' needs to be checked.
        We define our state dp[i][j] as following:

            dp[i][j] is True if the substring composed of the ith to the jth characters of the input string is a
            palindrome

        A string is considered a palindrome if:
            - Its first and last characters are equal, and
            - The rest of the string (excluding the boundary characters) is also a palindrome
        Thus, the answer to our problem lies in counting all substrings whose state is true:

                dp[i][j] = (s[i] == s[j]) AND (dp[i+1][j-1])

        But here, we should explain why we use dp[i+1][j-1] to calculate dp[i][j]. The reason is that i is in
        descending order and j is in ascending order. Then we know that before d[i][j] the value of d[i+1][j-1] is
        already known and calculated in a previous iteration.
        Build a table with all possible string[start:end] combinations, storing which are palindromes and which are
        not (True or False). At any given moment, when we're checking if string[i:j] is a palindrome, we only need to
        know two things:
            1- Is string[i] equal to string[j] ?
            2- Is string[i+1:j-1] a palindrome?
        For condition (1), a simple check will do. For condition (2), we use the table. If both conditions are met,
        mark dp[i][j] as True and increase the count.
    Time complexity: O(N^2)
    Space complexity: O(N^2), to store dp array
    """
    n, res = len(s), 0
    dp = [[False] * n for _ in range(n)]
    for i in range(n):  # Every isolated character is a palindrome
        dp[i][i] = True
        res += 1
    for i in reversed(range(n)):  # We reverse the range because the sub-problem is not populated yet. For example, if
        # we want to know if substring s[0-5] (i.e. dp[0][5]) is palindrome, we'd look up the table for dp[1][4].
        # However, if i goes from left to right, dp[1] has not been calculated yet because dp[1] comes after dp[0].
        for j in range(i + 1, n):
            if s[i] == s[j] and (j - i == 1 or dp[i + 1][j - 1]):  # When j = i + 1, j - i = 1, which is basically the
                # previous check s[i] == s[j]. When j > i + 1, the check dp[i + 1][j - 1] is necessary
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
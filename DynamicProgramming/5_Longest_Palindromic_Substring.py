""" Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.
"""


def longest_palindrome_v1(s):
    """ Expand Around Center.
        We observe that a palindrome mirrors around its center. Therefore, a palindrome can be expanded from its center.
        There are two cases of palindromes: even and odd length.
    Time complexity: O(N^2), since expanding a palindrome around its center could take O(N)
    Space complexity: O(1)
    """

    def palindrome_at(left, right):  # Starting at (left, right) expand outwards to find the longest palindrome
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1: right]

    n, res = len(s), ''
    for i in range(n):
        odd_palindrome = palindrome_at(i, i)  # Odd case, like "aba"
        even_palindrome = palindrome_at(i, i + 1)  # Even case, like "abba"
        res = max(res, odd_palindrome, even_palindrome, key=len)
    return res


def longest_palindrome_v2(s):
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
        Why are we counting down for i, but counting up for j? Each sub-problem dp[i][j] depends on dp[i+1][j-1].
    Time complexity: O(N ** 2)
    Space complexity: O(N ** 2) to store dp array
    """
    res = ''
    dp = [[False] * len(s) for _ in range(len(s))]
    for i in range(len(s)):
        dp[i][i] = True
        res = s[i]
    for i in reversed(range(len(s))):
        for j in range(i + 1, len(s)):
            if s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1]):  # dp[i+1][j-1] represents the middle of the current
                # considered substring
                dp[i][j] = True  # If the middle is a palindrome and the endpoints equal each other, it follows that
                # s[i:j+1] is a palindrome
                if j - i + 1 > len(res):
                    res = s[i: j + 1]
    return res



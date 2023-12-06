""" Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.
"""


def longest_palindrome_v1(s):
    """ Expand from centers.

        We observe that a palindrome mirrors around its center. Therefore, a palindrome can be expanded from its center.

        We can consider odd-length palindromes by starting the pointers at (i, i). To consider the even length
        palindromes, we can start the pointers at (i, i + 1). There are N starting points for the odd-length palindromes
        and N-1 starting points for the even-length palindromes.

        We expand from the center as far as we can to find the longest palindrome, and then return the length of this
        palindrome.

    Time complexity: O(N^2), since expanding a palindrome around its center could take O(N) and there are N centers
    Space complexity: O(1)
    """

    def palindrome_at(left, right):
        # Starting at (left, right), expand outwards to find the longest palindrome
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
        We observe that we can avoid unnecessary re-computation while validating palindromes.
        Consider the case 'ababa'. If we already knew that 'bab' is a palindrome, it is obvious that 'ababa' must be a
        palindrome since the two left and right end letters are the same.
        We define dp[i][j] as following:
            dp[i][j] = True if substring s[i:j + 1] is palindrome
        Therefore:
            dp[i][j] = (s[i] == s[j]) AND (dp[i+1][j-1])
        This yields a straightforward DP solution, in which we first initialize the 1-letter palindromes, and work our
        way up finding all 2-letter palindromes, and so on.
        Why are we counting down for i, but counting up for j? Each sub-problem dp[i][j] depends on dp[i+1][j-1].
    Time complexity: O(N^2)
    Space complexity: O(N^2), to store dp array
    """
    n, res = len(s), ''
    dp = [[False] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = True
        res = s[i]
    for i in reversed(range(n)):
        for j in range(i + 1, n):
            if s[i] == s[j] and (j == i + 1 or dp[i + 1][j - 1]):  # dp[i+1][j-1] represents the middle of the current
                # considered substring
                dp[i][j] = True  # If the middle is a palindrome and the endpoints equal each other, it follows that
                # s[i:j+1] is a palindrome
                if j - i + 1 > len(res):
                    res = s[i: j + 1]
    return res



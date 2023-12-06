""" Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.
"""


# Video explanation: https://youtu.be/XYQecbcd6_c
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

        Let's say that we knew the substring with inclusive bounds (i, j) was a palindrome. If s[i-1] == s[j+1], then
        we know the substring with inclusive bounds (i-1, j+1) must also be a palindrome, and this check can be done in
        constant time.

        We can flip the direction of this logic as well - if s[i] == s[j] and the substring (i+1, j-1) is a palindrome,
        then the substring (i, j) must also be a palindrome.

        We know that all substrings of length 1 are palindromes. From this, we can check if each substring of length 3
        is a palindrome using the above fact. We just need to check every (i, j) pair where j - i = 2. Once we know all
        palindromes of length 3, we can use that information to find all palindromes of length 5, and then 7, and so on.

        What about even-length palindromes? A substring of length 2 is a palindrome if both characters are equal. That
        is, (i, i+1) is a palindrome if s[i] == s[i+1]. From this, we can use the earlier logic to find all palindromes
        of length 4, then 6, and so on.

        Consider the case 'ababa'. If we already knew that 'bab' is a palindrome, it is obvious that 'ababa' must be a
        palindrome since the two left and right end letters are the same.

        We define dp[i][j] as following:

                        dp[i][j] = True if substring s[i:j + 1] is palindrome

        Therefore:

                        dp[i][j] = (s[i] == s[j]) AND (dp[i+1][j-1])

        This yields a straightforward DP solution, in which we first initialize the 1-letter palindromes, and work our
        way up finding all 2-letter palindromes, and so on.

        Why are we counting down for i, but counting up for j?

        We process the string backwards because dp[i][j] depends on dp[i+1][j-1]. If i goes from left to right (in
        increasing order), the sub-problem (i+1,j-1) wouldn't have been calculated yet when we need to solve the
        sub-problem (i,j). However, when i is decreasing, the calculation is possible as (i, j) == ( (i+1)-1, (j-1)+1 )
        —> i decreasing and j increasing.

    Time complexity: O(N^2)
    Space complexity: O(N^2), to store dp array
    """
    n = len(s)
    res = s[0] # Every character in the string is a palindrome by default
    dp = [[False] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = True
    for i in reversed(range(n)):
        for j in range(i + 1, n):
            # dp[i+1][j-1] represents the middle of the current considered substring
            if s[i] == s[j] and (j == i + 1 or dp[i + 1][j - 1]):
                # If the middle is a palindrome and the endpoints equal each other, it follows that
                # s[i:j+1] is a palindrome
                dp[i][j] = True
                if j - i + 1 > len(res):
                    res = s[i: j + 1]
    return res



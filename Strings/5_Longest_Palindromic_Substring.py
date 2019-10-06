""" Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.
"""


def longest_palindrome_v1(s):
    """ Expand Around Center.
        We observe that a palindrome mirrors around its center. Therefore, a palindrome can be expanded from its center.
        There are two cases of palindromes: even and odd length.
    Time complexity: O(N ** 2), since expanding a palindrome around its center could take O(N)
    Space complexity: O(1)
    """

    def palindrome_at(left, right):  # Starting at left, right expand outwards to find the longest palindrome
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1: right]

    res = ''
    for i in range(len(s)):
        odd_palindrome = palindrome_at(i, i)  # Odd case, like "aba"
        even_palindrome = palindrome_at(i, i + 1)  # Even case, like "abba"
        res = max(res, odd_palindrome, even_palindrome, key=len)
    return res


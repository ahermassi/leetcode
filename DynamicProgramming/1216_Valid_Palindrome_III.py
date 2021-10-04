""" Given a string s and an integer k, return true if s is a k-palindrome.

A string is k-palindrome if it can be transformed into a palindrome by removing at most k characters from it. """


def is_valid_palindrome_v1(s, k):
    """ Brute force. TLE

        How do we find the minimum characters to be removed to make the string a palindrome? Let's imagine matching the
        characters of the string like a palindrome, from the beginning and the end with two pointers 'left' and
        'right'. We may encounter the two following scenarios:
            - The character at 'left' matches character at 'right'
            - The characters don't match

        For case 1, we just increase the left pointer and decrease the right pointer and process the rest of the string
        In the second case, we have 2 options:
            - Remove the character at 'left' and see if the previous character matches character at 'left'.
                Or
            - Remove the character at 'right' and see if the next character matches character at 'right'.

        Since we are not actually removing the characters from the string but just calculating the number of characters
        to be removed, we either decrement the right pointer and left pointer stays as it is, or increment the left
        pointer and right pointer stays as it is. In both the cases, we remove 1 character and thus it adds 1 to the
        removal cost.

        We can then use these two different pairs of new 'left' and 'right' values (left+1, right) and (left, right-1)
        to again repeat the process until the entire string is processed.
    Time complexity: O(2^N), we try to find result for all combinations of 'left' and 'right' where 'left' and 'right'
    range from 0 to N. At each step we either delete a character or delete it.
    Space complexity: O(N)
    """

    def can_construct_palindrome(left, right, removals):
        if left >= right:  # Base case: only 1 character remaining OR the entire string has been processed (left>right)
            return True
        if s[left] == s[right]:
            return can_construct_palindrome(left + 1, right - 1, removals)
        if removals == 0:  # No more characters' removal is possible
            return False
        # Character at 'left' does not match character at 'right'. Either delete character at 'left' or delete
        # character at 'right'
        return can_construct_palindrome(left + 1, right, removals - 1) \
               or can_construct_palindrome(left, right - 1, removals - 1)

    n = len(s)
    return can_construct_palindrome(0, n - 1, k)


def is_valid_palindrome_v2(s, k):
    """ Top-Down Dynamic Programming.
        Same previous algorithm but with memoization.
    Time complexity: O(N^2)
    Space complexity: O(N)
    """

    def can_construct_palindrome(left, right, removals):
        if left >= right:
            return True
        if (left, right, removals) not in memo:
            if s[left] == s[right]:
                res = can_construct_palindrome(left + 1, right - 1, removals)
            elif removals == 0:
                res = False
            else:
                res = can_construct_palindrome(left + 1, right, removals - 1) or \
                      can_construct_palindrome(left, right - 1, removals - 1)
            memo[(left, right, removals)] = res
        return memo[(left, right, removals)]

    n = len(s)
    memo = {}
    return can_construct_palindrome(0, n - 1, k)

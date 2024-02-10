""" Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.
"""

import unittest2 as unittest


def is_palindrome_v1(x):
    """ Convert x to a string and check if it's a palindrome using two pointers.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    s = str(x)
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def is_palindrome_v2(x):
    """ First note that if the input is negative, then its representation as a decimal string cannot be palindromic,
         since it begins with a '-'.

         We can avoid the O(N) space complexity used by the string representation by directly extracting the digits from
         the input. By doing so, we can reverse the entire input number and check if the reversed number is equal to
         the original number. If they are the same, then the number is a palindrome.

            - Initialize two variables:
               reverse: This variable will store the reversed value of the number x.
               temp: This variable is a temporary placeholder to manipulate the input number without modifying the
               original value.

            - Extract the last digit of temp using the modulo operator %

            - To reverse the number, multiply the current value of reversed by 10 and add the extracted digit.

            - Divide temp by 10 to remove the last digit and move on to the next iteration.

    Time complexity: O(log10 x), since we divide the input by 10 in every iteration
    Space complexity: O(1)
    """
    if x < 0:
        return False
    temp, reverse = x, 0
    while temp:
        reverse = reverse * 10 + temp % 10
        temp //= 10
    return reverse == x


def is_palindrome_v3(x):
    """ What if we only revert half of the int number? After all, the reverse of the last half of the palindrome should
        be the same as the first half of the number, if the number is a palindrome.
        Now the question is, how do we know that we've reached the half of the number?
        Since we divided the number by 10, and multiplied the reversed number by 10, when the original number is less
        than the reversed number, it means we've processed half of the number digits.
    Time complexity: O(log10 x)
    Space complexity: O(1)
    """
    if x < 0 or (x % 10 == 0 and x):  # When x < 0, x is not a palindrome. Also if the last digit of the number is 0,
        # in order to be a palindrome, the first digit of the number also needs to be 0. Only 0 satisfies this property.
        return False
    reverse = 0
    while reverse < x:
        reverse = reverse * 10 + x % 10
        x = x // 10
    # When the length is an odd number, we can get rid of the middle digit by reverse // 10. For example, when the
    # input is 12321, at the end of the while loop we get x = 12, reverse = 123. Since the middle digit doesn't matter
    # in palindrome (it will always be equal to itself), we can simply get rid of it.
    return reverse == x or reverse // 10 == x


class Test(unittest.TestCase):
    data = [(121, True), (-123, False), (10, False)]

    def test_is_palindrome(self):
        for test_number, result in self.data:
            self.assertEqual(result, is_palindrome_v1(test_number))
            self.assertEqual(result, is_palindrome_v2(test_number))
            self.assertEqual(result, is_palindrome_v3(test_number))


if __name__ == '__main__':
    unittest.main()

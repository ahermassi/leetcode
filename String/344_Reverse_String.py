""" Write a function that reverses a string. The input string is given as an array of characters char[].
Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra
memory. """

import unittest2 as unittest


def reverse_string_v1(s):
    """ Two pointers are used to process two array elements at the same time.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return s


def reverse_string_v2(s):
    """ Implement recursive function helper() which receives two pointers, left and right, as arguments.
        If left >= right, do nothing.
        Otherwise, swap s[left] and s[right] and call helper(left + 1, right - 1).
    Time complexity: O(N)
    Space complexity: O(N) for recursion stack
    """

    def helper(left, right):
        if left < right:
            s[left], s[right] = s[right], s[left]
            helper(left + 1, right - 1)

    helper(0, len(s) - 1)
    return s


class Test(unittest.TestCase):
    data = [(['h', 'e', 'l', 'l', 'o'], ['o', 'l', 'l', 'e', 'h']),
            (['H', 'a', 'n', 'n', 'a', 'h'], ['h', 'a', 'n', 'n', 'a', 'H'])]

    def test_reverse_string(self):
        for test_string, result in self.data:
            # self.assertEqual(result, reverse_string_v1(test_string))
            self.assertEqual(result, reverse_string_v2(test_string))


if __name__ == '__main__':
    unittest.main()

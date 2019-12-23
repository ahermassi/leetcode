""" Write a function that reverses a string. The input string is given as an array of characters char[].
Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra
memory. """

import unittest2 as unittest


def reverse_string(s):
    """
    Time complexity: O(N)
    Space complexity: O(1)
    """
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return s


class Test(unittest.TestCase):
    data = [(['h', 'e', 'l', 'l', 'o'], ['o', 'l', 'l', 'e', 'h']),
            (['H', 'a', 'n', 'n', 'a', 'h'], ['h', 'a', 'n', 'n', 'a', 'H'])]

    def test_reverse_string(self):
        for test_string, result in self.data:
            self.assertEqual(result, reverse_string(test_string))


if __name__ == '__main__':
    unittest.main()

""" A strobogrammatic number is a number that looks the same when rotated 180 degrees (looked at upside down).
Write a function to determine if a number is strobogrammatic. The number is represented as a string. """

import unittest2 as unittest


def is_strobogrammatic_v1(num):
    """ Pretty straightforward. This solution is hash map based.
    Time complexity: O(N), where N is the length of num
    Space complexity: O(N), for num_upside_down list (the dictionary is O(1) space)
    """
    map, num_upside_down = {'0': '0', '1': '1', '6': '9', '8': '8', '9': '6'}, []
    for c in num:
        if c not in map:
            return False
        num_upside_down.append(map[c])
    return num_upside_down[::-1] == list(num)


def is_strobogrammatic_v2(num):
    """ Keep two pointers and check each 2 digits from both ends, similar to what we do to check a palindrome.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    map = {'0': '0', '1': '1', '6': '9', '8': '8', '9': '6'}
    left, right = 0, len(num) - 1
    while left <= right:
        a, b = num[left], num[right]
        if a not in map or map[a] != b:
            return False
        left += 1
        right -= 1
    return True


class Test(unittest.TestCase):
    data = [('69', True),
            ('88', True),
            ('962', False)
            ]

    def test_is_strobogrammatic(self):
        for test_num, result in self.data:
            self.assertEqual(result, is_strobogrammatic_v1(test_num))
            self.assertEqual(result, is_strobogrammatic_v2(test_num))


if __name__ == '__main__':
    unittest.main()

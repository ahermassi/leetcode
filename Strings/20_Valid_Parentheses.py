""" Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is
valid.
An input string is valid if:
1- Open brackets must be closed by the same type of brackets.
2- Open brackets must be closed in the correct order.
"""

import unittest2 as unittest


def is_valid_v1(s):
    """ Let's do this recursively.
        1- An empty string is valid
        2 - A string s of length 2 is valid if and only if s[1] is the closing bracket of s[0] (Condition 2 below)
        3- A string s of the length > 2 is:
            * Not valid if s[0] is a closing bracket. (Condition 3 below)
            * Candidate valid if s[0] is an opening bracket but s[1] is not its matching closing bracket, in which case
            recursively investigate s[1:] and go to 1- 2- 3- (Condition 4 below)
            * Candidate valid if s[1] is the closing bracket of s[0], in which case remove s[0:2] and recursively
            investigate the rest of the string. (Condition 5 below)
        The idea is to examine pairs of same type of bracket, when a matching pair is found delete it, rinse and repeat.
    Time complexity: O(N) where N is the length of s
    Space complexity: O(N), in the worst case s could be a sequence of only opening brackets ( '(((((((((((' )
    """

    s, d = list(s), {'(': ')', '{': '}', '[': ']'}

    def process(s, index):
        if not s:  # Condition 1
            return True
        if len(s) == 2:
            try:
                return s[index + 1] == d[s[index]]  # Condition 2
            except KeyError:
                return False
        if len(s) > 2:
            if s[index] not in d:  # Condition 3
                return False
            if s[index + 1] != d[s[index]]:  # Condition 4
                return process(s, index + 1)
            else:  # Condition 5
                s[index:index + 2] = []
                return process(s, index - 1 if index >= 1 else 0)

    return process(s, 0)


class Test(unittest.TestCase):
    data = [('()', True),
            ('()[]{}', True),
            ('(]', False),
            ('([)]', False),
            ('{[]}', True)
            ]

    def test_is_valid(self):
        for test_string, result in self.data:
            self.assertEqual(result, is_valid_v1(test_string))


if __name__ == '__main__':
    unittest.main()
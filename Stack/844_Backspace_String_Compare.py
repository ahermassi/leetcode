""" Given two strings S and T, return if they are equal when both are typed into empty text editors. # means a
backspace character. """

import unittest2 as unittest


def backspace_compare(s, t):
    """ To build the result of a string build(S), use a stack based approach, simulating the result of each
    keystroke.
    Time complexity: O(max(N, M)) where N is the length of s and M is the length of t
    Space complexity: O(max(N, M))
    """

    def build(string):  # This is a helper function, saves us a few keystrokes
        stack = []
        for c in string:
            if c != '#':
                stack.append(c)
            elif len(stack):
                stack.pop()
        return ''.join(stack)

    return build(s) == build(t)


class Test(unittest.TestCase):
    dataT = [('ab#c', 'ad#c'),
             ('ab##', 'c#d#'),
             ('a##c', '#a#c')
             ]
    dataF = [('a#c', 'b')]

    def test_move_zeroes(self):
        for test_string1, test_string2 in self.dataT:
            self.assertTrue(backspace_compare(test_string1, test_string2))
        for test_string1, test_string2 in self.dataF:
            self.assertFalse(backspace_compare(test_string1, test_string2))


if __name__ == '__main__':
    unittest.main()

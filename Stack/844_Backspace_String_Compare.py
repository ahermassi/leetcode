""" Given two strings S and T, return if they are equal when both are typed into empty text editors. # means a
backspace character. """

import itertools
import unittest2 as unittest


def backspace_compare_v1(s, t):
    """ To build the result of a string build(S), we use a stack to simulate the result of each keystroke. Every time
        we encounter a valid char, we add it to the stack. Every time we encounter a backspace, we pop the last char
        that was added to the stack.
    Time complexity: O(max(N, M)), where N is the length of s and M is the length of t
    Space complexity: O(max(N, M))
    """

    def build(string):
        stack = []
        for c in string:
            if c != '#':
                stack.append(c)
            elif stack:
                stack.pop()
        return ''.join(stack)

    return build(s) == build(t)


def backspace_compare_v2(s, t):
    """ Make generators to yield the final chars from back to front. Compare the chars one-by-one.
    This is the recommended (follow up) version in interviews.
    Time complexity: O(max(N, M)) where N is the length of s and M is the length of t
    Space complexity: O(1)
    """
    def next_char_gen(string):
        backspace = 0
        for i in reversed(range(len(string))):
            if string[i] == '#':
                backspace += 1
            elif backspace > 0:
                backspace -= 1
            else:
                yield string[i]

    s_gen = next_char_gen(s)
    t_gen = next_char_gen(t)
    for s, t in itertools.zip_longest(s_gen, t_gen):
        if s != t:
            return False
    return True


class Test(unittest.TestCase):
    dataT = [('ab#c', 'ad#c'),
             ('ab##', 'c#d#'),
             ('a##c', '#a#c')
             ]
    dataF = [('a#c', 'b')]

    def test_backspace_compare(self):
        for test_string1, test_string2 in self.dataT:
            self.assertTrue(backspace_compare_v1(test_string1, test_string2))
            self.assertTrue(backspace_compare_v2(test_string1, test_string2))
        for test_string1, test_string2 in self.dataF:
            self.assertFalse(backspace_compare_v1(test_string1, test_string2))
            self.assertFalse(backspace_compare_v2(test_string1, test_string2))


if __name__ == '__main__':
    unittest.main()

""" Given two strings S and T, return if they are equal when both are typed into empty text editors. # means a
backspace character. """

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
    """ When writing a character, it may or may not be part of the final string depending on how many backspace
        keystrokes occur in the future. If instead we iterate through the string in reverse, then we will know how many
        backspace characters we have seen, and therefore whether the result includes our character. If we meet a '#',
        it tells us we need to skip next lowercase char.
        The idea is that we read next letter from end to start. If we meet a '#', we increase the number we need to
        step back, until backspace = 0
    Time complexity: O(max(N, M)), where N is the length of s and M is the length of t
    Space complexity: O(1)
    """
    i, j = len(s) - 1, len(t) - 1
    backspace_s = backspace_t = 0
    while i >= 0 or j >= 0:
        while i >= 0 and (s[i] == '#' or backspace_s > 0):
            backspace_s += 1 if s[i] == '#' else -1
            i -= 1
        while j >= 0 and (t[j] == '#' or backspace_t > 0):
            backspace_t += 1 if t[j] == '#' else -1
            j -= 1
        if i >= 0 and j >= 0 and s[i] != t[j]:  # If two actual characters are different
            return False
        if (i >= 0) != (j >= 0):  # If expecting to compare char to nothing
            return False
        i -= 1
        j -= 1
    return True


class Test(unittest.TestCase):
    data = [('ab#c', 'ad#c', True), ('ab##', 'c#d#', True), ('a##c', '#a#c', True), ('a#c', 'b', False)]

    def test_backspace_compare(self):
        for test_s, test_t, result in self.data:
            self.assertEqual(result, backspace_compare_v1(test_s, test_t))
            self.assertEqual(result, backspace_compare_v2(test_s, test_t))


if __name__ == '__main__':
    unittest.main()

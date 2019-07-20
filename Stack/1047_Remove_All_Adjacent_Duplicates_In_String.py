""" Given a string S of lowercase letters, a duplicate removal consists of choosing two adjacent and equal letters,
and removing them.
We repeatedly make duplicate removals on S until we no longer can. """

import unittest2 as unittest


def remove_duplicates(S):
    """ Loop on characters in the string S one by one.
        If the next character is the same as the last in stack, pop the last character from stack.
        Otherwise append the the next character to the end of stack.
    Time complexity: O(N) where N is the length of the string
    Space complexity: O(N)
    """
    stack = []
    for c in S:
        if len(stack) >= 1 and stack[-1] == c:
            stack.pop()
        else:
            stack.append(c)
    return ''.join(stack)


class Test(unittest.TestCase):
    data = [('abbaca', 'ca')]

    def test_move_zeroes(self):
        for test_string, result in self.data:
            self.assertEqual(result, remove_duplicates(test_string))


if __name__ == '__main__':
    unittest.main()


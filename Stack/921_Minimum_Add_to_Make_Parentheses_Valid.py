""" Given a string S of '(' and ')' parentheses, we add the minimum number of parentheses ( '(' or ')', and in any
positions ) so that the resulting parentheses string is valid.
Formally, a parentheses string is valid if and only if:
It is the empty string, or
It can be written as AB (A concatenated with B), where A and B are valid strings, or
It can be written as (A), where A is a valid string.
Given a parentheses string, return the minimum number of parentheses we must add to make the resulting string valid. """

import unittest2 as unittest


def min_add_to_make_valid_v1(S):
    """ Each time we encounter an open parenthesis '(', we add it to the stack. If we come across a closing
        parenthesis ')' we check if there is a matching '(' on top of stack. If yes, we pop it out. Otherwise, we
        increment 'right_unmatched' counter by 1. At the end, we count in the unmatched parenthesis remaining in the
        stack.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    stack, right_unmatched = [], 0
    for c in S:
        if c == '(':
            stack.append(c)
        elif stack:
            stack.pop()
        else:
            right_unmatched += 1
    return len(stack) + right_unmatched


def min_add_to_make_valid_v2(S):
    """ The previous solution could use one less variable. The stack can hold both unmatched left and right parenthesis.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    stack = []
    for c in S:
        if c == '(':  # Push the open parenthesis anticipating for a closing match
            stack.append(c)
        elif not stack or stack[-1] == ')':  # Push the closing parenthesis if it has no opening match
            stack.append(c)
        else:
            stack.pop()  # It's a match! Pop
    return len(stack)


def min_add_to_make_valid_v3(S):
    """ Since there is only one kind of char, '(', in the stack, only a counter will also work.
        To make a string valid, we can add some '(' on the left, and add some ')' on the right. We need to find the
        number of each.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    left_unmatched = right_unmatched = 0
    for c in S:
        if c == '(':
            left_unmatched += 1
        elif left_unmatched > 0:
            left_unmatched -= 1
        else:  # This is a right parenthesis ')' and there isn't an open one '(' to balance it out
            right_unmatched += 1
    return left_unmatched + right_unmatched


class Test(unittest.TestCase):
    data = [('())', 1), ('(((', 3), ('()', 0), ('()))((', 4)]

    def test_min_add_to_make_valid(self):
        for test_s, result in self.data:
            self.assertEqual(result, min_add_to_make_valid_v1(test_s))
            self.assertEqual(result, min_add_to_make_valid_v2(test_s))
            self.assertEqual(result, min_add_to_make_valid_v3(test_s))


if __name__ == '__main__':
    unittest.main()

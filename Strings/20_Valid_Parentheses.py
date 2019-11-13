""" Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is
valid.
An input string is valid if:
1- Open brackets must be closed by the same type of brackets.
2- Open brackets must be closed in the correct order.
"""

import unittest2 as unittest


def is_valid_v1(s):
    """ An interesting property about a valid parenthesis expression is that a sub-expression of a valid expression
        should also be a valid expression. (Not every sub-expression)
        What if whenever we encounter a matching pair of parenthesis in the expression, we simply remove it from the
        expression? If it is a valid expression, we would be left with an empty string in the end.
        The stack data structure can come in handy here in representing this recursive structure of the problem. We
        can't really process this from the inside out because we don't have an idea about the overall structure. But,
        the stack can help us process this recursively i.e. from outside to inwards.
        If we encounter an opening bracket, we simply push it onto the stack. This means we will process it later, let
        us simply move onto the sub-expression ahead.
        If we encounter a closing bracket, then we check the element on top of the stack. If the element at the top of
        the stack is an opening bracket of the same type, then we pop it off the stack and continue processing. Else,
        this implies an invalid expression.
        In the end, if we are left with a stack still having elements, then this implies an invalid expression.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    d, stack = {'(': ')', '{': '}', '[': ']'}, []
    for ch in s:
        if stack and stack[-1] in d and ch == d[stack[-1]]:
            stack.pop()
        else:
            stack.append(ch)
    return not stack


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
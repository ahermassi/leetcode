""" Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is
valid.
An input string is valid if:
1- Open brackets must be closed by the same type of brackets.
2- Open brackets must be closed in the correct order.
"""

import unittest2 as unittest


def is_valid_v1(s):
    """ Before looking at how we can check if a given expression consisting of these parentheses is valid or not, let
         us look at a simpler version of the problem that consists of just one type of parenthesis.

         We process the expression one bracket at a time starting from the left.
         Suppose we encounter an opening bracket i.e. (, it may or may not be an invalid expression because there can
         be a matching ending bracket somewhere in the remaining part of the expression. Here, we simply increment the
         counter keeping track of left parenthesis till now: left += 1
         If we encounter a closing bracket, this has two meanings:
            - One, there was no matching opening bracket for this closing bracket and in that case we have an invalid
               expression. This is the case when left == 0 i.e. when there are no unmatched left brackets available.
            - We had some unmatched opening bracket available to match this closing bracket. This is the case when
               left > 0 i.e. we have unmatched left brackets available.
        If we encounter a closing bracket i.e. ) when left == 0, then we have an invalid expression on our hands.
        Else, we decrement left thus reducing the number of unmatched left parenthesis available.
        Continue processing the string until all parenthesis have been processed.
        If in the end we still have unmatched left parenthesis available, this implies an invalid expression.

        If we try and follow the same approach for our original problem, then it simply won't work. The reason a
        simple counter based approach works above is because all the parenthesis are of the same type. So when we
        encounter a closing bracket, we simply assume a corresponding opening matching bracket to be available i.e.
        if left > 0. But, in our problem, if we encounter say ], we don't really know if there is a corresponding
        opening [ available or not.

        Why not maintain a separate counter for the different types of parenthesis?
        This doesn't work because the relative placement of the parenthesis also matters here. e.g.: [{]
        If we simply keep counters here, then as soon as we encounter the closing square bracket ], we would know
        there is an unmatched opening square bracket available as well. But, the closest unmatched opening bracket
        available is a curly bracket { and not a square bracket [ and hence the counting approach breaks here.

        An interesting property about a valid parenthesis expression is that a sub-expression of a valid expression
        should also be a valid expression. (Not every sub-expression)

        What if whenever we encounter a matching pair of parenthesis in the expression, we simply remove it from the
        expression? If it is a valid expression, we would be left with an empty string in the end.

        The stack data structure can come in handy here in representing this recursive structure of the problem. We
        can't really process this from the inside out because we don't have an idea about the overall structure. But,
        the stack can help us process this recursively i.e. from outside inwards.

        If we encounter an opening bracket, we simply push it onto the stack. This means we will process it later, let
        us simply move onto the sub-expression ahead.

        If we encounter a closing bracket, then we check the element on top of the stack. If the element at the top of
        the stack is an opening bracket of the same type, then we pop it off the stack and continue processing. Else,
        this implies an invalid expression.

        In the end, if we are left with a stack still having elements, then this implies an invalid expression.

    Time complexity: O(N)
    Space complexity: O(N), we push all opening brackets onto the stack and in the worst case we will end up pushing
    all the brackets onto the stack. e.g. ((((((((((
    """
    brackets = {'(': ')', '{': '}', '[': ']'}
    stack = []
    for c in s:
        if c in brackets:
            stack.append(c)
        elif not stack or brackets[stack.pop()] != c:
            return False
    return not stack


def is_valid_v2(s):
    """ A similar stack-based solution.

        Whenever we encounter an opening bracket, we push its counterpart closing bracket to the stack (as if
        anticipating the closing bracket). If a closing bracket is met, we check if the element sitting on the top of the
        stack is the same bracket, since we already anticipated the current closing bracket. If not, the expression is
        invalid.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    brackets = {'(': ')', '{': '}', '[': ']'}
    stack = []
    for c in s:
        if c in brackets:
            stack.append(brackets[c])
        elif not stack or stack.pop() != c:
            return False
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
            self.assertEqual(result, is_valid_v2(test_string))


if __name__ == '__main__':
    unittest.main()
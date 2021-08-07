""" Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses. """

import unittest2 as unittest


def generate_parenthesis_v1(n):
    """ Instead of adding '(' or ')' every time, let's only add them when we know it will remain a valid sequence.
        We can do this by keeping track of the number of opening and closing brackets we have placed so far.
        We can start an opening bracket if we still have one (of n) left to place. And we can start a closing bracket
        if it would not exceed the number of opening brackets.
        The goal is to print a string of '(' ,')' in certain order. The length of the string is 2n. The constraints are
        that '('s need to match ')'s. Without constraints, we just simply print out '(' or ')' until length hits 2n.
        Let’s add in constraints now. We need to interpret the meanings of constraints. First, the first character
        should be '('. Second, at each step, we can either print '(' or ')', but print ')' only when there are more
        '('s than ')'s. Stop printing out '(' when the number of '(' s hits n.
        The main concept is that in a parenthesis balanced string, count of ')' must be less than or equal to count of
        '(' for every prefix of the string. A parentheses balanced string (of size 2N) must have N number of '(' and N
        number of ')'. We go on adding '(' before ')' for every recursive state string until count of '(' becomes equal
        to N. Then we start adding ')' only on a condition that the count of ')' is less than the count of '('. These
        two conditions will always produce a balanced string.
        The key to all backtracking problems is "to choose". We have to choose between many options and then come back
        to choose again. In this problem, we have to choose between left and right parenthesis.
        Visualization: n = 2
        backtrack(0, 0, '')  # open < 2, '(' can be inserted
        backtrack(1, 0, '(')  # open < 2, '(' can be inserted
                backtrack(2, 0, '((')  # close < open, ')' can be inserted
                        backtrack(2, 1, '(()')  # close < open, ')' can be inserted
                                backtrack(2, 2, '(())') # open == close == 2. We got '(())' and we append it to result
                backtrack(1, 1, '()')  # close < open, ')' can be inserted
                        backtrack(2, 1, '()(') # open < 2, '(' can be inserted
                                backtrack(2, 2, '()()') # open == close == 2. We got '(())' and we append it to result
                        backtrack(1, 2, '())') # will just return as close > open
        backtrack(0, 1, ')') # will just return as close > open
        Another example with n = 3:
        (
            ((
                (((
                    ((()
                        ((())
                            ((()))
                (()
                    (()(
                        (()()
                            (()())
                    (())
                        (())(
                            (())()
            ()
                ()(
                    ()((
                        ()(()
                            ()(())
                    ()()
                        ()()(
                            ()()()
    Time complexity: O(2^(2n)) = O(4^n). The way to think about the runtime of backtracking algorithms is O(b^d), where
    b is the branching factor and d is the maximum depth of recursion.
    Backtracking is characterized by a number of decisions b that can be made at each level of recursion. If we
    visualize the recursion tree, this is the number of children each internal node has. We can also think of b as
    standing for 'base', which can help remember that b is the base of the exponential.
    If we can make b decisions at each level of recursion, and we expand the recursion tree to d levels (i.e.: each
    path has a length of d), then we get b^d nodes. Since backtracking is exhaustive and must visit each one of these
    nodes, the runtime is O(b^d).
    Space complexity: O(2n) = O(n), for the call stack
    """

    def backtrack(open, close, s):
        if open == close == n:  # We have used all left and right parentheses necessary within constraints up to this
            # point. Therefore, the answer we add will be a valid paren string. We can add this answer and then
            # backtrack so the previous call can exhaust more possibilities and express more answers, and then return
            # to its caller, etc. etc.
            # Yeah, this is what backtracking is all about.
            res.append(s)
        if open < n:  # Can we insert a left parenthesis? Only if we have lefts remaining to insert at this point in
            # the recursion
            backtrack(open + 1, close, s + '(')
        if open > close:  # Can we insert a right parenthesis? Only if the number of placed left parenthesis is greater
            # than the number of placed right parenthesis. This stops us from constructing a string like ()).
            backtrack(open, close + 1, s + ')')

    res = []
    backtrack(0, 0, '')
    return res


class Test(unittest.TestCase):
    data = [(3, [
        '((()))',
        '(()())',
        '(())()',
        '()(())',
        '()()()'
    ])]

    def test_generate_parenthesis(self):
        for test_pairs, result in self.data:
            self.assertEqual(result, generate_parenthesis_v1(test_pairs))


if __name__ == '__main__':
    unittest.main()

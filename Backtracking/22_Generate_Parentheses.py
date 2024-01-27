""" Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=sz1qaKt0KGQ
# Video explanation: https://www.youtube.com/watch?v=s9fokUqJ76A
def generate_parenthesis_v1(n):
    """ The brute force approach involves generating all possible strings of length 2n, and then verifying their
         validity. As a valid combination of parentheses of length 2n must have n left parentheses, with each of them
         matched to one of the n right parentheses to its right, we can keep track of a parameter called left_count.
         left_count represents the number of left parentheses that have not been matched by any right parentheses.
         If we encounter a left parenthesis, we increment left_count by 1. If we encounter a right parenthesis, we
         decrement left_count by 1 as it can match and "offset" one previous left parenthesis. However, the value of
         left_count cannot be negative, which would mean that there is a right parenthesis without a corresponding left
         parenthesis to its left.

         Generating all possible strings of length 2n and checking each one is simple but inefficient, as it generates
         many invalid strings that must be checked.

         A better approach is to use backtracking to generate only valid strings. This involves recursively building
         strings of length 2n and checking their validity as we go. In case the current string is invalid, we will not
         continue the recursive process on it. Instead, we will backtrack to the previous valid string on the recursive
         path.

        Instead of adding '(' or ')' every time, let's only add them when we know it will remain a valid sequence.
        This ensures that as each additional character is added, the resulting string has the potential to be
        completed to a string with n pairs of matched parens.
        We can do this by keeping track of the number of opening and closing brackets we have placed so far.

            - If we add a left parens, and still want to complete the string to a string with n pairs of matched parens,
               it must be that the number of left parens we placed so far is less than n.

            - If we add a right parens, and still want to complete the string to a string with n pairs of matched parens,
               it must be that the number of left parens we placed so far is greater than the number of right parens
               (i.e., there are unmatched left parens in the string).

        The goal is to print a string of '(' ,')' in certain order. The length of the string is 2n. The constraints are
        that '('s need to match ')'s. Without constraints, we just simply print out '(' or ')' until length hits 2n.
        Let’s add in constraints now. We need to interpret the meanings of constraints. First, the first character
        should be '('. Second, at each step, we can either print '(' or ')', but print ')' only when there are more
        '('s than ')'s. Stop printing out '(' when the number of '(' s hits n.

        The main concept is that in a parenthesis-balanced string, the count of ')' must be less than or equal to the
        count of '(' for EVERY PREFIX of the string. A parentheses-balanced string (of size 2N) must have N number of
        '(' and N number of ')'. We go on adding '(' before ')' for every recursive state string until the count of '('
        becomes equal to N. Then we start adding ')' only on the condition that the count of ')' is less than the count
        of '('. These two conditions will always produce a balanced string.

        The key to all backtracking problems is to "choose". We have to choose between many options and then come back
        to choose again. In this problem, we have to choose between left and right parenthesis.

        Example: n = 2

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

        Example: n = 3
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
    Space complexity: O(2n) = O(n), for the call stack. Each recursive call either adds a left parenthesis or a right
    parenthesis, and the total number of parentheses is 2n. Therefore, at most O(n) levels of recursion will be created.
    """

    def dfs(left, right, path):
        if left == right == n:
            # We have used all left and right parentheses necessary within constraints up to this point. Therefore,
            # the answer we add will be a valid parenthesis string. We can add this answer and then backtrack so the
            # previous call can exhaust more possibilities and express more answers, and then return to its caller,
            # etc. etc. Yeah, this is what backtracking is all about.
            res.append(path)
        if left < n:
            # Can we insert a left parenthesis? Only if we have lefts remaining to insert at this point in the recursion
            dfs(left + 1, right, path + '(')
        if right < left:
            # Can we insert a right parenthesis? Only if the number of placed left parenthesis is greater than the
            # number of placed right parenthesis. This stops us from constructing a string like ()).
            dfs(left, right + 1, path + ')')

    res = []
    dfs(0, 0, '')
    return res


def generate_parenthesis_v2(n):
    """ Same algorithm but with "explicit" backtracking. Also, expensive string concatenation can be avoided.

    Time complexity: O(4^n)
    Space complexity: O(n)
    """
    def dfs(open, close, path):
        if open == close == n:
            res.append(''.join(path))
        if open < n:
            path.append('(')
            dfs(open + 1, close, path)
            path.pop()
        if open > close:
            path.append(')')
            dfs(open, close + 1, path)
            path.pop()

    res = []
    dfs(0, 0, [])
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
            self.assertEqual(result, generate_parenthesis_v2(test_pairs))


if __name__ == '__main__':
    unittest.main()

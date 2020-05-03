""" Given a string containing only three types of characters: '(', ')' and '*', write a function to check whether this
string is valid. We define the validity of a string by these rules:
Any left parenthesis '(' must have a corresponding right parenthesis ')'.
Any right parenthesis ')' must have a corresponding left parenthesis '('.
Left parenthesis '(' must go before the corresponding right parenthesis ')'.
'*' could be treated as a single right parenthesis ')' or a single left parenthesis '(' or an empty string.
An empty string is also valid. """

import unittest2 as unittest


def check_valid_string_v1(s):
    """ The idea of recursion is very simple: increment 'open' when we encounter '(' and decrement it when we see a ')'.
        Otherwise, we just need to consider 3 cases: skip * symbol or substitute it with either closing or opening
        parenthesis, i.e. increase or decrease open.
        Check for case when we want to decrement zero-valued open, that means that we want to put ) before (, which is
        not acceptable.
    Time complexity: O(N^2), O(3^N) + memoization, proportional to the size of the hash map which is open * index where
    both factors are proportional to the size of the input string
    Space complexity: O(N)
    """

    def dfs(open, index):
        if index == n:
            return open == 0
        if open < 0:
            return False
        if (open, index) not in memo:
            if s[index] == '(':
                memo[(open, index)] = dfs(open + 1, index + 1)
            elif s[index] == ')':
                memo[(open, index)] = dfs(open - 1, index + 1)
            else:
                memo[(open, index)] = dfs(open + 1, index + 1) or dfs(open - 1, index + 1) or dfs(open, index + 1)
        return memo[(open, index)]

    n, memo = len(s), {}
    return dfs(0, 0)


class Test(unittest.TestCase):
    data = [('()', True), ('(*)', True), ('(*))', True)]

    def test_check_valid_string(self):
        for test_s, result in self.data:
            self.assertEqual(result, check_valid_string_v1(test_s))


if __name__ == '__main__':
    unittest.main()

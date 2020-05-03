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


# Great visualization: https://bit.ly/3bZDp0n

def check_valid_string_v2(s):
    """ Scan the string from left to right, and record counts of unpaired ‘(’ for all possible cases. For ‘(’ and ‘)’,
        it is straightforward, just increment and decrement all counts, respectively.
        When the character is '*', there are three cases, ‘(’, empty, or ‘)’. We can think of those three cases as
        three branches in the ongoing route. During the process, we use 2 variables:
        min_unpaired_left: counts the minimum open parenthesis, which means the number of unbalanced '(' that MUST be
        paired.
        max_unpaired_left: counts the maximum open parenthesis, which means the maximum number of unbalanced '(' that
        COULD be paired.
        We basically count the number of ')' we are waiting for, and it's equal to the number of open parenthesis.
        This number will be in a range and we count it as [min_unpaired_left, max_unpaired_left].
        The string is valid for 2 condition:
            1- 'max_unpaired_left' will never be negative
            2- 'min_unpaired_left' is 0 at the end
        Take s =(**()) as an example. There are 6 characters:
        At step 0, only one count = 1.
        At step 1, the route will be diverted into three branches, so there are three counts: 1 - 1, 1, 1 + 1 which is
        0, 1, 2, for ‘)’, empty and ‘(’ respectively.
        At step 2, each route is diverged into three routes again, so there will be 9 possible routes now.
            For count = 0, it will be diverted into 0 – 1, 0, 0 + 1, which is -1, 0, 1, but when the count is -1, that
            means there are more ‘)’s than ‘(’s, and we need to stop early at that route, since it is invalid. We end
            up with 0, 1.
            For count = 1, it will be diverted into 1 – 1, 1, 1 + 1, which is 0, 1, 2
            For count = 2, it will be diverted into 2 – 1, 2, 2 + 1, which is 1, 2, 3
        To summarize step 2, we end up with counts of 0, 1, 2, 3
        At step 3, increment all counts --> 1, 2, 3, 4
        At step 4, decrement all counts --> 0, 1, 2, 3
        At step 5, decrement all counts --> -1, 0, 1, 2. The route with count -1 is invalid, so stop early at that
        route. Now we have 0, 1, 2.
        In the very end, we find that there is a route that can reach count == 0, which means all ‘(’ and ‘)’ are
        cancelled out. So, the original string is valid.
        Another finding is that the counts of unpaired ‘(’ for all valid routes are consecutive integers. So we only
        need to keep a lower (min_unpaired_left) and upper (max_unpaired_left) bound of that consecutive integers to
        save space.
        'max_unpaired_left' considers each '*' as '(', which should never be negative.
        'min_unpaired_left' considers each '*' as ')' as much as possible (treat it as empty string if
        min_unpaired_left < 0 --> max(min_unpaired_left - 1, 0)).
        In the end, 'min_unpaired_left' should be 0. If it's larger than 0, it means even if we consider EVERY '*' as
        ')', there is still some '(' left unpaired.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    min_unpaired_left = max_unpaired_left = 0
    for c in s:
        if c == '(':
            min_unpaired_left += 1
            max_unpaired_left += 1
        elif c == ')':
            min_unpaired_left = max(0, min_unpaired_left - 1)
            max_unpaired_left -= 1
        else:
            min_unpaired_left = max(0, min_unpaired_left - 1)
            max_unpaired_left += 1
        if max_unpaired_left < 0:  # Number of ')' is more than available '( ' and '*'
            return False
    return min_unpaired_left == 0  # If we wait for no ')' at the end, then we are good


class Test(unittest.TestCase):
    data = [('()', True), ('(*)', True), ('(*))', True)]

    def test_check_valid_string(self):
        for test_s, result in self.data:
            self.assertEqual(result, check_valid_string_v1(test_s))
            self.assertEqual(result, check_valid_string_v2(test_s))


if __name__ == '__main__':
    unittest.main()

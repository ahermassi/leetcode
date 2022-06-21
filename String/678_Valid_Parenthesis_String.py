""" Given a string containing only three types of characters: '(', ')' and '*', write a function to check whether this
string is valid. We define the validity of a string by these rules:
Any left parenthesis '(' must have a corresponding right parenthesis ')'.
Any right parenthesis ')' must have a corresponding left parenthesis '('.
Left parenthesis '(' must go before the corresponding right parenthesis ')'.
'*' could be treated as a single right parenthesis ')' or a single left parenthesis '(' or an empty string.
An empty string is also valid. """

import unittest2 as unittest


def check_valid_string_v1(s):
    """ Top-Down Dynamic Programming (recursion + memoization).

        The idea of recursion is very simple: increment 'open' when we encounter '(' and increment 'close' when we
         see a ')'. Otherwise, we just need to consider 3 cases: Skip '*' symbol or substitute it with either closing or
         opening parenthesis.

        Check for the case when we want to decrement zero-valued 'open', that means that we want to put ')' before
        '(' which is not acceptable.

    Time complexity: O(N^2), O(3^N) + memoization
    Space complexity: O(N)
    """

    def dfs(index, open, close):
        if index == n:
            return open == close
        if open < close:
            return False
        if (index, open, close) not in memo:
            cur_char = s[index]
            if cur_char == '(':
                memo[(index, open, close)] = dfs(index + 1, open + 1, close)
            elif cur_char == ')':
                memo[(index, open, close)] = dfs(index + 1, open, close + 1)
            else:
                memo[(index, open, close)] = dfs(index + 1, open + 1, close) or dfs(index + 1, open, close + 1) \
                                             or dfs(index + 1, open, close)
        return memo[(index, open, close)]

    n, memo = len(s), {}
    return dfs(0, 0, 0)


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


def check_valid_string_v3(s):
    """ The basic idea is to track the index of the left bracket and star position.
        Step 1: Here we consider '*' as an opening parenthesis IF open stack becomes empty.
        Push all the indices of the star and left bracket to their stack respectively. Once a right bracket comes try
        to match it, so pop left bracket stack first if it is not empty. If the left bracket stack is empty, pop the
        star stack if it is not empty. A false return can be made if both stacks are empty.
        Step 2: Here we consider '*' as a closed parenthesis. Now attention is paid to the remaining stuff in these two
        stacks. Note that the left bracket CANNOT appear after the star as there is NO way to balance the bracket. In
        other words, if index at top of open stack > index at top of ast stack, it means there was no '*' after the
        last '(' , so return false. Otherwise, pop out each from the left bracket and star stack.
        A correct sequence should have an empty left bracket stack, which means we were able to balance the complete
        string.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    open, star = [], []
    for i, c in enumerate(s):
        if c == '(':
            open.append(i)
        elif c == '*':
            star.append(i)
        elif open:
            open.pop()
        elif star:
            star.pop()
        else:
            return False
    while open and star:
        if open.pop() > star.pop():
            return False
    return not open


class Test(unittest.TestCase):
    data = [('()', True), ('(*)', True), ('(*))', True)]

    def test_check_valid_string(self):
        for test_s, result in self.data:
            self.assertEqual(result, check_valid_string_v1(test_s))
            self.assertEqual(result, check_valid_string_v2(test_s))
            self.assertEqual(result, check_valid_string_v3(test_s))


if __name__ == '__main__':
    unittest.main()

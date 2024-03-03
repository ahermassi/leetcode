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
          see a ')'. Otherwise, we just need to consider 3 cases: skip '*' or substitute it with either closing or
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
                res = dfs(index + 1, open + 1, close)
            elif cur_char == ')':
                res = dfs(index + 1, open, close + 1)
            else:
                res = dfs(index + 1, open + 1, close) or dfs(index + 1, open, close + 1) or dfs(index + 1, open, close)
            memo[(index, open, close)] = res
        return memo[(index, open, close)]

    n, memo = len(s), {}
    return dfs(0, 0, 0)


# Video explanation: https://www.youtube.com/watch?v=QhPdNS143Qg
# Great visualization: https://bit.ly/3bZDp0n
def check_valid_string_v2(s):
    """ Let's assume the string consists of only '(' and ')' brackets. When checking whether the string is valid, we
         only care about the "balance": the number of extra, open left brackets as we parsed through the string.

         For example, when checking whether '(()())' is valid, we have a balance of 1, 2, 1, 2, 1, 0 as we parse through
         the string: '(' has 1 left bracket, '((' has 2, '(()' has 1, and so on. This means that after parsing the first
         few symbols, (which may include asterisks,) we only need to keep track of what the balance could be.

         If we have the string '(***)', then as we parse each symbol, the set of possible values for the balance is:
            - [1] for '('
            - [0, 1, 2] for '(*'
            - [0, 1, 2, 3] for '(**'
            - [0, 1, 2, 3, 4] for '(***'
            - [0, 1, 2, 3] for '(***)'.

         Furthermore, these possible values of the balance always form a contiguous interval. Thus, we only need to
         know the lower and upper bounds of this interval. That is, we would keep those intermediate states as
         [lo, hi] = [1, 1], [0, 2], [0, 3], [0, 4], [0, 3].

         Scan the string from left to right and keep a count of the smallest and largest possible number of open left
         brackets ‘(’ for all possible cases.
         If we encounter ‘(’ or ‘)’, it is straightforward, just increment or decrement the counters, respectively.
         When the character is '*', there are three substitution cases: ‘(’, empty, or ‘)’. We can think of those three
         cases as three branches in the ongoing route.

         During the process, we use the following variables for the counters:

                - min_unmatched_left: the lower bound of open parenthesis, which is the number of unmatched '(' that
                   MUST be paired.

                - max_unmatched_left: the upper bound of open parenthesis, which is the maximum number of unmatched
                   '(' that COULD be paired.

          We basically count the number of ')' we are waiting for, and it's equal to the number of open parenthesis.
          This number will be in a range, and we represent it as [min_unmatched_left, max_unmatched_left].

          'min_unmatched_left' considers each '*' as ')' as much as possible.
          'max_unmatched_left' considers each '*' as '('.
          In the end, 'min_unmatched_left' should be 0. If it's larger than 0, it means even if we consider EVERY '*' as
          ')', there is still some '(' left unmatched.

          The input string is valid if two conditions are met:

             1- max_unmatched_left is never negative. If max_unmatched_left becomes negative, that means, with all the
                  '(' and '*' we have encountered, there are more ')'.
                  Example: s= "())". max_unmatched_left would be less than 0 because we have two ' )' and only one '('.
                  Irrespective of how many '*' we have, this sequence is already invalid, hence we return false.

             2- min_unmatched_left is 0 at the end

         Note that every time during the process min_unmatched_left falls below zero, it's set back to zero.
         If min_unmatched_left < 0, it means we have taken some extra '*' as ')' which has caused the current "state" to
         become invalid, i.e. no opening bracket is there to balance the closing bracket. So, we can assume few of the
         '*'s as empty string.
         If min_unmatched_left < 0, it means that this replacement results in more ')' than '(', so it should be
         avoided. To avoid it, we simply reset min_unmatched_left to 0 which implies we only replace '*' with '(' or
         empty string.

         The input string can be invalid if there are unbalanced parentheses. There are two such patterns:

             1- Too many ')' at any instant when parsing the string left to right.
                  max_unmatched_left deals with this condition. Since it treats each '*' as '(', then any time the number
                  of ')' exceeds maximum possible '(', the string is flagged as invalid.

             2- At least one '(' at the end doesn't have a matching ')'.
                  min_unmatched_left deals with this condition. Since it treats each '*' as ')' AND clips its own value
                  at 0, therefore it doesn't care if there are too many ')' (saturated at 0). But, if there are any '('
                  with no matching ')' at the end, then it invalidates the string.

         min_unmatched_left and max_unmatched_left are complementary as they deal with two scenarios that can invalidate
         the string.

         Example: s =(**())

         At step 0, only one count = 1.

         At step 1, the route diverges into three branches, so there are three counts: 1 - 1, 1, 1 + 1 which is
         0, 1, 2, for ‘)’, empty and ‘(’ respectively.

         At step 2, each route diverges into three routes again, so there will be 9 possible routes now.
             For count = 0, it will be 0 – 1, 0, 0 + 1, which is -1, 0, 1, but when the count is -1, that means there
             are more ‘)’s than ‘(’s, which is '())', and should be avoided. We end up with 0, 1.
             For count = 1, it will be 1 – 1, 1, 1 + 1, which is 0, 1, 2
             For count = 2, it will be 2 – 1, 2, 2 + 1, which is 1, 2, 3
         To summarize step 2, we end up with counts of 0, 1, 2, 3

         At step 3, increment all counts --> 1, 2, 3, 4

         At step 4, decrement all counts --> 0, 1, 2, 3

         At step 5, decrement all counts --> -1, 0, 1, 2. The route with count -1 is invalid, so avoid it. Now we have
         0, 1, 2.

         In the very end, we find that there is a route that can reach count == 0, which means all ‘(’ and ‘)’ are
         cancelled out. So, the input string is valid.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    min_unmatched_left = max_unmatched_left = 0
    for c in s:
        if c == '(':
            min_unmatched_left += 1
            max_unmatched_left += 1
        elif c == ')':
            min_unmatched_left -= 1
            max_unmatched_left -= 1
        else:
            min_unmatched_left -= 1 # '*' is used as ')'
            max_unmatched_left += 1 # '*' is used as '('
        if max_unmatched_left < 0:
            # Number of ')' is more than available '( ' and '*'. We can’t accommodate current right braces with current
            # left braces and asterisks. With all the '(' and '*' we have encountered, there are more ')'.
            return False
        if min_unmatched_left < 0:
            # min_unmatched_left can become negative because we COULD in theory use a '*' as a ')' even when there is
            # no previous '(' to match it. However, we don't want to do this because it would give us an invalid
            # string. This check serves as a guarantee that we won't ever perform this unwanted '*' substitution.
            min_unmatched_left = 0
    return min_unmatched_left == 0  # If we wait for no ')' at the end, then we are good


def check_valid_string_v3(s):
    """ Stack-based solution.

        The basic idea is to track the index of the left bracket and asterisk. Push all the indices of the asterisks and
        left brackets to their stacks, respectively.

        Step 1: When we encounter a right bracket, we try to match it. So, pop left bracket stack first if it is not
        empty. If the left bracket stack is empty, pop the asterisk stack if it is not empty. Here we consider '*' as
        an open parenthesis that can be match a closing parenthesis. False can be returned if both stacks are empty.

        Step 2: Here we consider '*' as a closing parenthesis. Attention is paid to the remaining stuff in the two
        stacks. Note that the left bracket CANNOT appear after the asterisk as there is NO way to balance the bracket.
        In other words, if index at top of left stack > index at top of asterisk stack, it means there was no '*' after
        the last '(' , so return false. Otherwise, pop out each from the left bracket and asterisk stack.

        A correct sequence should have an empty left bracket stack, which means we were able to balance the complete
        string.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    left, asterisk = [], []
    for i, c in enumerate(s):
        if c == '(':
            left.append(i)
        elif c == '*':
            asterisk.append(i)
        elif left:
            left.pop()
        elif asterisk:
            asterisk.pop()
        else:  # We can't match the current ')'
            return False
    # So far, we have cleared all the ')' using '(' accordingly. But, we may have more '(' and '*' than ')'. In the
    # remaining part, if there is any '(' after '*', we return False. We can only close an '(' if there is an '*'
    # that occurs at a greater/later index.
    while left and asterisk:
        if left.pop() > asterisk.pop():
            return False
    return not left


class Test(unittest.TestCase):
    data = [('()', True), ('(*)', True), ('(*))', True)]

    def test_check_valid_string(self):
        for test_s, result in self.data:
            self.assertEqual(result, check_valid_string_v1(test_s))
            self.assertEqual(result, check_valid_string_v2(test_s))
            self.assertEqual(result, check_valid_string_v3(test_s))


if __name__ == '__main__':
    unittest.main()

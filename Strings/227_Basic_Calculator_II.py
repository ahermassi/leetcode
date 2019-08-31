""" Implement a basic calculator to evaluate a simple expression string.
The expression string contains only non-negative integers, +, -, *, / operators and empty spaces . The integer division
should truncate toward zero. """

import unittest2 as unittest


def calculate(s):
    """ This solution is stack based. The stack is used to hold temporary results for partial expressions with lower
        precedence levels, which are + and -. This helps delaying calculations until an operator with a higher
        precedence is met.
        For example, let's look at '22 - 31 * 52 + 22'.
        First, num variable is used to accumulate the integer value of operands. Here, the first value of num will hold
        22. When '-' is encountered, we look at the last operator which is '+' by default. Since '+' is a lower
        precedence operator, push num (22) and let it wait, and change last operator to '-'. Again, num holds the value
        of next operand 31, and '*' is encountered. last operator is '-', so push -num (-31) to the stack and change
        last operator to *. Now num = 52 is processed and '+' is encountered. Since last operator is '*' which has
        higher precedence than '+', push the result of num = 52 multiplied by last element in the stack = -31 (after
        popping it), and change last operator to '+'. Now last operand is read i.e. num = 22, and we are at the end of
        the string, and since last operator was '+' then push +num = 22.
        Finally, the stack content is just 22, the multiplication of -31 by 52, and 22. The result is sum of the stack.
    Time complexity: O(N) where N is the length of s
    Space complexity: O(N)
     """
    num, stack, last_operator = 0, [], '+'
    for i in range(len(s)):
        if s[i].isdigit():
            num = num * 10 + int(s[i])
        if s[i] in '+-*/' or i == len(s) - 1:
            if last_operator == '+':
                stack.append(num)
            elif last_operator == '-':
                stack.append(-num)
            elif last_operator == '*':
                stack.append(stack.pop() * num)
            else:
                stack.append(int(float(stack.pop()) / num))
            num = 0
            last_operator = s[i]
    return sum(stack)


class Test(unittest.TestCase):
    data = [('3+2*2', 7), (' 3+5 / 2 ', 5)]

    def test_calculate(self):
        for test_string, result in self.data:
            self.assertEqual(result, calculate(test_string))


if __name__ == '__main__':
    unittest.main()

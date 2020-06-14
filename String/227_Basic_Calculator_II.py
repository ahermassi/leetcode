""" Implement a basic calculator to evaluate a simple expression string.
The expression string contains only non-negative integers, +, -, *, / operators and empty spaces . The integer division
should truncate toward zero. """

import unittest2 as unittest


def calculate_v1(s):
    """ This solution is stack based. The stack is used to hold temporary results for partial expressions with lower
        precedence levels, which are + and -. This helps delaying calculations until an operator with a higher
        precedence is met.
        Every time an operation sign is met, 'last_operator' variable tells us what type of a PREVIOUS operation the
        last integer we read is part of: 11 - 2 * 5: say we read 11 and then encounter '-', we look at 'last_operator'
        which is '+' by default, so we know that 11 is part of an addition operation (0 + 11). Then we read 2 and meet
        '*', we look at 'last_operator' which was assigned to '-', so we know that 2 is part of a subtraction operation
        (11 - 2).
        For example, let's look at '22 - 31 * 52 + 22'.
        First, ''num variable is used to accumulate the integer value of operands. Here, the first value of 'num' will
        hold 22. When '-' is encountered, we look at the last operator which is '+' by default. Since '+' is a lower
        precedence operator, push num (22) and let it wait, and change last operator to '-'. Again, 'num' holds the
        value of next operand 31, and '*' is encountered. Last operator is '-', so push -num (-31) to the stack and
        change last operator to *. Now num = 52 is processed and '+' is encountered. Since last operator is '*' which
        has higher precedence than '+', push the result of num = 52 multiplied by last element in the stack = -31
        (after popping it), and change last operator to '+'. Now last operand is read i.e. num = 22, and we are at the
        end of the string, and since last operator was '+' then push +num = 22.
        Finally, the stack content is just 22, the multiplication of -31 by 52, and 22. The result is sum of the stack.
    Time complexity: O(N) where N is the length of s
    Space complexity: O(N)
    """
    num, stack, last_operator = 0, [], '+'
    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
        if c in '+-*/' or i == len(s) - 1:
            if last_operator == '+':  # We have a new operation sign in hand and the accumulated integer 'num' is
                # part of a PREVIOUS addition operation
                stack.append(num)
            elif last_operator == '-':
                stack.append(-num)
            elif last_operator == '*':  # We have a new operation sign in hand and the accumulated integer 'num' is
                # part of a PREVIOUS multiplication operation
                stack.append(stack.pop() * num)  # Multiply 'num' with the previously accumulated integer that's been
                # waiting in the stack since multiplication is a higher level operation
            else:  # We have a new operation sign in hand and the accumulated integer 'num' is part of a PREVIOUS
                # division operation
                stack.append(int(stack.pop() / num))  # Perform the division of the previously accumulated integer
                # that's been waiting in the stack by the accumulated integer 'num' since division is a higher level
                # operation
            num = 0
            last_operator = c
    return sum(stack)


# Check out:
# https://leetcode.com/problems/basic-calculator-ii/discuss/63088/Explanation-for-Java-O(n)-time-and-O(1)-space-solution

def calculate_v2(s):
    """ Same logic but constant space.
        To have O(1) space solution, we have to drop the stack. To see why we can drop it, we need to reexamine the main
        purpose of the stack: it is used to hold temporary results for partial expressions with lower precedence.
        We only have two precedence levels: lower level with '+' and '-' operations and higher level with '*' and '/'
        operations. So the stack can be replaced by two variables, one for the lower level and the other for the higher
        level.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    num, last_operator = 0, '+'
    low = high = 0  # 'high' variable acts as an accumulator of the partial results that used to sit in the stack
    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
        if c in '+-*/' or i == len(s) - 1:
            if last_operator == ''+'':
                high += low
                low = num
            elif last_operator == '-':
                high += low
                low = -num
            elif last_operator == '*':
                low *= num
            else:
                low = int(low / num)
            num = 0
            last_operator = c
    return high + low


class Test(unittest.TestCase):
    data = [('3+2*2', 7), (' 3+5 / 2 ', 5)]

    def test_calculate(self):
        for test_string, result in self.data:
            self.assertEqual(result, calculate_v1(test_string))
            self.assertEqual(result, calculate_v2(test_string))


if __name__ == '__main__':
    unittest.main()

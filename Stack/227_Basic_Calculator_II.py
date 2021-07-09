""" Implement a basic calculator to evaluate a simple expression string.
The expression string contains only non-negative integers, +, -, *, / operators and empty spaces . The integer division
should truncate toward zero. """

import unittest2 as unittest


def calculate_v1(s):
    """ This solution is stack based. The stack is used to hold temporary results for partial expressions with lower
        precedence levels, which are + and -. This helps delaying calculations until an operator with a higher
        precedence is met.
        We know that there could be 4 types of operations: addition (+), subtraction (-), multiplication (*) and
        division (/). Without parenthesis, we know that, multiplication (*) and division (/) operations would always
        have higher precedence than addition (+) and subtraction (-) based on operator precedence rules:

            4 + 3 * 5               4 + 3 - 5               4 * 3 / 5               4 * 3 - 5
            4 +  15  = 19             7   - 5 = 2             12  / 5 = 2             12  - 5 = 7

        If we look at the above examples, we can make the following observations:

            - If the current operation is addition (+) or subtraction (-), then the expression is evaluated based on
              the precedence of the next operation.
              In example 1, 4 + 3 is evaluated later because the next operation is multiplication (3 * 5) which has
              higher precedence. But, in example 2, 4 + 3 is evaluated first because the next operation is subtraction
              (3 - 5) which has equal precedence.
            - If the current operator is multiplication (*) or division (/), then the expression is evaluated
              irrespective of the next operation. This is because in the given set of operations (+,-,*,/), the * and /
              operations have the highest precedence and therefore must be evaluated first.
              In the above examples 2 and 3, 4 * 3 is always evaluated first irrespective of the next operation.

        Using this intuition let's look at the algorithm to implement the problem.
        Scan the input string s from left to right and evaluate the expressions based on the following rules:
            - If the current character is a digit 0-9 ( operand ), add it to the number 'num'.
            - Otherwise, the current character must be an operation (+,-,*, /). Evaluate the expression based on the
              type of LAST operation:
                1) Addition (+) or Subtraction (-): We must evaluate the expression later based on the next operation.
                   So, we must store 'num' to be used later. Let's push 'num' to the Stack.
                   The last pushed number in the stack would be popped out first for evaluation. In addition, when we
                   pop from the stack and evaluate this expression in the future, we need a way to determine if the
                   LAST operation was Addition (+) or Subtraction (-). To simplify our evaluation, we can push -num to
                   the stack if the last operation was subtraction (-) and assume that the operation for all the values
                   in the stack is addition (+). This works because (a - num) is equivalent to (a + (-num)).
                2) Multiplication (*) or Division (/): Pop the top values from the stack and evaluate the current
                   expression. Push the evaluated value back to the stack.
        Once the string is scanned, pop from the stack and add to the result.

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
    Time complexity: O(N), where N is the length of s
    Space complexity: O(N)
    """
    n = len(s)
    num, stack, last_operator = 0, [], '+'
    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
        if c in '+-*/' or i == n - 1:
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
                stack.append(int(float(stack.pop()) / num))  # Perform the division of the previously accumulated
                # integer that's been waiting in the stack by the accumulated integer 'num' since division is a higher
                # precedence operation
            num = 0
            last_operator = c
    return sum(stack)


# Check out:
# https://leetcode.com/problems/basic-calculator-ii/discuss/63088/Explanation-for-Java-O(n)-time-and-O(1)-space-solution

def calculate_v2(s):
    """ In the previous approach, we used a stack to track the values of the evaluated expressions. In the end, we pop
        all the values from the stack and add to the result. Instead of that, we could add the values to the result
        beforehand and keep track of the last calculated number, thus eliminating the need for the stack.
        Instead of using a stack, we use a variable 'prev_num' to track the value of the last evaluated expression.
        If the operation is Addition (+) or Subtraction (-), add the 'prev_num' to the result instead of pushing it to
        the stack. The 'prev_num' would be updated to 'cur_num' for the next iteration.
        If the operation is Multiplication (*) or Division (/), we must evaluate the expression (prev_num * cur_num)
        and update the 'prev_num' with the result of the expression. This would be added to the result after the entire
        string is scanned.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(s)
    cur_num = prev_num = 0
    last_operator = '+'
    res = 0
    for i, c in enumerate(s):
        if c.isdigit():
            cur_num = cur_num * 10 + int(c)
        if i == n - 1 or c in '+-/*':
            if last_operator == '+':
                res += prev_num
                prev_num = cur_num
            elif last_operator == '-':
                res += prev_num
                prev_num = -cur_num
            elif last_operator == '*':
                prev_num *= cur_num
            else:
                prev_num = int(float(prev_num) / cur_num)
            last_operator = c
            cur_num = 0
    return res + prev_num


class Test(unittest.TestCase):
    data = [('3+2*2', 7), (' 3+5 / 2 ', 5)]

    def test_calculate(self):
        for test_string, result in self.data:
            self.assertEqual(result, calculate_v1(test_string))
            self.assertEqual(result, calculate_v2(test_string))


if __name__ == '__main__':
    unittest.main()

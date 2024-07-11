""" Implement a basic calculator to evaluate a simple expression string.
The expression string contains only non-negative integers, +, -, *, / operators and empty spaces . The integer division
should truncate toward zero. """

import unittest2 as unittest


def calculate_v1(s):
    """ This solution is stack-based. The stack is used to hold temporary results for partial expressions with lower
         precedence, which are + and -. This helps delay calculations until an operator with a higher
         precedence is met.

        We know that there could be 4 types of operations: addition (+), subtraction (-), multiplication (*) and
        division (/). Without parenthesis, we know that multiplication (*) and division (/) operations would always
        have higher precedence over addition (+) and subtraction (-) based on operator precedence rules:

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

        Using this intuition, let's look at the algorithm to implement the problem.
        Scan the input string s from left to right and evaluate the expressions based on the following rules:

            - If the current character is a digit 0-9 (operand), add it to the number 'cur_operand'.

            - Otherwise, the current character must be an operation (+,-,*, /). Evaluate the expression based on the
               type of LAST operator:

                1) Addition (+) or Subtraction (-): we must evaluate the expression later based on the next operator.
                    So, we must store 'cur_operand' to be used later. Push 'cur_operand' to the stack.
                    The last pushed number in the stack would be popped out first for evaluation. In addition, when we
                    pop from the stack and evaluate this expression in the future, we need a way to determine if the
                    LAST operator was Addition (+) or Subtraction (-). To simplify the evaluation, we can push
                    -cur_operand to the stack if the last operation was subtraction (-) and assume that the operation
                    for all the values in the stack is addition (+). This works because (a - num) is equivalent to
                    (a + (-num)).

                2) Multiplication (*) or Division (/): pop the top values from the stack and evaluate the current
                    expression. Push the evaluated value back to the stack.

        Once the string is scanned, pop from the stack and add to the result.

        Every time an operation sign is met, 'last_operator' variable tells us the type of the PREVIOUS operator the
        last integer we read is part of: 11 - 2 * 5: say we read 11 and then encounter '-', we look at 'last_operator'
        which is '+' by default, so we know that 11 is part of an addition operation (0 + 11). Then we read 2 and meet
        '*', we look at 'last_operator' which was assigned to '-', so we know that 2 is part of a subtraction operation
        (11 - 2).

        For example, let's look at '22 - 31 * 52 + 22'.
        First, 'cur_operand' variable is used to accumulate the integer value of operands. Here, the first value of
        'cur_operand' will hold 22.
        When '-' is encountered, we look at the last operator which is '+' by default. Since '+' is an equal precedence
        operator, push num (22) and let it wait, and change last operator to '-'.
        Again, 'cur_operand' holds the value of next operand 31, and '*' is encountered. Last operator is '-', so push
        -num (-31) to the stack and change last operator to *.
        Now cur_operand=52 is processed and '+' is encountered. Since last operator is '*' which has higher precedence
        than '+', push the result of cur_operand=52 multiplied by the last element in the stack=-31 (after popping it),
        and change last operator to '+'.
        Now last operand is read i.e. cur_operand=22, and we are at the end of the string, and since last operator was
         '+' then push cur_operand=22.
        Finally, the stack content is just 22, the multiplication of -31 by 52, and 22. The result is the sum of the
        stack.

    Time complexity: O(N), where N is the length of s
    Space complexity: O(N)
    """
    n = len(s)
    stack = []
    cur_operand , last_operator = 0, '+'
    for i, c in enumerate(s):
        if c.isdigit():
            cur_operand = cur_operand * 10 + int(c)
        if c in '+-*/' or i == n - 1:
            if last_operator == '+':
                # We have a new operation sign in hand and the accumulated integer 'cur_operand' is part of a PREVIOUS
                # addition operation
                stack.append(cur_operand)
            elif last_operator == '-':
                stack.append(-cur_operand)
            elif last_operator == '*':
                # We have a new operation sign in hand and the accumulated integer 'cur_operand' is part of a PREVIOUS
                # multiplication operation.
                # Multiply 'cur_operand' with the previously accumulated integer that's been waiting in the stack since
                # multiplication is a higher precedence operation
                stack.append(stack.pop() * cur_operand)
            else:
                # We have a new operation sign in hand and the accumulated integer 'cur_operand' is part of a PREVIOUS
                # division operation.
                # Perform the division of the previously accumulated integer that's been waiting in the stack by the
                # accumulated integer 'cur_operand' since division is a higher precedence operation.
                stack.append(int(float(stack.pop()) / cur_operand))
            cur_operand = 0
            last_operator = c
    return sum(stack)


# Check out:
# https://leetcode.com/problems/basic-calculator-ii/discuss/63088/Explanation-for-Java-O(n)-time-and-O(1)-space-solution
def calculate_v2(s):
    """ In the previous implementation, we used a stack to track the values of the evaluated expressions. In the end,
         we popped all the values from the stack and added to the result.

         Instead, we could add the values to the result beforehand and keep track of the last calculated number, thus
         eliminating the need for the stack.

        To replace the stack, we use a variable 'prev_exp_eval' to track the value of the last evaluated expression.

            - If the last operator is addition (+) or subtraction (-), add the 'prev_exp_eval' to the result instead of
               pushing it to the stack. 'prev_exp_eval' would then be updated to 'cur_num' for the next iteration.

            - If the last operator is multiplication (*) or division (/), we must evaluate the expression
               (prev_exp_eval * cur_operand) and update 'prev_exp_eval' with the result of the expression. This would be
               added to the result after the entire string is scanned.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(s)
    cur_operand = prev_exp_eval = 0
    last_operator = '+'
    res = 0
    for i, c in enumerate(s):
        if c.isdigit():
            cur_operand = cur_operand * 10 + int(c)
        if c in '+-/*' or i == n - 1:
            if last_operator == '+':
                res += prev_exp_eval
                prev_exp_eval = cur_operand
            elif last_operator == '-':
                res += prev_exp_eval
                prev_exp_eval = -cur_operand
            elif last_operator == '*':
                prev_exp_eval *= cur_operand
            else:
                prev_exp_eval = int(float(prev_exp_eval) / cur_operand)
            last_operator = c
            cur_operand = 0
    return res + prev_exp_eval


class Test(unittest.TestCase):
    data = [('3+2*2', 7), (' 3+5 / 2 ', 5)]

    def test_calculate(self):
        for test_string, result in self.data:
            self.assertEqual(result, calculate_v1(test_string))
            self.assertEqual(result, calculate_v2(test_string))


if __name__ == '__main__':
    unittest.main()

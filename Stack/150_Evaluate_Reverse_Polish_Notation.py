""" Evaluate the value of an arithmetic expression in Reverse Polish Notation.
Valid operators are +, -, *, /. Each operand may be an integer or another expression. """

import unittest2 as unittest


def eval_rpn(tokens):
    """ We'll start with looking at what it means for integer division to truncate towards zero. When dividing
         2 positive numbers, we always truncate down to the nearest integer. The non-integer values are
         in parentheses afterwards for reference:
         6 / 2 = 3 (3.0)
         11 / 5 = 2 (2.2)
         9 / 5 = 1 (1.8)

         Most programming languages do integer division by default (as opposed to float division, where decimal places
         are kept), and this is how they handle positive integers. Both of the following definitions could be (and are)
         used to describe the truncation.

            1- The result is truncated to a less than or equal number. i.e. 1 is less than 1.8.
            2- The truncation is towards zero, i.e. 1 is closer to zero than 1.8 is.

         For negative numbers, however, it is impossible to satisfy both of these, so one or the other has to be picked.
         For example, consider the following:
         -9 / 5 = ? (-1.8)
         If we wanted the truncated result to be smaller, we'd have to go to -2, as -2 < -1.
         If we wanted the truncated result to be nearer to zero, we'd have to go to -1 as -1 is nearer to zero than -2
         is.

         Some programming languages go with the first definition, and others go with the second. For this problem, we
         are expected to go with the second definition, regardless of what the chosen programming language uses.

         Python, for example, goes with the first definition. This means that we need to find a way of doing the
         division. Luckily, the int() function does truncate towards zero, and therefore we can use int(a / b) trick.

         The rule most programming languages use is to do division and multiplication first, in order from left to
         right, and then addition and subtraction, in order from left to right. When we want to do the operations in a
         different order, we use parenthesis (brackets) around the parts to do first. The parts in parentheses are
         always done before the parts outside.

         Just like Infix Notation, or in fact any other notation, Reverse Polish Notation has rules for how to evaluate
         it:
                    While there are operators remaining in the list, find the left-most operator. Apply it to the 2
                    numbers immediately before it, and replace all 3 tokens (the operator and 2 numbers) with
                    the result.

        As long as the input was valid, this rule will always work and leave a single number that should be returned.
        The leftmost operator that hasn't yet been removed will always have 2 numbers immediately before it.

        The two key steps of the above algorithm are:

            1- Visit each operator, in linear order. Finding these can be done with linear search of the original list.
            2- Get the 2 most recently seen numbers that haven't yet been replaced. These could be tracked using a
                 stack.

        Remember that for division and subtraction, the order of the numbers matters. i.e. 7 - 5 ≠ 5 - 7. On the stack,
        we have the second on the top. So we need to reverse them before applying the operator.

    Time complexity: O(N), we do a linear search to put all numbers on the stack, and process all operators. Processing
    an operator requires removing 2 numbers off the stack and replacing them with a single number, which is an O(1)
    operation.
    Space complexity: O(N)
    """
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: int(x / y)
    }
    stack = []
    for token in tokens:
        if token not in operations:
            stack.append(int(token))
        else:
            a, b = stack.pop(), stack.pop()
            operation = operations[token]
            stack.append(operation(b, a))
    return stack.pop()


class Test(unittest.TestCase):
    data = [(['2', '1', '+', '3', '*'], 9),
            (['4', '13', '5', '/', '+'], 6),
            (['10', '6', '9', '3', '+', '-11', '*', '/', '*', '17', '+', '5', '+'], 22)]

    def test_eval_rpn(self):
        for test_tokens, result in self.data:
            self.assertEqual(result, eval_rpn(test_tokens))


if __name__ == '__main__':
    unittest.main()


""" Evaluate the value of an arithmetic expression in Reverse Polish Notation.
Valid operators are +, -, *, /. Each operand may be an integer or another expression. """

import unittest2 as unittest


def eval_rpn(tokens):
    """ Pretty straightforward stack solution.
        When we see a digit, we push it to the stack.
        When we see an operator, we perform 2 pops, apply the operation between the 2 values (first popped item goes on
        left of the sign, 2nd popped item goes on the right of the sign), and then push the result back onto the stack
        so we can work with it as we continue.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    operators = {'+': lambda x, y: x + y, '-': lambda x, y: x - y,
                 '*': lambda x, y: x * y, '/': lambda x, y: int(x / y)}
    stack = []
    for token in tokens:
        if token not in operators:
            stack.append(int(token))
        else:
            a, b = stack.pop(), stack.pop()
            stack.append(operators[token](b, a))
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


""" Evaluate the value of an arithmetic expression in Reverse Polish Notation.
Valid operators are +, -, *, /. Each operand may be an integer or another expression. """

import unittest2 as unittest


def eval_rpn(tokens):
    """ Pretty straightforward stack solution.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    stack = []
    for token in tokens:
        if token not in '+-*/':
            stack.append(int(token))
        else:
            op1, op2 = stack.pop(), stack.pop()
            stack.append(op1 + op2 if token == '+'
                         else op2 - op1 if token == '-'
                         else op1 * op2 if token == '*'
                         else int(float(op2) / op1))
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


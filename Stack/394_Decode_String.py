""" Given an encoded string, return its decoded string.
The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly
k times. Note that k is guaranteed to be a positive integer. """

import unittest2 as unittest


def decode_string(s):
    """ The solution is a simple stack based one which evaluates the innermost brackets first.
        Concatenate digits and alphabets. When '[' appears, push the current alphas and digits into the stack, and
        start a new concatenation for alphas and digits. When a ']' appears, pop the stack and extend the popped
        alphas n times to the current alphas.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    current_string, num = '', 0
    stack = []
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c.isalpha():
            current_string += c
        elif c == '[':
            stack.append(current_string)
            stack.append(num)
            current_string, num = '', 0
        elif c == ']':
            repeat = stack.pop()
            substr = stack.pop()
            current_string = substr + repeat * current_string
    return current_string


class Test(unittest.TestCase):
    data = [('3[a]2[bc]', 'aaabcbc'), ('3[a2[c]]', 'accaccacc'), ('2[abc]3[cd]ef', 'abcabccdcdcdef')]

    def test_decode_string(self):
        for test_string, result in self.data:
            self.assertEqual(result, decode_string(test_string))


if __name__ == '__main__':
    unittest.main()
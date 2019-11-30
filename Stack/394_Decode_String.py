""" Given an encoded string, return its decoded string.
The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly
k times. Note that k is guaranteed to be a positive integer. """

import unittest2 as unittest


def decode_string(s):
    """ The solution is a simple stack based one which evaluates the innermost brackets first. We iterate over the 
        string and push everything to a stack until we find a right bracket. We use that and pop from the stack to 
        evaluate the innermost expression in the string. For example, if we have 2[a3[b]], our stack would be 
        [2, '[', 'a', 3, '[', 'b'] when it reaches the first right bracket. We attempt to evaluate everything in the 
        innermost bracket by popping from the stack to form the entire string we need to multiply, and find the number 
        we need to multiply by. After this, the stack will look like: [2, '[', 'a', 'bbb' ]. The innermost expression 
        of 3, '[', 'b' was turned into 'bbb' and put back into the stack. At the next right bracket, we will similarly 
        evaluate the innermost bracket , so that the stack turns into ['abbbabbb']. If there are multiple sets of 
        enclosed brackets in the expression, our stack will end up with multiple strings in the end. Simply join them 
        for the result.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    stack, num, res = [], 0, ''
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c.isalpha():
            stack.append(c)
        elif c == '[':
            stack.append(num)
            stack.append(c)
            num = 0
        elif c == ']':
            cur_str = ''
            while stack and stack[-1] != '[':
                cur_str = stack.pop() + cur_str
            stack.pop()
            repeat = stack.pop()
            stack.append(repeat * cur_str)
    return ''.join(stack)


class Test(unittest.TestCase):
    data = [('3[a]2[bc]', 'aaabcbc'), ('3[a2[c]]', 'accaccacc'), ('2[abc]3[cd]ef', 'abcabccdcdcdef')]

    def test_decode_string(self):
        for test_string, result in self.data:
            self.assertEqual(result, decode_string(test_string))


if __name__ == '__main__':
    unittest.main()
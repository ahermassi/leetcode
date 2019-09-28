""" Given two non-negative integers num1 and num2 represented as strings, return the product of num1 and num2,
also represented as a string. """

import unittest2 as unittest


def multiply_v1(num1, num2):
    """ Multiply each digit of num1 by num2. Sum the partial results. Exactly as humans do.
    Time complexity: O(N * M) where N is the length of num1 and M is the length of num2
    Space complexity: O(N + M)
    """
    res = []
    for c in num1[::-1]:
        s, carry, factor, acc = 0, 0, 1, 0
        for d in num2[::-1]:
            s = int(c) * int(d) + carry
            acc += (s % 10) * factor
            carry = s // 10
            factor *= 10
        if carry:
            acc += carry * factor
        res.append(acc)
    factor, ans = 1, 0
    for i in res:
        ans += i * factor
        factor *= 10
    return str(ans)


def multiply_v2(num1, num2):
    product = [0] * (len(num1) + len(num2))  # placeholder for multiplication n digits by m digits results in n+m digits
    position = len(product) - 1  # position within the placeholder

    for c in num1[::-1]:
        temp_pos = position
        for d in num2[::-1]:
            product[temp_pos] += int(c) * int(d)  # adding the results of single multiplication
            product[temp_pos - 1] += product[temp_pos] // 10  # bring out carry number to the left array
            product[temp_pos] %= 10  # remove the carry out from the current array
            temp_pos -= 1  # first shifting the multiplication to the end of the first integer
        position -= 1  # then once first integer is exhausted shifting the second integer and starting

    # once the second integer is exhausted we want to make sure we are not zero padding
    pointer = 0  # pointer moves through the digit array and locate where the zero padding finishes
    while pointer < len(product) - 1 and product[pointer] == 0:  # if we have zero before the numbers shift the
        # pointer to the right
        pointer += 1

    return ''.join(map(str, product[pointer:]))  # only report the digits to the right side of the pointer


class Test(unittest.TestCase):
    data = [('2', '3', '6'), ('123', '456', '56088')]

    def test_multiply(self):
        for test_num1, test_num2, result in self.data:
            self.assertEqual(result, multiply_v1(test_num1, test_num2))
            self.assertEqual(result, multiply_v2(test_num1, test_num2))


if __name__ == '__main__':
    unittest.main()

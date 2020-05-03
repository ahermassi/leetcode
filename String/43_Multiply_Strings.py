""" Given two non-negative integers num1 and num2 represented as strings, return the product of num1 and num2,
also represented as a string. """

import unittest2 as unittest


# Check out: https://leetcode.com/problems/multiply-strings/discuss/17605/Easiest-JAVA-Solution-with-Graph-Explanation

def multiply(num1, num2):
    """ Start from right to left, perform multiplication on every pair of digits, and add them together.
        We can immediately conclude that:
            num1[i] * num2[j] will be placed at indices [i + j, i + j + 1]
        Traverse from the end of the num1 and num2 strings, respectively, extract the characters at the
        corresponding positions, convert them into integers, and multiply them. Then determine the positions 'left' and
        'right' where the multiplied two digits are going to be placed. Since 'right' is lower than 'left', the
        resulting two-digit mul is first added to whatever is in the 'right' index, which may cause the number on the
        'right' to be greater than 9, so the number on the tens place is added to the high position 'left', leaving
        only the remainder at the 'right' position.
        Remember that leading zeros should be skipped. If skipping them leaves us with an empty list, then return '0'.
        Otherwise, return the result 'res'
    Time complexity: O(N * M) where N is the length of num1 and M is the length of num2
    Space complexity: O(N + M)
    """
    n, m = len(num1), len(num2)
    res = [0] * (n + m)  # placeholder for multiplication, n digits by m digits results in n+m digits
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            mul = (ord(num1[i]) - ord('0')) * (ord(num2[j]) - ord('0'))
            # 'left' and 'right' are where we're going to place the result of current multiplication in 'res' list.
            # We use the observation that 'left' and 'right' are always going to be equal to i+j and i+j+1, respectively
            left = i + j
            right = i + j + 1
            mul += res[right]  # There could be an integer at 'right' index from a previous calculation
            res[right] = mul % 10
            res[left] += mul // 10  # res[left] could be 9 and mul > 10, but it will be ultimately taken care of by
            # res[right] = mul % 10 in later traversal where left will become the right of following iteration
    i = 0
    while i < len(res) and res[i] == 0:  # Move through the 'res' array and locate where the zero padding ends
        i += 1
    return ''.join(map(str, res[i:])) if i < len(res) else '0'


class Test(unittest.TestCase):

    data = [('2', '3', '6'), ('123', '456', '56088')]

    def test_multiply(self):
        for test_num1, test_num2, result in self.data:
            self.assertEqual(result, multiply(test_num1, test_num2))


if __name__ == '__main__':
    unittest.main()

""" Given two non-negative integers num1 and num2 represented as strings, return the product of num1 and num2,
also represented as a string. """

import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=1vZswirL8Y8
# Check out: https://leetcode.com/problems/multiply-strings/discuss/17605/Easiest-JAVA-Solution-with-Graph-Explanation


def multiply_v1(num1, num2):
    """ We can try to break the problem down into manageable chunks, as is done in elementary mathematics. Thus, we will
         focus on one digit at a time.

         We take the ones place digit of the second number, then multiply it with all digits of the first number
         consequently going backward, and write the result. We need to remember about carry as well.
         Then we take the tens place digit of the second number and multiply it with all digits of the first number.
         Then we continue the same way with hundreds place digit, then with thousands place digit of the second number,
         and so on, until we have visited every digit in the second number.

         If we know the maximum size of the answer array ahead of time, we can add each multiplication result directly
         to the final answer.

         Try a few test cases, multiply two numbers, count how many digits are in the result, and compare that to the
         number of digits in each number. Notice that whenever two numbers with the number of digits N and M are
         multiplied, the result never exceeds (N+M) digits.

         So, an answer array of size N+M is guaranteed to be large enough to hold our final result. Let's create one and
         initialize all of its values as zero.

        Start from right to left, perform multiplication on every pair of digits, and add them together.
        We can immediately conclude that:

                num1[i] * num2[j] will be placed at indices [i + j, i + j + 1]

        Traverse from the end of the num1 and num2 strings, respectively, extract the characters at the
        corresponding positions, convert them into integers, and multiply them. Then determine the positions 'left' and
        'right' where the multiplied two digits are going to be placed.

        Since 'right' is lower than 'left', the resulting two-digit mul is first added to whatever is in the 'right'
        index, which may cause the number on the 'right' to be greater than 9, so the number on the tens place is added
        to the high position 'left', leaving only the remainder at the 'right' position.

        Remember that leading zeros should be skipped. If skipping them leaves us with an empty list, then return '0'.
        Otherwise, return the result 'res'.

    Time complexity: O(N * M), where N is the length of num1 and M is the length of num2
    Space complexity: O(N + M)
    """
    n, m = len(num1), len(num2)
    res = [0] * (n + m)  # placeholder for multiplication, n digits by m digits results in n+m digits
    for i in reversed(range(n)):
        a = (ord(num1[i]) - ord('0'))
        for j in reversed(range(m)):
            b = (ord(num2[j]) - ord('0'))
            mul = a * b
            # 'left' and 'right' are where we're going to place the result of current multiplication in the list.
            # We use the observation that 'left' and 'right' are always going to be equal to i+j and i+j+1, respectively
            left, right = i + j, i + j + 1
            mul += res[right]  # There could be an integer at 'right' index from a previous calculation
            res[right] = mul % 10
            res[left] += mul // 10
            # res[left] could be 9 and mul > 10, but it will be ultimately taken care of by res[right] = mul % 10 in
            # later traversal where left will become the right of following iteration. Current 'left' will be 'right'
            # in next iteration, and the % operation will always get right result in 'right' position. Finally, the
            # overflow will end at head but will not overflow again.
            # Example: num1 = 99, num2 = 99
            # Before -> [0, 0, 0, 0]
            # After  -> [0, 0, 8, 1]
            # =================
            # Before -> [0, 0, 8, 1]
            # After  -> [0, 8, 9, 1]
            # =================
            # Before -> [0, 8, 9, 1]
            # After  -> [0, 17, 0, 1]
            # =================
            # Before -> [0, 17, 0, 1]
            # After  ->  [9, 8, 0, 1]
    i = 0
    while i < n + m and res[i] == 0:  # Move through the array and locate where the zero padding ends
        i += 1
    return ''.join(map(str, res[i:])) if i < n + m else '0'


def multiply_v2(num1, num2):
    """ If coming up with left and right insertion indices if not intuitive, we can use a write index that we keep
         shifting to the left once a digit multiplication is exhausted.
    Time complexity: O(N * M)
    Space complexity: O(N + M)
    """
    n, m = len(num1), len(num2)
    res = [0] * (n + m)
    write_index = n + m - 1
    for i in reversed(range(n)):
        a = (ord(num1[i]) - ord('0'))
        index = write_index
        for j in reversed(range(m)):
            b = (ord(num2[j]) - ord('0'))
            mul = a * b
            mul += res[index]
            res[index] = mul % 10
            res[index-1] += mul // 10
            index -= 1
        write_index -= 1
    i = 0
    while i < n + m and res[i] == 0:
        i += 1
    return ''.join(map(str, res[i:])) if i < n + m else '0'


def multiply_v3(num1, num2):
    """ Similar algorithm but with an extra loop.

         If we break the multiplication down into pieces, it will have the following steps:

            - Compute products from each pair of digits from num1 and num2
            - Carry each element over

        Example: num1 = "12", num2 = "19"

        First for loop:
        res = [0, 0, 0,18], after first iteration
        res = [0, 0, 9,18], after second iteration
        res = [0, 0,11,18], after third iteration
        res = [0, 1,11,18], after fourth iteration

        Second for loop:
        res = [0, 1, 11, 8], carry = 1, after first iteration
        res = [0, 1, 2, 8], carry = 1, after second iteration
        res = [0, 2, 2, 8], carry = 0, after third iteration

    Time complexity: O(N * M)
    Space complexity: O(N + M)
    """
    n, m = len(num1), len(num2)
    res = [0] * (n + m)
    for i in reversed(range(n)):
        a = (ord(num1[i]) - ord('0'))
        for j in reversed(range(m)):
            b = (ord(num2[j]) - ord('0'))
            mul = a * b
            res[i + j + 1] += mul
    carry = 0
    for i in reversed(range(len(res))):
        res[i] += carry
        carry = res[i] // 10
        res[i] %= 10
    i = 0
    while i < len(res) and res[i] == 0:
        i += 1
    return ''.join(map(str, res[i:])) if i < len(res) else '0'


class Test(unittest.TestCase):

    data = [('2', '3', '6'), ('123', '456', '56088')]

    def test_multiply(self):
        for test_num1, test_num2, result in self.data:
            self.assertEqual(result, multiply_v1(test_num1, test_num2))
            self.assertEqual(result, multiply_v2(test_num1, test_num2))
            self.assertEqual(result, multiply_v3(test_num1, test_num2))


if __name__ == '__main__':
    unittest.main()

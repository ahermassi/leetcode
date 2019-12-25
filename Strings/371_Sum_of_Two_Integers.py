""" Calculate the sum of two integers a and b, but you are not allowed to use the operator + and -. """

import unittest2 as unittest


def get_sum(a, b):
    """ The key insight is to realize that basic mathematical rules still work when using binary. So to solve these
        questions we should:
            1- Work out how the basic mathematical operation works step-by-step
            2- Replicate these operations using the basic bitwise operators
        In this case, we have addition. How does addition work normally (base 10/decimal)?
            1- If the two digits of the number add up to less than 10, we add that digit to our sum, with no carry
            2- If the two digits of the number add up to 10 or more, we add the least significant digit and carry the
               1 to the next position.
        '&' the AND operator:
            0101
            1101
            ----
            0101
        Notice how this ONLY happens at positions that will need a carry.
        '^' the XOR (exclusive or) operator:
            1010
            0110
            ----
            1100
        Notice something: this operator basically does addition (discarding carry)
        '<<' the left shift operator shifts all bits to the left in a binary representation:
            1010
            ----
            0100
        We need to be able to:
            1- Know what positions need a carry. The & operator can do this for us.
            2- Be able to add 'a' and 'b' after we know what positions yielded a carry. The '^' operator is perfect
               for this.
        Example:
            a = 1, b = 3
            a = (0001) base 2
            b = (0011) base 2
            What we do is have 'a' keep the running results of our additions, and we will have 'b' hold the carries
            that we will add against over...and over...and over...until there is nothing left to carry.

            1st iteration: a = (0001), b = (0011)
            '&' result [this is to see where we need to carry values over]
            0001
            0011
            ----
            0001 (this bit sequence represents positions that yield a carry)
            '^' result [this is to get the 'sum' between the 2 bit sequences. This is addition]
            0001
            0011
            ----
            0010
            << the carry [we do this since carries must be applied to 1 position to the left]
            0001
            ----
            0010    (in the next iteration, b will hold this, and it will be added against 'a' using '^', which
                     makes total sense. The carry we recorded before should be moved 1 left so it can simply be
                     added, then more carries will pop up, and so on until there are no carries left and we are
                     done with the addition.)

            2nd iteration: a = (0010), b = (0010)
            '&' result [this is to see where we need to carry values over]
            0010
            0010
            ----
            0010 (this bit sequence represents positions that yield a carry)
            '^' result [this is to get the 'sum' between the 2 bit sequences. This is addition]
            0010
            0010
            ----
            0000
            << the carry [we do this since carries must be applied to 1 position to the left]
            0010
            ----
            0100

            3rd iteration: a = (0000), b = (0100)
            '&' result [this is to see where we need to carry values over]
            0000
            0100
            ----
            0000 (This bit sequence represents positions that yield a carry: no more carry, so calculation stops at
                  next iteration)
            '^' result [this is to get the 'sum' between the 2 bit sequences. This is addition]
            0000
            0100
            ----
            0100
            << the carry [we do this since carries must be applied to 1 position to the left]
            0000
            ----
            0000

            4th iteration: a = (0100), b = (0000)
            b is null, so return the running sum a: a + b = 1 + 3 = 4 = 0100
    """
    while b:  # Keep adding until we have no carry left
        carry = a & b  # Take note of what positions will need a carry, we will left shift this below and make b hold
        # it. Remember: a carry is not applied where it is discovered. It is applied 1 position to the left of where
        # it was born
        a = a ^ b  # a's job is to keep the sum we are going to be working on, '^' does bit addition
        b = carry << 1  # b will house the carry from the operation, we left shift by 1 because in the next iteration
        # we will add against the carry
    return a


class Test(unittest.TestCase):
    data = [(1, 2, 3)]

    def test_get_sum(self):
        for test_a, test_b, result in self.data:
            self.assertEqual(result, get_sum(test_a, test_b))


if __name__ == '__main__':
    unittest.main()

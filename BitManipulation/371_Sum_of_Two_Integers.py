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

        Our first Instinct in problems like these should be that we're going to have to work with bits. Why?
        Because when we take the + sign, what other choice do we have? Plus, that's how computers do it!

        Our next thought should be to deeply understand how addition works. We can walk through an addition problem to
        see if we can understand something new—some pattern—and then see if we can replicate that with code. We'll work
        in base 10 so that it, easier to see.

        To add 759 + 674, we would usually add digit [0] from each number, carry the one, add digit [1] from each
        number, carry the one, and so on. We could take the same approach in binary: add each digit, and carry the one
        as necessary.

        Can we make this a little easier? Yes! Imagine we decided to split apart the "addition" and "carry" steps. That is, we do the following:

            - Add 759 + 674, but "forget" to carry. We then get 323.
            - Add 759 + 674 but only do the carrying, rather than the addition of each digit. We then get 1110.
            - Add the result of the first two operations (recursively, using the same process described in step 1
               and 2): 1110 + 323 = 1433.

        Now, how would we do this in binary?

            - If we add two binary numbers together, but forget to carry, the ith bit in the sum will be 0 only if a and b
               have the same ith bit (both 0 or both 1).This is essentially an XOR.
            - If we add two numbers together but only carry, we will have a 1 in the ith bit of the sum only if bits i-1
               of a and b are both 1s. This is an AND, shifted.
            - Now, iterate until there's nothing to carry.

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

        NOTE: This logic will cause a TLE in the case of negative numbers in Python. In Python, unlike other languages,
        the range of bits for representing a value is not 32, it's much larger than that. This is great when dealing
        with non-negative integers. However, this becomes a big issue when dealing with negative numbers. Why ?

        Let's have a look, say we are adding -2 and 3, which = 1.
        In Python this would be ( showing only 3 bits for clarity):

            1 1 0 +
            0 1 1

        Using binary addition we would get:

            0 0 1

        That seems fine but what happened to the extra carry bit ? ( 1 0 0 0 ). If we were doing this by hand we would
        simply ignore it, but Python does not, instead it continues 'adding' that bit and continuing the sum.

        1 1 1 1 1 1 0 +
        0 0 0 0 0 1 1
        0 0 0 1 0 0 0 + ( carry bit )

        So this actually continues on forever. For this reason, the mask is used to handle the negative case. if there
        is no mask then this will be an infinite loop, why? If b is negative then MSB of 'b' is 1 and the loop
        condition "while b & mask:" without mask will cause an infinite loop.

        The logic behind a mask is really simple. we should know that x & 1 = x, so using that simple principle, if we
        create a series of 4 1's and & them to any larger size series, we will get just that part of the series we want,
         so:

            1 1 1 1 1 0 0 1
            0 0 0 0 1 1 1 1 &
            0 0 0 0 1 0 0 1 (Important to note that using a mask removes the two's compliment)

        For this question, we just need to create a 32-bit mask of 1's , the quickest way is to use the hexadecimal
        0xffffffff.

        Note that in the while loop condition, if b = 0 that means the carry bit 'finished', but when there is a
        negative number (like -1), the carry bit will continue until it exceeds the 32-bit mask (to end the while loop).
    """
    mask = 0xffffffff
    while b & mask:  # Keep adding until we have no carry left
        carry = a & b  # Take note of what positions will need a carry, we will left shift this below and make b hold
        # it. Remember: a carry is not applied where it is discovered. It is applied 1 position to the left of where
        # it was born
        a = a ^ b  # a's job is to keep the sum we are going to be working on, '^' does bit addition
        b = carry << 1  # b will house the carry from the operation, we left shift by 1 because in the next iteration
        # we will add against the carry
    return a & mask if b > 0 else a


class Test(unittest.TestCase):
    data = [(1, 2, 3)]

    def test_get_sum(self):
        for test_a, test_b, result in self.data:
            self.assertEqual(result, get_sum(test_a, test_b))


if __name__ == '__main__':
    unittest.main()

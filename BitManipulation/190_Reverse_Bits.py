""" Reverse bits of a given 32 bits unsigned integer. """


def reverse_bits(n):
    """ Similar to 7- Reverse Integer, but instead of using modulo and division by 10, we use bit manipulation.

         One of the most intuitive solutions is to reverse the bits one by one.

         To retrieve the right-most bit in an integer n, we could apply the bit AND operation (i.e. n & 1). In order to
         combine the results of reversed bits, we could use the bit OR operation.

         Shift 1 bit to left == multiply by 2
         Shift 1 bit to right == divide by 2
         Bit & 1 determines if a bit is 0 or 1. Similarly, x & 1 gets the value of the least significant bit of x.

         The key idea is that for a bit that is situated at the index i, after being reversed, its position should be
         31-i (note: the index starts from zero).

            - We iterate through the bit string of the input integer, from right to left (i.e. n = n >> 1). To retrieve
               the right-most bit, we apply the bit AND operation (n & 1).
            - For each bit, we reverse it to the correct position, then we accumulate this reversed bit to the final
               result.

        Let's work on an example. Say, n = 19, which is 00000000000000000000000000010011 in binary, so in the
        output we should get 11001000000000000000000000000000 in binary, which is 3355443200.

        We initialize 'answer' to 0, so in binary it's 32 zeroes. We loop over 32 times, since every integer
        is going to have 32 possible 0/1's.

        1st line in the loop: n & 1, we check if last bit of n is set, is it 1 or 0; answer << 1 shifts all bits that we
        already have in our answer to the left, so after this shifting the bit on the right is 0; by using | we set
        the last bit in the answer to the value that we got in n & 1.

        2nd line in the loop: we shift bits of our initial number n to the right, since we've already checked the least
        significant bit of n, so we just move on to the next bit.

        So, in our example, we're going to work on only the first 5 right bits, since other bits are 0.

        answer = 0, in binary: 00000000000000000000000000000000
        answer << 1 = 00000000000000000000000000000000, n & 1 = 00000000000000000000000000000001,
        after | operation, answer = 00000000000000000000000000000001

        answer = 1, in binary: 00000000000000000000000000000001
        answer << 1 = 00000000000000000000000000000010, n & 1 = 00000000000000000000000000000001
        after | operation, answer = 00000000000000000000000000000011

        answer = 3, in binary: 00000000000000000000000000000011
        answer << 1 = 00000000000000000000000000000110, n & 1 = 00000000000000000000000000000000
        after | operation, answer = 00000000000000000000000000000110

        answer = 6, in binary: 00000000000000000000000000000110
        answer << 1 = 00000000000000000000000000001100, n & 1 = 00000000000000000000000000000000
        after | operation, answer = 00000000000000000000000000001100

        answer = 12, in binary: 00000000000000000000000000001100
        answer << 1 = 00000000000000000000000000011000, n & 1 = 00000000000000000000000000000001
        after | operation, answer = 00000000000000000000000000011001

        And after that, we'll just shift 00000000000000000000000000011001 all the way to the left, which results in
        11001000000000000000000000000000

        We are asked to reverse bits in our number. What is the most logical way to do it? Create number 'answer',
        process the original number bit by bit starting with the Least Significant Bit, and add this bit to the end of
        'answer' number, and that is all!

            - answer = (answer << 1) | (n & 1) adds last bit of n to 'answer'
            - n = n >> 1 removes last bit from n

    Time complexity: O(1)
    Space complexity: O(1)
    """
    reversed = 0
    for _ in range(32):
        reversed = (reversed << 1) | (n & 1)
        n = n >> 1
    return reversed

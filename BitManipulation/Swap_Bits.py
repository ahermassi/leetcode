""" Implement code that takes as input a 64-bit integer and swaps the bits at indices i and j. """


def swap_bits(x, i, j):
    """ We first test if the bits to be swapped differ. If they do not, the swap does not change the integer. If the
        bits are different, swapping them is the same as flipping their individual values.
    Time complexity: O(1)
    """
    if (x >> i & 1) != (x >> j & 1):  # Extract the ith and jth bits and see if they differ
        bit_mask = 1 << i | 1 << j  # We will swap them by flipping their values. Select the bits to flip with bit_mask.
        # This bit mask is a binary value with ith and jth bits set to 1 and the rest set to 0: 00001(ith)0001(jth)000
        x ^= bit_mask  # Since 1^1 = 0 and 0^1 = 1, we can perform the flip XOR.
    return x
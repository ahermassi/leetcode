""" Given a positive integer n, find the smallest integer which has exactly the same digits existing in the integer n
and is greater in value than n. If no such positive integer exists, return -1.

Note that the returned integer should fit in 32-bit integer, if there is a valid answer but it does not fit in 32-bit
integer, return -1. """


def next_greater_element(n):
    """ Refer to 31- Next Permutation.
        Why do we have to walk from right to left? Because we want the least significant digit that is greater than the
        current number.
        Why do we have to find digits[j] and swap? We're trying to find a digit which is only 1 distance greater than
        digits[i-1] so that this can become the new number and is 1 greater than the new dip.
        Why do we have to reverse the suffix? We're trying to make the new number as small as possible. Because we know
        that the sequence is increasing from right to left, we can reverse it to be an increasing sequence from left to
        right.
    Time complexity: O(N), where N is the number of digits in the given number
    Space complexity: O(N)
    """
    digits = list(str(n))
    i = j = len(digits) - 1
    while i > 0 and digits[i - 1] >= digits[i]:  # Looking for the longest decreasing (from left) suffix
        i -= 1
    if i == 0:  # If the entire sequence is decreasing, then the current permutation is the last in order. Return -1.
        return -1
    k = i - 1  # This is the index just before the starting index of the longest decreasing suffix
    while digits[j] <= digits[k]:  # Looking for the smallest element greater than the value at k. We want to increase
        # the permutation by as little as possible
        j -= 1
    digits[j], digits[k] = digits[k], digits[j]
    l, r = k + 1, len(digits) - 1
    while l < r:   # Reverse the suffix
        digits[l], digits[r] = digits[r], digits[l]
        l += 1
        r -= 1
    res = int(''.join(digits))
    return res if res <= 2 ** 31 - 1 else -1

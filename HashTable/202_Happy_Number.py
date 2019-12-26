""" Write an algorithm to determine if a number is "happy".
A happy number is a number defined by the following process: Starting with any positive integer, replace the number by
the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay), or it
loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers.
"""

import unittest2 as unittest


def is_happy_v1(n):
    """ There are 2 parts to the algorithm we'll need to design and code.
            1- Given a number n, what is its next number?
            2- Follow a chain of numbers and detect if we've entered a cycle.
        Part 1 can be done using the division and modulus operators to repeatedly take digits off the number until none
        remains, and then squaring each removed digit and adding them together.
        Part 2 can be done using a hash set. Each time we generate the next number in the chain, we check if it's
        already in our hash set. If it is not in the hash set, we should add it. If it is in the hash set, that means
        we're in a cycle and so should return false.
    Time complexity: we are processing each digit in the number, and the number of digits in a number is given by logn.
    Space complexity: O(logn) ?
    """

    def sum_digits(n):
        total_sum = 0
        while n:
            digit = n % 10
            n = n // 10
            total_sum += digit ** 2
        return total_sum

    seen = {n}
    while n != 1:
        n = sum_digits(n)
        if n in seen:
            return False
        seen.add(n)
    return True


class Test(unittest.TestCase):

    def test_is_happy(self):
        self.assertTrue(is_happy_v1(19))


if __name__ == '__main__':
    unittest.main()
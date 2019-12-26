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

    def digit_square_sum(n):
        total_sum = 0
        while n:
            digit = n % 10
            n = n // 10
            total_sum += digit ** 2
        return total_sum

    seen = {n}
    while n != 1:
        n = digit_square_sum(n)
        if n in seen:
            return False
        seen.add(n)
    return True


def is_happy_v2(n):
    """ The chain we get by repeatedly calling digit_square_sum(n) is an implicit linked list. Implicit means we don't
        have actual nodes and pointers, but the data does still form a linked list structure. The starting number is
        the head node of the list, and all the other numbers in the chain are nodes. The next pointer is obtained with
        our digit_square_sum(n) function.
        We can therefore use Floyd's Cycle-Finding Algorithm here. This algorithm is based on 2 runners running around
        a circular race track, a fast runner and a slow runner. At each step of the algorithm, the slow runner goes
        forward by 1 number in the chain, and the fast runner goes forward by 2 numbers (nested calls to the
        digit_square_sum(n) function).
        If n is a happy number, i.e. there is no cycle, then the fast runner will eventually get to 1 before the slow
        runner.
        If n is not a happy number, then eventually the fast runner and the slow runner will be on the same number.
    Time complexity: O(logn), we're treating the length of the chain to the cycle as insignificant compared to the cost
    of calculating the next value for the first n
    Space complexity: O(1), we don't need a hash set to detect the cycle
    """

    def digit_square_sum(n):
        total_sum = 0
        while n:
            digit = n % 10
            n = n // 10
            total_sum += digit ** 2
        return total_sum

    slow, fast = n, digit_square_sum(n)
    while fast != 1:
        slow = digit_square_sum(slow)
        fast = digit_square_sum(digit_square_sum(fast))
        if slow == fast:
            return False
    return True


class Test(unittest.TestCase):

    def test_is_happy(self):
        self.assertTrue(is_happy_v1(19))
        self.assertTrue(is_happy_v2(19))


if __name__ == '__main__':
    unittest.main()
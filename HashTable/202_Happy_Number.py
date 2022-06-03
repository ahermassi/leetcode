""" Write an algorithm to determine if a number is "happy".
A happy number is a number defined by the following process: Starting with any positive integer, replace the number by
the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay), or it
loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers.
"""

import unittest2 as unittest


def is_happy_v1(n):
    """ There are 2 parts to the algorithm we'll need to design and code:

            1- Given a number n, what is its next number?
            2- Follow a chain of numbers and detect if we've entered a cycle.

        Part 1 can be done using the division and modulus operators to repeatedly take digits off the number until none
        remains, and then squaring each removed digit and adding them together.

        Part 2 can be done using a hash set. Each time we generate the next number in the chain, we check if it's
        already in our hash set. If it is not in the hash set, we should add it. If it is in the hash set, that means
        we're in a cycle and so should return false.

    Time complexity: O(log n), we are processing each digit in the number, and the number of digits in a number is given
    by log(n). Think about what would happen if we had a number with 1 million digits in it. The first step of the
    algorithm would process those million digits, and then the next value would be, at most (pretend all the digits
    are 9), be 81 * 1,000,000 = 81,000,000. In just one step, we've gone from a million digits, down to just 8.
    The largest possible 8-digit number we could get is 99,999,999, which then goes down to 81 * 8 = 648. And then from
    here, the cost will be the same as if we'd started with a 3-digit number. Starting with 2 million digits
    (a massively larger number than one with a 1 million digits) would only take roughly twice as long, as again, the
    dominant part is summing the squares of the 2 million digits, and the rest is tiny in comparison.
    What is the maximum number of loops?
    Imagine the input has x digits, so the first sum of squares is not bigger than 81x (with all digits equals 9).
    And we can prove that when x > 2, sum of squares of the input will be definitely smaller than input itself
    (compare a * a and a*10^x with a in one digit), which means the next sum of squares will be smaller than the first
    one, which means the maximum square sum is not bigger than 81x. So in the worst case, suppose x is bigger than 2,
    the maximum number of loops should be at most 81x times (from 1 to 81x, which is clearly not reachable).
    Space complexity: O(log n) ?
    """

    def digit_square_sum(n):
        total_sum = 0
        while n:
            digit = n % 10
            total_sum += digit ** 2
            n = n // 10
        return total_sum

    seen = set()
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
        a circular racing track, a fast runner (hare) and a slow runner (tortoise). At each step of the algorithm, the
        slow runner goes forward by 1 number in the chain, and the fast runner goes forward by 2 numbers
        (nested calls to the digit_square_sum(n) function).

        Regardless of where the tortoise and hare start in the cycle, they are guaranteed to eventually meet. This is
        because the hare moves one node closer to the tortoise (in their direction of movement) each step.

        If n is a happy number, i.e. there is no cycle, then the fast runner will eventually get to 1 before the slow
        runner.

        If n is not a happy number, then eventually the fast runner and the slow runner will meet at the same number.

    Time complexity: O(log n), we're treating the length of the chain to the cycle as insignificant compared to the cost
    of calculating the next value for the first n
    Space complexity: O(1), we don't need a hash set to detect the cycle
    """

    def digit_square_sum(n):
        total_sum = 0
        while n:
            digit = n % 10
            total_sum += digit ** 2
            n = n // 10
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
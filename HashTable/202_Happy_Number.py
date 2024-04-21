""" Write an algorithm to determine if a number is "happy".
A happy number is a number defined by the following process: Starting with any positive integer, replace the number by
the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay), or it
loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers.
"""

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=ljz85bxOYJ0
def is_happy_v1(n):
    """ After working through some examples, we'd expect continually following links to end in one of three ways:

            - Eventually get to 1
            - Eventually get stuck in a cycle
            - Keep going higher and higher, up towards infinity

        That 3rd option sounds really annoying to detect and handle. How would we even know that it is going to
        continue going up, rather than eventually going back down, possibly to 1? Luckily, it turns out we don't need
        to worry about it. Think carefully what is the largest next number we could get for each number of digits.

        Digits	 Largest	               Next
            1	        9	                        81
            2	        99	                    162
            3	        999	                    243
            4	        9999	                324
            13	    9999999999999	1053

        For a number with 3 digits, it's impossible for it to ever go beyond 243. This means it will have to either get
        stuck in a cycle below 243 or go down to 1. Numbers with 4 or more digits will always lose a digit at each step
        until they are down to 3 digits. So we know that at worst, the algorithm might cycle around all the numbers
        below 243 and then go back to one it's already been to (a cycle) or go to 1. But it won't go on indefinitely,
        allowing us to rule out the 3rd option.

        There are 2 parts to the algorithm we'll need to design and code:

            1- Given a number n, what is its next number?
            2- Follow a chain of numbers and detect if we've entered a cycle.

        Part 1 can be done using the division and modulus operators to repeatedly take digits off the number until none
        remains, and then squaring each removed digit and adding them together.

        Part 2 can be done using a hash set. Each time we generate the next number in the chain, we check if it's
        already in the hash set. If it is not in the hash set, we should add it. If it is in the hash set, that means
        we're in a cycle and so should return false.

    Time complexity: O(log n), we are processing each digit in the number, and the number of digits in a number is given
    by log(n). Think about what would happen if we had a number with 1 million digits in it. The first step of the
    algorithm would process those million digits, and then the next value would be, at most (pretend all the digits
    are 9), 81 * 1,000,000 = 81,000,000. In just one step, we've gone from a million digits, down to just 8.
    The largest possible 8-digit number we could get is 99,999,999, which then goes down to 81 * 8 = 648. And then from
    there, the cost will be the same as if we'd started with a 3-digit number. Starting with 2 million digits
    (a massively larger number than one with a 1 million digits) would only take roughly twice as long, as again, the
    dominant part is summing the squares of the 2 million digits, and the rest is tiny in comparison.
    The time complexity analysis is broken down into two steps, based off of the insight that once a number reaches the
    <= 243 threshold it cannot get above it again: 1) the amount of time it takes a number to reach 243, and 2) once a
    number reaches the <= 243 threshold, the amount of time it takes to either find a cycle or get to 1.
    For 1) we argue that the time to reach 243 is O(log n) + O(log log n) + ..., but we disregard the terms after
    O(log n) because they are insignificant compared with O(log n). So the time complexity for 1) is O(log n).
    For 2) we argue that once a number reaches the <= 243 threshold, it will take, at absolute worst case, 243 more
    getNext() calls before we reach a cycle or get to 1. So each getNext call is O(log N) or O(d), where d is number of
    digits. So each getNext call here is O(3), or just 3, resulting in O(243 * 3) time complexity.
    Adding the two steps together we get O(log n) + O(243 * 3) ~= O(log n) is the time complexity.
    Space complexity: O(log n) ?
    """

    def digit_square_sum(n):
        total_sum = 0
        while n:
            digit = n % 10
            total_sum += digit * digit
            n = n // 10
        return total_sum

    square_sums = set()
    while n != 1:
        n = digit_square_sum(n)
        if n in square_sums:
            return False
        square_sums.add(n)
    return True


def is_happy_v2(n):
    """ The chain we get by repeatedly calling digit_square_sum(n) is an implicit linked list. Implicit means we don't
         have actual nodes and pointers, but the data does still form a linked list structure. The starting number is the
         head node of the list, and all the other numbers in the chain are nodes. The next pointer is obtained with the
         digit_square_sum(n) function.

         We can therefore use Floyd's Cycle-Finding Algorithm here. This algorithm is based on 2 pointers running around
         a circular racing track, a fast runner (hare) and a slow runner (tortoise). At each step of the algorithm, the
         slow runner moves forward by 1 number in the chain, and the fast runner moves forward by 2 numbers (nested
         calls to the digit_square_sum(n) function).

         Regardless of where the tortoise and hare start in the cycle, they are guaranteed to eventually meet. This is
         because the hare moves one node closer to the tortoise (in its direction of movement) each step.

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
            total_sum += digit * digit
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
""" Count the number of prime numbers less than a non-negative number, n. """

import unittest2 as unittest

# Good explanation: https://primes.utm.edu/glossary/page.php?sort=SieveOfEratosthenes


def count_primes(n):
    """ The solution is based on a technique called the Sieve of Eratosthenes.
            Make a list of all the integers less than n. Strike out the multiples of all primes less than or equal to
            the square root of n, then the numbers that are left are the primes.
        Create primes list for the integers up to n, initializing all indices to prime (1).
        Now set MULTIPLES of remaining prime numbers (marked 1) to not prime (0). Use upper limit of (n ** 0.5) + 1,
        because the smallest factor of a non-prime number will not be > sqrt(n).
        The terminating loop condition can be i < √n, as all non-primes ≥ √n must have already been marked off. When
        the loop terminates, all the numbers in the table that are non-marked are primes.
        Notes: To test whether a number is prime or not, we have to test whether it is divisible only up to the square
        root of that number.
        If a number n is not a prime, it can be factored into two factors a and b: n = a * b
        If both a and b were greater than the square root of n, then a * b would be greater than n, so at least one of
        those factors must be less than or equal to the square root of n. If we can't find any factors less than or
        equal to the square root of n, then n must be prime.
    Time complexity: O(n log n)
    Space complexity: O(n)
    """
    if n <= 2:  # We are interested in numbers LESS than the input number. Exit early if input LESS than 2 (2 is prime)
        return 0
    primes = [1] * n
    primes[0] = primes[1] = 0  # We know that 0 and 1 are not prime
    for i in range(2, int(n ** 0.5) + 1):
        if primes[i]:
            # Say i = 5, we mark off multiples of 5 starting at 5 × 5 = 25, because 5 × 2 = 10 was already marked
            # off by multiples of 2, similarly 5 × 3 = 15 was already marked off by multiples of 3. Therefore,
            # if the current number is p, we can always mark off multiples of p starting at p**2, then in increments of
            # p: p**2 + p, p**2 + 2p ...
            for j in range(i * i, n, i):
                primes[j] = 0
            # Same as:
            # primes[i * i: n: i] = [0] * len(primes[i * i: n: i])
    return sum(primes)


class Test(unittest.TestCase):

    def test_count_primes(self):
        self.assertEqual(4, count_primes(10))
        self.assertEqual(25, count_primes(100))


if __name__ == '__main__':
    unittest.main()
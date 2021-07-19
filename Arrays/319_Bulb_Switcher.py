""" There are n bulbs that are initially off. You first turn on all the bulbs, then you turn off every second bulb.

On the third round, you toggle every third bulb (turning on if it's off or turning off if it's on). For the ith round,
you toggle every i bulb. For the nth round, you only toggle the last bulb.

Return the number of bulbs that are on after n rounds. """

from math import sqrt


def bulbSwitch(n):
    """ Before we take a jump to the solution, let's first try to clear out what exactly the problem is about.
        As we know that there are n bulbs, let's name them as 1, 2, 3, 4, ..., n.
        We first turn on all the bulbs.
        Then, we turn off every second bulb (2, 4, 6, ...)
        On the third round, we toggle every third bulb (3, 6, 9, ...)
        For the ith round, we toggle every ith bulb (i, 2i, 3i, ...)
        For the nth round, we only toggle the last bulb (n)
        If n > 6, we can find that bulb 6 is toggled in rounds 2 and 3. Later, it will also be toggled in round 6, and
        round 6 will be the last round when bulb 6 is toggled. Here, 2,3 and 6 are all factors of 6 (except 1).
        We can come to the conclusion that the bulb i is toggled k times, where k is the number of i's factors
        (except 1).
        Now, the key problem here is to judge whether k is even or odd. Since all bulbs are ON at the beginning, we
        can get:

            Odd toggling operations will result in ON state
            Even toggling operations will result in OFF state

        Bulb i is switched in round d if and only if d divides i. So bulb i ends up ON if and only if it has an odd
        number of divisors.
        Divisors come in pairs, like i = 12 has divisors (1 , 12), (2 , 6), and (3 , 4). Except when i is a square,
        like 36 has divisors (1 , 36), (2 , 18), (3 , 12), (4 , 9), and double divisor 6.

            Bulb i ends up ON if and only if i is a square

        Because a perfect square number has an odd number of divisors, there is no round that can cancel out the toggle
        made by the "square-root" round. That's why all the perfect square numbers are in ON state.
        Now if we want to find how many bulbs are ON after n rounds, we need to find out how many perfect square
        numbers are NO MORE than n.
        The number of perfect square numbers less than or equal to n is the integer part of sqrt(n).
    Time complexity: O(1)
    Space complexity: O(1)
    """
    return int(sqrt(n))

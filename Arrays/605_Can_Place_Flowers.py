""" Suppose you have a long flowerbed in which some of the plots are planted and some are not. However,
flowers cannot be planted in adjacent plots - they would compete for water and both would die.
Given a flowerbed (represented as an array containing 0 and 1, where 0 means empty and 1 means not empty), and a
number n, return if n new flowers can be planted in it without violating the no-adjacent-flowers rule. """

import unittest2 as unittest


def can_place_flowers_v1(flowerbed, n):
    """ The idea is to find the maximum number of flowers that can be planted between each two consecutive 1s.
        We construct a list 'ones' that contains the indices of flowerbed that have value 1. After that, we examine
        each 2 consecutive indices in 'ones' list and do the math to calculate how many flowers can be planted between
        these 2 indices.
    """
    count, ones = 0, [i for i, num in enumerate(flowerbed) if num == 1]
    if not ones:
        return n <= (len(flowerbed) + 1) // 2
    for i in range(len(ones) - 1):
        prev_one, next_one = ones[i], ones[i + 1]
        count += (next_one - prev_one - 2) // 2
    first_one, last_one = ones[0], ones[-1]  # This is to account for cases where the first and/or last one is not
    # the first / last element in flowerbed
    a = first_one // 2
    b = (len(flowerbed) - last_one - 1) // 2
    count += a + b
    return count >= n


def can_place_flowers_v2(flowerbed, n):
    """ Iterate over the flowerbed and verify if slots of 3 consecutive zeros can be found. Update the array
    accordingly.
    Time complexity: O(N)
    Space complexity: O(N) for the new flowerbed array
    """
    flowerbed[:] = [0] + flowerbed + [0]  # Leading an trailing zeros are necessary for cases when flowerbed starts
    # and/or ends with 0
    count = 0
    for i in range(1, len(flowerbed) - 1):
        if flowerbed[i - 1] == flowerbed[i] == flowerbed[i + 1] == 0:
            flowerbed[i] = 1
            count += 1
    return count >= n


class Test(unittest.TestCase):
    data = [([1, 0, 0, 0, 1], 1, True), ([1, 0, 0, 0, 1], 2, False)]

    def test_can_place_flowers(self):
        for test_array, n, result in self.data:
            self.assertEqual(result, can_place_flowers_v1(test_array, n))
            self.assertEqual(result, can_place_flowers_v2(test_array, n))


if __name__ == '__main__':
    unittest.main()

""" Suppose you have a long flowerbed in which some of the plots are planted and some are not. However,
flowers cannot be planted in adjacent plots - they would compete for water and both would die.
Given a flowerbed (represented as an array containing 0 and 1, where 0 means empty and 1 means not empty), and a
number n, return if n new flowers can be planted in it without violating the no-adjacent-flowers rule. """

import unittest2 as unittest


def can_place_flowers_v1(flowerbed, n):
    """ Iterate over the flowerbed and verify if slots of 3 consecutive zeros can be found. Update the array
        accordingly. We can stop the process of checking the positions for planting the flowers as soon as 'count'
        becomes equal to n. If 'count' never becomes equal to n, n flowers can't be planted at the empty positions.
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
            if count == n:
                return True
    return False


def can_place_flowers_v2(flowerbed, n):
    """ This solution is more suitable when the input array is read-only.
        If there are 'count' zeroes in between two 1s, then how many 1s can we place in those zeroes without violating
        the given condition? Answer is (count-1)/2. The only cases this doesn't apply are when there are zeroes
        (1 or more):
            1- At the beginning of the array.
            2- At the end of the array.
        For these 2 cases, the number of 1s that we can place is count/2. But to generalize the algorithm and to
        simplify code inside loop, 'count' is initialized to 1 for the first time and result += (count-1)/2 effectively
        becomes result += count/2 for the case 1. For case 2, result is updated outside the loop, again by
        count/2 times.
        Finally, we check if the number of possible 1s that we can place is greater than or equal to n. If so, we
        return true else false.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not n:
        return True
    count, res = 1, 0
    for flower in flowerbed:
        if not flower:
            count += 1
        else:
            res += (count - 1) // 2
            count = 0
    if count:
        res += count // 2
    return res >= n


class Test(unittest.TestCase):
    data = [([1, 0, 0, 0, 1], 1, True), ([1, 0, 0, 0, 1], 2, False)]

    def test_can_place_flowers(self):
        for test_array, n, result in self.data:
            self.assertEqual(result, can_place_flowers_v1(test_array, n))
            self.assertEqual(result, can_place_flowers_v2(test_array, n))


if __name__ == '__main__':
    unittest.main()

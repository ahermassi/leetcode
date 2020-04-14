""" Suppose you have a long flowerbed in which some of the plots are planted and some are not. However,
flowers cannot be planted in adjacent plots - they would compete for water and both would die.
Given a flowerbed (represented as an array containing 0 and 1, where 0 means empty and 1 means not empty), and a
number n, return if n new flowers can be planted in it without violating the no-adjacent-flowers rule. """

import unittest2 as unittest


def can_place_flowers_v1(flowerbed, n):
    """ We can find out the extra maximum number of flowers, 'count', that can be planted for the given flowerbed
        arrangement. To do so, we can traverse over all the elements of the flowerbed and find out those elements which
        are 0 (implying an empty position). For every such element, we check if its both adjacent positions are also
        empty. If so, we can plant a flower at the current position without violating the no-adjacent-flowers-rule.
        For the first and last elements, we need not check the previous and the next adjacent positions, respectively.
        If the 'count' obtained is greater than or equal to n, the required number of flowers to be planted, we can
        plant n flowers in the empty spaces, otherwise not.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    m, count = len(flowerbed), 0
    for i in range(m):
        if flowerbed[i] == 0 and (i == 0 or flowerbed[i - 1] == 0) and (i == m - 1 or flowerbed[i + 1] == 0):
            flowerbed[i] = 1
            count += 1
    return count >= n


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

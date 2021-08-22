""" Koko loves to eat bananas. There are N piles of bananas, the i-th pile has piles[i] bananas.  The guards have gone
and will come back in H hours.
Koko can decide her bananas-per-hour eating speed of K.  Each hour, she chooses some pile of bananas, and eats K
bananas from that pile.  If the pile has less than K bananas, she eats all of them instead, and won't eat any more
bananas during this hour.
Koko likes to eat slowly, but still wants to finish eating all the bananas before the guards come back.
Return the minimum integer K such that she can eat all the bananas within H hours. """

import unittest2 as unittest


def min_eating_speed(piles, h):
    """ Koko needs at least len(piles) hours, as she cannot move onto a new pile even if she completes her current one
        within the hour. This is why we have h >= len(piles) in the description. If h = len(piles), we get only one
        hour to finish each pile. In this case, the rate will depend only on the size of the largest pile.
        For any list of pile sizes, eating at rate K = max(piles) will ensure that each pile takes only one hour, and
        the total time taken will be len(piles) which is <= h according to the description. This makes max(piles) a
        rate at which Koko is always able to finish.
        Any answer that we report should fall in the closed interval [1, max(piles)].
        The problem is basically asking us how much slower Koko can eat and still finish the piles within h hours.
        To get the optimal answer, we should probably try to use as many of the hours available as possible.
        Each hour, Koko chooses some pile of bananas and eats K bananas from that pile. There is a limited range of
        K's to enable her to eat all the bananas within h hours. We ought to reduce the searching space and to return
        the minimum valid K. Binary Search is born for that.
        There is a limited value range of K: [lo, hi]. There is a K' value such that K (for any K >= K') can enable
        Koko to eat all the bananas within h hours. We are asked to find K'.
    Time complexity: O(N logW), where N is the number of piles and W is the maximum size of a pile
    Space complexity: O(1)
    """
    left, right = 1, max(piles)
    while left < right:
        mid, hours_needed = (left + right) // 2, 0
        for bananas in piles:
            hours_needed += bananas // mid if bananas % mid == 0 else (bananas // mid) + 1
        if hours_needed <= h:
            right = mid
        else:
            left = mid + 1
    return left


class Test(unittest.TestCase):
    data = [([3, 6, 7, 11], 8, 4), ([30, 11, 23, 4, 20], 5, 30), ([30, 11, 23, 4, 20], 6, 23)]

    def test_min_eating_speed(self):
        for test_piles, test_h, result in self.data:
            self.assertEqual(result, min_eating_speed(test_piles, test_h))


if __name__ == '__main__':
    unittest.main()

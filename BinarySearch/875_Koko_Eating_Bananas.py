""" Koko loves to eat bananas. There are N piles of bananas, the i-th pile has piles[i] bananas.  The guards have gone
and will come back in H hours.
Koko can decide her bananas-per-hour eating speed of K.  Each hour, she chooses some pile of bananas, and eats K
bananas from that pile.  If the pile has less than K bananas, she eats all of them instead, and won't eat any more
bananas during this hour.
Koko likes to eat slowly, but still wants to finish eating all the bananas before the guards come back.
Return the minimum integer K such that she can eat all the bananas within H hours. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=U2SozAs9RzA
def min_eating_speed(piles, h):
    """ The first constraint of the problem is that Koko has to eat all the piles within h hours, where h is no less
         than the number of piles. We can imagine that with a fast speed, Koko spends 1 hour on each pile, and
         therefore can always finish all the piles within h hours. Let's call this kind of speed workable speed.

         Likewise, let any eating speed at which Koko can't eat all the piles be unworkable speed.

         However, we have another constraint that Koko would like to eat as slow as possible. Therefore, among all the
         workable eating speeds, we need to find out the minimum one.

         Does the order by which Koko eats affect the overall time?

         The answer is no. The order does not matter because Koko will stop eating for the rest of the hour, even if
         there are no more bananas left in the current pile. Therefore, the time she spends eating a particular pile is
         given as⌈number_of_bananas/speed⌉, regardless of the order of this pile in her eating plan ( ⌈x⌉ denotes
         ceil(x)). Thus, we can conclude that as long as the eating speed is the same, the order of the piles by which
         Koko eats does not affect the total hours, so we can keep the array as it is for convenience.

         The brute force approach is to try every possible eating speed to find the smallest workable speed. Starting
         from speed=1 and incrementing it by 1 each time, we will find a speed at which Koko can eat all piles within
         h hours, that is, the first minimum speed.

         We shall look for a more efficient way to locate the minimum workable eating speed.

         Koko needs at least len(piles) hours, as she cannot move to a new pile even if she completes the current one
         within the hour. This is why we have h >= len(piles) in the description. If h = len(piles), we get only one
         hour to finish each pile. In this case, the rate will depend only on the size of the largest pile.

         For any list of pile sizes, eating at rate K = max(piles) will ensure that each pile takes only one hour, and
         the total time taken will be len(piles) which is <= h according to the description. This makes max(piles) a
         rate at which Koko is always able to finish.

         Therefore, any answer that we report should fall in the closed interval [1, max(piles)].

         Each hour, Koko chooses some pile of bananas and eats K bananas from that pile. There is a limited range of
         K's to enable her to eat all the bananas within h hours. We ought to reduce the searching space and return the
         minimum valid K. Binary Search is born for that.

         We can observe that:

            - If Koko can eat all the piles with a speed of n, she can also finish the task with the speed of n+1.
               With a larger eating speed, Koko will spend less or equal time on every pile. Thus, the overall time is
               guaranteed to be less than or equal to that of the speed n.

            - If Koko can't finish with a speed of n, then she can't finish with the speed of n-1 either. With a smaller
               eating speed, Koko will spend more or equal time on every pile, thus the overall time will be greater
               than or equal to that of the speed n.

        Given the previous observations, we conclude that if the current speed is workable, then the minimum workable
        speed should be on its left inclusively. If the current speed is not workable, that is, too slow to finish the
        eating task, then the minimum workable speed should be on its right exclusively.

         Therefore, we can use binary search to locate the boundary that separates workable speeds and unworkable
         speeds to get the minimum workable speed.

        First, let's set a reasonable upper and lower bound for binary search to ensure that we do not miss any
        workable speed. Let the lower bound be 1, the minimum possible eating speed since there is no speed slower
        than 1. The upper bound will be the maximum eating speed, that is the maximum number of bananas in a pile.
        For instance, if the piles are [3,5,7,9], then 9 is the maximum number of bananas in a single pile, we can
        set the upper boundary as 9. Because Koko can eat every pile within 1 hour with a speed of 9, or any other
        faster speed, 9 is thus guaranteed to be a workable value.

        Once we set the boundaries, we can then apply the binary search to reduce the search space. In each iteration,
        we reduce the remaining search space by half until we have narrowed down the search space to just one element,
        which is the minimum workable eating speed.

         If we define w(x) = speed x is workable, then the distribution will look something like the following:
         [False, False, False,...,  False, True, True, True, ... True]
         Binary search is about finding the first/smallest x such that w(x) = True

    Time complexity: O(N logM), where N is the number of piles and M is the maximum size of a pile
    Space complexity: O(1)
    """

    def hours_needed_to_eat_at_speed(mid):
        hours_needed = 0
        for bananas in piles:
            hours_needed += bananas // mid
            if bananas % mid:
                hours_needed += 1
        return hours_needed

    left, right = 1, max(piles)
    while left < right:
        mid = (left + right) // 2
        if hours_needed_to_eat_at_speed(mid) <= h:
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

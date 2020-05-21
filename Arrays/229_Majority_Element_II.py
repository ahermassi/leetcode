""" Given an integer array of size n, find all elements that appear more than ⌊ n/3 ⌋ times.
Note: The algorithm should run in linear time and in O(1) space. """

import unittest2 as unittest


# Great visual explanation:
# https://leetcode.com/problems/majority-element-ii/discuss/543672/BoyerMoore-majority-vote-algorithm-EXPLAINED-(with-pictures)

def majority_element(nums):
    """ Boyer-Moore Majority Voting algorithm.
        The essential concepts is we keep a counter for the majority number X. If we find a number Y that is not X,
        the current counter should be decreased by 1. The reason is that if there is 5 X and 4 Y, there would be one
        (5-4) more X than Y. This could be explained as "4 X being paired out by 4 Y".
        Since the requirement is finding the majority for more than ceiling of [n/3], the answer would be less than or
        equal to two numbers. So we can modify the algorithm to maintain two counters for two majority CANDIDATES.
        They are not necessarily the 2 most frequent elements after the 1st round. Consider 3 cases:
            1- There are no elements that appears more than n/3 times, then whatever candidates the algorithm got from
               1st round would be rejected in the second round.
            2- There is only one element that appears more than n/3 times. After 1st round, the other candidate would
               be rejected in 2nd round.
            3- There are two elements appears more than n/3 times, so candidates would be equal to both of them.
        Given n numbers and k counters, only less than n/(k+1) pair-outs can happen.
            - Given n numbers and 1 counter (which is 169- Majority Element problem), at most (n/2) pair-outs can
              happen, which will lead to the survival of the only one element that appeared more than n/2 times.
            - Given n numbers and 2 counters (which is our case), at most n/3 pair-outs can happen, which will lead to
              the survival of (at most 2) elements that appeared more than n/3 times.
            - Given n numbers and k counters, at most (n/k+1) pair-outs can happen, which will lead to the survival of
              elements that appeared more than n/(k+1) times.
        Suppose nums = [1, 2, 3, 4, 5, 6], and we are finding two candidates and we have two counters.
        The procedure will be like this:

        candidate1 = 1, counter1 = 1
        candidate2 = 2, counter2 = 1

        current number = 3
        candidate1 = 1, counter1 = 0
        candidate2 = 2, counter2 = 0
        (One pair-out happens and both counters got decreased)

        current number = 4
        candidate1 = 4, counter = 1
        candidate2 = 2, counter2 = 0
        (Pair-out cannot happen and counter1 got increased)

        current number = 5
        candidate1 = 4, counter1 = 1
        candidate2 = 5, counter2 = 1
        (Pair-out can still not happen and counter2 got increased)

        current number = 6
        candidate1 = 4, counter1 = 0
        candidate2 = 5, counter2 = 0
        (Pair-out happens and both counters become 0)

        The main point of the algorithm is to form triples of different numbers like these (1,2,3), (1,3,4). The
        leftovers after this triple-forming procedure will be our majority candidates. These triples are produced when
        the two counters are decreased.
        Note that "-"'s occur simultaneously for the two counters but "+"'s occur to only one of them. Also every step
        leads to either "+" or "-". "+" means that we were unable to form a triple because we didn't have enough
        different elements at our disposal when the current element matched with one of the two types of stashed
        elements and we need to stash this element as well for the future.
        Why do we partition the elements into triples with different elements in each triple? It's because the
        leftovers after this procedure are the candidates for the majority elements. There will be elements of only two
        types in the leftovers (otherwise we could make a triple of them).
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    candidate1, candidate2 = None, None
    count1 = count2 = 0
    for num in nums:
        if num == candidate1:
            count1 += 1
        elif num == candidate2:
            count2 += 1
        elif count1 == 0:
            candidate1, count1 = num, 1
        elif count2 == 0:
            candidate2, count2 = num, 1
        else:
            count1 -= 1
            count2 -= 1
    return [candidate for candidate in (candidate1, candidate2) if nums.count(candidate) > n // 3]


class Test(unittest.TestCase):
    data = [([3, 2, 3], [3]), ([1, 1, 1, 3, 3, 2, 2, 2], [1, 2])]

    def test_majority_element(self):
        for test_array, result in self.data:
            self.assertEqual(result, majority_element(test_array))


if __name__ == '__main__':
    unittest.main()

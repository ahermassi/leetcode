""" You have d dice, and each die has f faces numbered 1, 2, ..., f.
Return the number of possible ways (out of fd total ways) modulo 10^9 + 7 to roll the dice so the sum of the face up
numbers equals target. """

import unittest2 as unittest


def num_rolls_to_target_v1(d, f, target):
    """ This problem is like coin change , with the difference that the total number of coins (dices) should be equal
        to d.
        Let dp(d, f, target) be the number of possible dice rolls of d dices with f faces to get a sum equal to target.
        As an initial example, suppose we have d= 5 dices with f = 6 faces each and we want to determine how many ways
        to make target = 18. In other words, what is dp(5, 6, 18) ?
        At first glance, this is seems difficult and overwhelming. But if we make one simple observation, we can reduce
        this big problem into several smaller sub-problems. We have 5 dices, but let's first just look at ONE of these
        dices (say the last one). This dice can take on f different values (1, ... , f), so we can consider what
        happens when we fix its value to any of these possibilities. In this case, f = 6.
        Case 1: The last dice roll is a 1. The remaining 4 dices must sum to 18-1=17. This can happen dp(4, 6, 17) ways.
        Case 2: The last dice roll is a 2. The remaining 4 dices must sum to 18-2=16. This can happen dp(4, 6, 16) ways.
        Case 3: The last dice roll is a 3. The remaining 4 dices must sum to 18-3=15. This can happen dp(4, 6, 15) ways.
        Case 4: The last dice roll is a 4. The remaining 4 dices must sum to 18-4=14. This can happen dp(4, 6, 14) ways.
        Case 5: The last dice roll is a 5. The remaining 4 dices must sum to 18-5=13. This can happen dp(4, 6, 13) ways.
        Case 6: The last dice roll is a 6. The remaining 4 dices must sum to 18-6=12. This can happen dp(4, 6, 12) ways.
            dp(5, 6, 18) = dp(4, 6, 17) + dp(4, 6, 16) + dp(4, 6, 15) + dp(4, 6, 14) + dp(4, 6, 13) + dp(4, 6, 12)
        We sum up the solutions for each of these 6 cases to arrive at our result. Of course, each of these cases
        branches off into 6 cases of its own.
        Therefore, the general relationship is:
            dp(d, f, target) = dp(d-1, f, target-1) + dp(d-1, f, target-2) + ... + dp(d-1, f, target-f)
        The first base case occurs when d = 0. We can make target = 0 with 0 dice, but nothing else.
        The second base case occurs when target > f * d. This means target is greater than the biggest sum that can be
        made with all the dices which happens to be f * d.
        The third base case occurs when d = 1. If we can roll only one dice, target should be <= f.
        We use memoization to avoid repeated calculations and don't consider negative or null targets.
    Time complexity: O(d * f * target)
    Space complexity: O(d * target)
    """

    def roll(d, remaining):
        if not d or remaining > f * d:
            return 0
        if d == 1:
            return int(remaining <= f)
        if (d, remaining) not in memo:
            res = 0
            for i in range(1, f + 1):
                if remaining - i > 0:  # Prune negative or null sums as the first is not feasible and the second is
                    # covered by the base case
                    res += roll(d - 1, remaining - i)
            memo[(d, remaining)] = res
        return memo[(d, remaining)]

    memo = {}
    return roll(d, target) % (10 ** 9 + 7)


class Test(unittest.TestCase):
    data = [(1, 6, 3, 1), (2, 6, 7, 6), (2, 5, 10, 1), (1, 2, 3, 0), (30, 30, 500, 222616187)]

    def test_num_rolls_to_target(self):
        for test_d, test_f, test_target, result in self.data:
            self.assertEqual(result, num_rolls_to_target_v1(test_d, test_f, test_target))


if __name__ == '__main__':
    unittest.main()

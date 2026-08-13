""" A conveyor belt has packages that must be shipped from one port to another within D days.
The i-th package on the conveyor belt has a weight of weights[i].  Each day, we load the ship with packages on the
conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship.
Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped
within D days. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=ER_oLmdc-nw
def ship_within_days(weights, days):
    """ The ship's capacity must be at least max(weights), because the heaviest package has to fit on the ship by
        itself. At the other extreme, a capacity of sum(weights) is always enough, because we could ship every package
        in a single day.

        So the answer must lie in: [max(weights), sum(weights)]

        Now define the predicate:

            can_ship(capacity) = days_needed_to_ship_with_capacity(capacity) <= days

        As capacity increases, shipping never becomes harder.
        For small capacities, we may need too many days: False False False False
        Eventually the capacity becomes large enough to meet the day limit: True True True ...

        So the answer space looks like: F F F F F T T T T
                                                  ^
                                                 first True

        We therefore use our canonical boundary binary search to find the smallest capacity for which can_ship(capacity)
        is True.

        For each candidate capacity `mid`, simulate loading the packages in order.
        if days_needed <= days: mid works, so it is in the True region. It could be the FIRST True, so keep it:
        right = mid
        Otherwise,mid does not work, so it is in the False region. Eliminate it: left = mid + 1

        When left == right, we have found the first True: the minimum ship capacity that can deliver all packages
        within `days`.

    Time complexity: O(N log(sum(weights) - max(weights)))
    Space complexity: O(1)
    """

    def days_needed_to_ship_with_capacity(capacity):
        days_needed, load = 0, 0
        # ---- Simulating loading the weight to ship one by one ---- #
        for weight in weights:
            load += weight
            if load > capacity:
                # Current ship meets its capacity
                days_needed += 1
                load = weight
        # After the loop, there is still the final partially/fully loaded day to count, hence + 1.
        # The important invariant is: every individual package must fit by itself. And because the binary search lower
        # bound is left = max(weights), that is guaranteed.
        return days_needed + 1

    left, right = max(weights), sum(weights)
    while left < right:
        mid = (left + right) // 2
        if days_needed_to_ship_with_capacity(mid) <= days:
            right = mid
        else:
            # We needed too many days, so we need to increase capacity to reduce number of days needed
            left = mid + 1
    return left


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 15), ([3, 2, 2, 4, 1, 4], 3, 6), ([1, 2, 3, 1, 1], 4, 3)]

    def test_ship_within_days(self):
        for test_weights, test_d, result in self.data:
            self.assertEqual(result, ship_within_days(test_weights, test_d))


if __name__ == '__main__':
    unittest.main()

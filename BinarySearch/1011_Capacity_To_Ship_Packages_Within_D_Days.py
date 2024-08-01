""" A conveyor belt has packages that must be shipped from one port to another within D days.
The i-th package on the conveyor belt has a weight of weights[i].  Each day, we load the ship with packages on the
conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship.
Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped
within D days. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=ER_oLmdc-nw
def ship_within_days(weights, days):
    """ An intuitive approach would be to start with checking ship capacity equal to the largest weight in weights,
         say w. The ship's capacity cannot be smaller than w, otherwise the conveyor belt couldn't ship the heaviest
         package.

         We check if it is possible to ship all the packages within the days' limit, using w as the capacity of the
         ship. If we are able to ship all the packages within the required days, we have w as the required answer.
         Otherwise, we increment the capacity and try with w+1. If we are able to ship the packages within the required
         days now, w+1 is the answer. Otherwise, we try with the ship's capacity as w+2, etc.

         How long can we go? In the worst case, we might need to choose the capacity of the ship equal to the sum of
         all the weights and send them all in one day.

         So, the range starts from the largest weight and goes until the sum of the weights in weights, i.e. the
         solution lies within a range.

         The intuitive, linear approach will provide the right answer to all the test cases but will indicate that the
         time limit has been exceeded. Let's think of a faster way by making some observations.

         If we cannot ship the packages in the required days with capacity A, we can never ship packages with a capacity
         less than A. Also, if we can ship the packages in the required days with capacity B, we can always ship them
         with a capacity greater than B.

         A scenario like this where the task is to search for an element X from a given range (L, R) where all values
         smaller than X do not satisfy a certain condition and all values greater than or equal to X satisfy it (or
         vice-versa), can be solved optimally with a binary search.

         Therefore, the question becomes binary search to find the minimum weight capacity of the ship between
         the two boundaries defined above.

        We set mid = (left + right) / 2 as the current weight capacity of the ship.
        To check whether we can ship all the packages with the given capacity mid, we create define two variables,
        days_needed = 1 and cur_load = 0 which store the total number of days needed to ship all the weights with
        mid ship capacity and to keep track of how much weight has been placed in the ship on a day, respectively.

        We iterate over all the weights, and for each weight, we place the weight in the ship and increase its load to
        cur_load = cur_load + weight. We keep on placing the weights until cur_load > mid. If cur_load exceeds capacity,
        we cannot keep adding weight and need an additional day. So, we increase the days needed to ship the packages
        by one, i.e., days_needed += 1 we also set cur_load = weight as this is the current load for the next day.

        If we can ship the packages with mid as the ship's capacity in less than or equal to the days' limit, we move to
        the lower half of the range by setting right = mid - 1. Otherwise, if we cannot ship the packages with
        capacity=mid in the required days, we move to the upper half of the range by setting left = mid + 1.

        NOTE: binary search using predicate
        f(mid) = days_needed_to_ship_with_capacity_mid > days
        -> [T, T, ..., T, F, F, ..., F]
        -> Find the first F

    Time complexity: O(N logN)
    Space complexity: O(1)
    """
    left, right = max(weights), sum(weights)
    while left <= right:
        mid = (left + right) // 2
        # loaded capacity of current ship and number of days needed
        cur_load, days_needed = 0, 1
        # ---- Simulating loading the weight to ship one by one ---- #
        for weight in weights:
            cur_load += weight
            if cur_load > mid:
                # Current ship meets its capacity
                cur_load = weight
                days_needed += 1
        # --------------- simulation ends -------------------------- #
        if days_needed > days:
            # We needed too many days, so we need to increase capacity to reduce number of days needed
            left = mid + 1
        else:
            # We were able to ship within good number of days, but we still need to find the optimal minimum capacity
            right = mid - 1
    return left


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 15), ([3, 2, 2, 4, 1, 4], 3, 6), ([1, 2, 3, 1, 1], 4, 3)]

    def test_ship_within_days(self):
        for test_weights, test_d, result in self.data:
            self.assertEqual(result, ship_within_days(test_weights, test_d))


if __name__ == '__main__':
    unittest.main()

""" A conveyor belt has packages that must be shipped from one port to another within D days.
The i-th package on the conveyor belt has a weight of weights[i].  Each day, we load the ship with packages on the
conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship.
Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped
within D days. """

import unittest2 as unittest


def ship_within_days(weights, D):
    """ The answer to the problem has a minimum value and a maximum value i.e. that solution lies within a range.
        The minimum value being the maximum weight and the maximum value being the sum of all the weights.
        Therefore the question becomes Binary Search to find the minimum weight capacity of the ship between left and
        right. We start from mid = (left + right) / 2 as our current weight capacity of the ship.
        need = days needed == 1 ; cur_capacity = current cargo in the ship == 0
        Start putting cargo into ship in order. When need > D, it means the current ship is too small, we modify
        left = mid + 1 and continue. If all the cargo is successfully put into need, we might have a chance to find a
        smaller ship, so let right = mid and continue. Finally, when our left == right, we reach our answer.
        One thing to note in Binary Search for this problem, is even if we end up finding a weight that gets us to D
        partitions, we still want to continue the space on the minimum side, because there could be a better minimum
        sum that still passes <= D partitions.
    Time complexity: O(N + logN) = O(N)
    Space complexity: O(1)
    """
    left, right = max(weights), sum(weights)
    while left < right:
        mid = (left + right) // 2
        cur_capacity, need = 0, 1  # loaded capacity of current ship and number of days needed
        # ----simulating loading the weight to ship one by one----#
        for weight in weights:
            cur_capacity += weight
            if cur_capacity > mid:  # current ship meets its capacity
                cur_capacity = weight
                need += 1
        # ---------------simulation ends--------------------------#
        if need > D:  # We needed too many days, so we need to increase capacity to reduce number of days needed
            left = mid + 1
        else:  # We were able to ship within good number of days, but we still need to find the optimal minimum capacity
            right = mid
    return left


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 15), ([3, 2, 2, 4, 1, 4], 3, 6), ([1, 2, 3, 1, 1], 4, 3)]

    def test_ship_within_days(self):
        for test_weights, test_d, result in self.data:
            self.assertEqual(result, ship_within_days(test_weights, test_d))


if __name__ == '__main__':
    unittest.main()

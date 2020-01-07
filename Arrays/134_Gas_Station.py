""" There are N gas stations along a circular route, where the amount of gas at station i is gas[i].
You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from station i to its next station
(i+1). You begin the journey with an empty tank at one of the gas stations.
Return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise
return -1. """

import unittest2 as unittest


def can_complete_circuit_v1(gas, cost):
    """ Let's notice two things.
        1- It's impossible to perform the road trip if sum(gas) < sum(cost). In this situation the answer is -1.
           We could compute total amount of gas in the tank total_tank = sum(gas) - sum(cost) during the round trip,
           and then return -1 if total_tank < 0.
        2- It's impossible to start at a station i if gas[i] - cost[i] < 0, because then there is not enough gas in the
           tank to travel to i + 1 station.
           The second fact could be generalized.
        Let's introduce current_gas variable to track the current amount of gas in the tank. If at some station
        current_gas is less than 0, that means we couldn't reach next station. Next step is to mark next station as a
        new starting point, and reset current_gas to zero since we start with no gas in the tank.
        Now the algorithm is straightforward :
        Initiate total_gas and current_gas as zero, and choose station 0 as a starting station.
        Iterate over all stations :
            - Update total_gas and current_gas at each step, by adding gas[i] and subtracting cost[i].
            - If current_gas < 0 at station i, make station (i + 1) a new starting point and reset current_gas = 0 to
              start with an empty tank.
        Return starting station if total_gas >= 0 and -1 otherwise.
        Why this works ?
        There's an assumption that can be made that isn't well-clarified, which is that if total_tank >= 0, then no
        matter what there is a solution that will work, so we're simply figuring out which one it is. In other words,
        we don't actually have to loop around to prove it works because it's already been proven (see point 1- above).
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(gas)
    total_gas = current_gas = start = 0
    for i in range(n):
        total_gas += gas[i] - cost[i]
        current_gas += gas[i] - cost[i]
        if current_gas < 0:  # If we couldn't get to station (i + 1)
            start = i + 1  # Pick up the next station as the starting position
            current_gas = 0  # Start with an empty tank
    return start if total_gas >= 0 else -1


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3), ([2, 3, 4], [3, 4, 3], -1)
            ]

    def test_can_complete_circuit(self):
        for test_gas, test_cost, result in self.data:
            self.assertEqual(result, can_complete_circuit_v1(test_gas, test_cost))


if __name__ == '__main__':
    unittest.main()

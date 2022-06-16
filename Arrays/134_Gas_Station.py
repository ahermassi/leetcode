""" There are N gas stations along a circular route, where the amount of gas at station i is gas[i].
You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from station i to its next station
(i+1). You begin the journey with an empty tank at one of the gas stations.
Return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise
return -1. """

import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=lJwbPZGo05A


def can_complete_circuit_v1(gas, cost):
    """ The first idea is to check every single station :

            - Choose the station as starting point.
            - Perform the road trip and check how much gas we have in tank at each station.

         That means O(N^2) time complexity, and for sure we could do better.

         Let's notice two things.

            1- It's impossible to perform the road trip if sum(gas) < sum(cost). In this situation the answer is -1.
                 We could compute total amount of gas in the tank total_tank = sum(gas) - sum(cost) during the round
                 trip, and then return -1 if total_tank < 0.

            2- It's impossible to start at a station i if gas[i] - cost[i] < 0, because then there is not enough gas in
                 the tank to travel to station (i + 1).

        The second fact could be generalized.

        Let's introduce current_tank variable to track the current amount of gas in the tank. If at some station
        current_tank is less than 0, that means we couldn't reach next station. Next step is to mark next station as a
        new starting point, and reset current_tank to zero since we start with no gas in the tank.

        Now the algorithm is straightforward:

            - Initiate total_gas and current_tank as zero, and choose station 0 as a starting station.

            - Iterate over all stations:

                - Update total_gas and current_tank at each step, by adding gas[i] and subtracting cost[i].
                - If current_tank < 0 at station i, make station (i + 1) a new starting point and reset current_tank = 0
                   to start with an empty tank.

            - Return starting station if total_gas >= 0 and -1 otherwise.

        We visit gas stations in series of stages one station at a time. At each stage we select the best station to
        start our trip from . The best station to start our trip from is the station that can get us to the next gas
        station. if there is no best station at given stage, we do not make a selection and move on to the next stage.

        Suppose at stage 0 we have to make the decision of whether we select station 0 as the best station thus far.
        We defined the best station as the station that can get our car to the next station. The car can only get to the
        next station if the car has enough gas.

        When we run out of fuel at station i, why start from station i+1 ?

        If car starts at A and can not reach B, then any station between A and B can not reach B.
        Proof: Let's assume that:

            - A cannot reach B
            - There are C1,C2, ..., Ck between A and B
            - A can reach C1, C2, ..., Ck

        A --- C1 --- C2  --- ... Ck --- B

        Assume that C1 can reach B.
        => A can reach C1 (by Fact 3) & C1 can reach B
        => A can reach B (contradiction with Fact1 !)
        => Assumption is wrong; C1 cannot reach B
        Same proof by contradiction could be applied to C2 ~ Ck
        => Any station between A and B that A can reach cannot reach B

        When the algorithm returns N_s as a starting station, it directly ensures that it's possible to go from N_s to
        the station 0. But what about the last part of the round trip from the station 0 to the station N_s? How could
        we ensure that it's possible to loop around to N_s ?

        We are resetting start as soon as current_tank dips below 0 and setting it to the next index. Let's say the last
        update to start index was at index k where 0 <= k < n.

        At the end of the iteration, current_tank contains the total amount of fuel collected from the last updated
        start index till the end of tha array:
                    current_tank = (gas[k] - cost[k]) + (gas[k + 1] - cost[k + 1]) + ... + (gas[n - 1] - cost[n - 1])

        This current_tank must be able to offset the net fuel consumption before the kth index so that we are able to
        circle back and finish at the index k.
                    Net Fuel Consumption Before k = (gas[0] - cost[0]) + (gas[1] - cost[1]) + ... + (gas[k - 1] - cost[k - 1])

        Now, total_gas contains the total fuel collected from the 0th to the (n-1)th index:
                    total_gas = (gas[0] - cost[0]) + (gas[1] - cost[1]) + ... (gas[n - 1] - cost[n -1]);

        This means that: Net Fuel Consumption Before k = total_gas - current_tank

        This implies that if (current_tank + (total_gas - current_tank)) >= 0 then the current start index is the
        correct answer. (current_tank + (total_gas - current_tank)) >= 0 is the same as total_gas >= 0.

        Less formally: We know that we would be able to reach from 0 to k-1 without any difficulty. Having started with
        zero fuel and now that we know that after traversing from k to the end we have some fuel left, so that extra
        fuel will help us traverse from k-1 to k when verifying the circular tour (we've already checked that it's
        possible to travel from the 0th index to k-1).

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(gas)
    total_gas = current_tank = start = 0
    for i in range(n):
        total_gas += gas[i] - cost[i]
        current_tank += gas[i] - cost[i]
        if current_tank < 0:  # If we couldn't get to station (i + 1)
            start = i + 1  # Pick up the next station as the starting position
            current_tank = 0  # Start with an empty tank
    return start if total_gas >= 0 else -1


def can_complete_circuit_v2(gas, cost):
    """ Same solution as above but with two differences:
            1- We check the condition sum(gas) < sum(cost) beforehand and return -1 if it's verified.
            2- Because of that, this solution performs 2 passes over the arrays instead of 1 pass.
        Note that in the previous solution (sum(gas) - sum(cost)) is being accumulated during the execution of the
        algorithm using 'total_gas' variable: sum(gas) - sum(cost) = sum(i=0..n-1) {gas[i] - cost[i]}. total_gas < 0
        is checked at the end.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if sum(gas) < sum(cost):
        return -1
    n = len(gas)
    current_gas = start = 0
    for i in range(n):
        current_gas += gas[i] - cost[i]
        if current_gas < 0:
            start = i + 1
            current_gas = 0
    return start


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3), ([2, 3, 4], [3, 4, 3], -1)
            ]

    def test_can_complete_circuit(self):
        for test_gas, test_cost, result in self.data:
            self.assertEqual(result, can_complete_circuit_v1(test_gas, test_cost))
            self.assertEqual(result, can_complete_circuit_v2(test_gas, test_cost))


if __name__ == '__main__':
    unittest.main()

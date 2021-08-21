""" There is a car with capacity empty seats. The vehicle only drives east (i.e., it cannot turn around and drive west).

You are given the integer capacity and an array trips where trip[i] = [numPassengers_i, from_i, to_i] indicates that the
ith trip has numPassengers_i passengers and the locations to pick them up and drop them off are from_i and to_i
respectively. The locations are given as the number of kilometers due east from the car's initial location.

Return true if it is possible to pick up and drop off all passengers for all the given trips, or false otherwise. """

from collections import defaultdict
from heapq import heappop, heappush


def car_pooling_v1(trips, capacity):
    """ We first sort trips by start location, because that’s how the question is framed - we go in one direction and
        cannot turn back. That’s how we must iterate through the trips array.
        We put the whole trip’s information into the priority queue. Why? Because we will eventually need the number of
        passengers of the trip and its end location.
        Now that we have put our first trip into the priority queue, we look at our next trip. We have two possible
        scenarios:
            - Our next trip’s start location were to be less than the end location of the trip we just stored
              (with lowest / nearest end location trips at the top of the heap). Since we need to pick up more
              passengers, we once again increase our counterent number of passengers.
            - Our next trip’s start location is greater than or equal to the trip’s end location that we just stored
              previously. We let out some passengers, and therefore we can decrease the counterent number of passengers.
        If the counterent number of passengers were ever to go exceed the capacity, we return false.
        The priority queue is like the “car” (maybe more like a big bus) in some sense, because it stores passengers
        such that the ones who will get off soon should sit near the front. The bus receives information about its next
        trip to make, and if the next trip’s start location is beyond what the counterent passengers destinations, those
        counterent passengers get off.
    Time complexity: O(N logN), where N is the number of trips
    Space complexity: O(N)
    """

    trips.sort(key=lambda passengers, start, end: start)
    heap = []
    occupancy = 0
    for passengers, start, end in trips:
        while heap and heap[0][0] <= start:  # Any passengers need to get off?
            occupancy -= heap[0][1]  # Less occupancy as some passengers out
            heappop(heap)
        heappush(heap, (end, passengers))
        occupancy += passengers  # More occupancy as some passengers in
        if occupancy > capacity:  # Not enough capacity
            return False
    return True


def car_pooling_v2(trips, capacity):
    """ A simple idea is to go through the trips from the start to end and check if the current number of passengers
        exceeds capacity. To find that out, we just need the number of passengers changed at each timestamp.
        We can save the number of passengers changed at each time, sort it by timestamp, and finally iterate it to
        check the actual capacity.
        Process all trips, adding passenger count to the start location, and removing it from the end location since
        they will leave the car at that point. After processing all trips, a positive value for the specific location
        tells that we are getting more passengers; negative means more empty seats.
        Finally, scan all stops and check if we ever exceed our vehicle capacity.
        Example: trips = [[3,2,7],[3,7,9],[8,3,9]], capacity = 11. Trips can be represented it in the following way:
            # # 3 3 3 3 3 # # #
            # # # # # # # 3 3 3
            # # # 8 8 8 8 8 8 8
        Initially:      counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        After trip 1:   counter = [0, 0, 3, 0, 0, 0, 0, -3, 0, 0]
        After trip 2:   counter = [0, 0, 3, 0, 0, 0, 0, 0, 0, -3]
        After trip 3:   counter = [0, 0, 3, 8, 0, 0, 0, -3, 0, -11]
        Now, if we start adding elements of array up to, say index i, then at i we will get the maximum people which
        can be accommodated in the car.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    counter = defaultdict(int)
    for passengers, start, end in trips:
        counter[start] += passengers
        counter[end] -= passengers
    occupancy = 0
    for timestamp in sorted(counter.keys()):  # Go over the timestamps in a chronological order
        occupancy += counter[timestamp]
        if occupancy > capacity:
            return False
    return True


def car_pooling_v3(trips, capacity):
    """ Note that in the problem there is a interesting constraint:
            0 <= trips[i][1] < trips[i][2] <= 1000
        What comes to mind is Bucket Sort, which is a linear time sorting algorithm that requires some prior knowledge
        about the range of data. We can use it instead of the normal sorting.
        We initialize 1001 buckets and put the number of passengers changed in corresponding buckets. Finally, we scan
        all stops and check if we ever exceed our vehicle capacity.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    counter = [0] * 1001
    for passengers, start, end in trips:
        counter[start] += passengers
        counter[end] -= passengers
    occupancy = 0
    for passengers in counter:
        occupancy += passengers
        if occupancy > capacity:
            return False
    return True

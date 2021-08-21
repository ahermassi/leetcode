""" There is a car with capacity empty seats. The vehicle only drives east (i.e., it cannot turn around and drive west).

You are given the integer capacity and an array trips where trip[i] = [numPassengers_i, from_i, to_i] indicates that the
ith trip has numPassengers_i passengers and the locations to pick them up and drop them off are from_i and to_i
respectively. The locations are given as the number of kilometers due east from the car's initial location.

Return true if it is possible to pick up and drop off all passengers for all the given trips, or false otherwise. """

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
              passengers, we once again increase our current number of passengers.
            - Our next trip’s start location is greater than or equal to the trip’s end location that we just stored
              previously. We let out some passengers, and therefore we can decrease the current number of passengers.
        If the current number of passengers were ever to go exceed the capacity, we return false.
        The priority queue is like the “car” (maybe more like a big bus) in some sense, because it stores passengers
        such that the ones who will get off soon should sit near the front. The bus receives information about its next
        trip to make, and if the next trip’s start location is beyond what the current passengers destinations, those
        current passengers get off.
    Time complexity: O(N logN), where N is the number of trips
    Space complexity: O(N)
    """

    trips.sort(key=lambda passengers, start, end: start)
    heap = []
    passengers = 0
    for num, start, end in trips:
        while heap and heap[0][0] <= start:  # Any passengers need to get off?
            passengers -= heap[0][1]  # Less passengers as some out
            heappop(heap)
        heappush(heap, (end, num))
        passengers += num  # More passengers as some in
        if passengers > capacity:  # Not enough capacity
            return False
    return True

""" There are n cars going to the same destination along a one-lane road. The destination is target miles away.

You are given two integer array position and speed, both of length n, where position[i] is the position of the ith car
and speed[i] is the speed of the ith car (in miles per hour).

A car can never pass another car ahead of it, but it can catch up to it and drive bumper to bumper at the same speed.
The faster car will slow down to match the slower car's speed. The distance between these two cars is ignored
(i.e., they are assumed to have the same position).

A car fleet is some non-empty set of cars driving at the same position and same speed. Note that a single car is also
a car fleet.

If a car catches up to a car fleet right at the destination point, it will still be considered as one car fleet.

Return the number of car fleets that will arrive at the destination. """

# Video explanation: https://www.youtube.com/watch?v=H5w6doOXz10


def car_fleet_v1(target, position, speed):
    """ How can we know if a car can catch up with the car in front of it? If we calculate the time each car needs
        to reach the target without any blockers, then the car that has shorter time can catch up with other cars ahead
        of it.

        Sort the cars by their start positions. Then, loop through each car in reverse order of their positions, so the
        rightmost positioned car is the car that is the closest to the target.
        With that in mind, calculate the time needed for each car to arrive to the target, where 'slowest_car_time'
        records the current slowest arrival time.

        If the current car needs less or equal time than 'slowest_car_time' (head of the fleet), it can catch up with
        this car fleet.
        If it needs more time than the car ahead (head of the fleet), it will be the new slowest car and becomes the
        lead of a new car fleet.

        Even if the car catches up to a slower car, that doesn't change the fact that the only way to make more fleets
        is if cars behind actually go slower than the slowest we have seen so far. A faster car, even after slowing
        down when joining a fleet, won't change our slowest time.

        So the idea is: If a car located further away from target arrives at target with less time compared to cars
        closer to target, they will bump into a group.

        Why process the cars in the reverse order of their positions? Since the car farther away is the closest to the
        target, therefore, it will definitely lead a fleet since no car behind it can pass it.

    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    n = len(position)
    positions_and_speeds = sorted(zip(position, speed))
    fleet, slowest_car_time = 0, 0
    for i in reversed(range(n)):
        position, speed = positions_and_speeds[i]
        time_to_target = (target - position) / speed
        if time_to_target > slowest_car_time:
            # If the current car behind takes more time to reach the target than the head of the fleet, that means
            # the two cars are separated, so we will increase the fleet count
            fleet += 1
            slowest_car_time = time_to_target
    return fleet


def car_fleet_v2(target, position, speed):
    """  Similar to previous solution but using a stack to track the fleets of cars.

        Since the first vehicle will always lead a fleet, starting from the second vehicle, compare each vehicle's
        ideal arrival time with the arrival time of the fleet in front of it, i.e., stack[-1]. If its ideal arrival time
        is earlier, it will join the fleet in front of it. Otherwise, it will lead a new fleet, and we append its arrival
        time into the stack.

        Finally, the stack contains the arrival times of the fleets and the length of stack will be the number of
        distinct arrival times, i.e., the number of fleets.

        This problem fits the pattern of what we can call "allocating resources to overlapping events".
        In this kind of problems, it's usually the case that we have to sort the items with respect to some feature and
        process them one at a time while constantly checking the previous items by popping from a stack.
        Many greedy problems require sorting and processing things in order while checking if the current item
        overlaps/dissolves into its predecessor (the previous item).

    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    n = len(position)
    positions_and_speeds = sorted(zip(position, speed))
    stack = []
    for i in reversed(range(n)):
        position, speed = positions_and_speeds[i]
        time_to_target = (target - position) / speed
        if not stack or time_to_target > stack[-1]:
            stack.append(time_to_target)
        # If curr time_to_target is = previous time_to_target, then the current car joins the previous fleet and
        # gets dissolved into it (aka we don't need to do anything)
    return len(stack)

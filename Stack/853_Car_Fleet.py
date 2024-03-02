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
         to reach the target without any blockers, then the car that needs shorter time can catch up with the other cars
         ahead of it.

            - Sort the cars by their start positions.

            - Loop over the cars' positions in reverse order, so the rightmost position is the car that is closest to
               the target.

            - Calculate the time needed for each car to reach the target, where 'current_fleet_time' is the time needed
               by the fleet ahead of the current car to reach the target.

                    * If the current car needs less or equal time than 'current_fleet_time', it can join this fleet.
                    * Otherwise, if it needs more time than the 'current_fleet_time', the car will become the head of a
                       new car fleet, and 'current_fleet_time' is now the time needed by the current car to reach the
                       target.

         Even if the car catches up to a slower car, that doesn't change the fact that the only way to make more fleets
         is if cars behind actually go slower than the slowest we have seen so far. A faster car, even after slowing
         down when joining a fleet, won't change the slowest time.

         So the idea is: Keep track of the time needed to arrive at the target. Whenever a car's time is less than or
         equal to the time of the car in the fleet ahead, they will form a fleet together.

         Why process the cars in the reverse order of their positions? Since the car farther away is the closest to the
         target, therefore, it will definitely lead a fleet since no car behind it can pass it. If we start processing
         the first car to the left and want to know if it would collide with the second car, we don't even know at what
         speed the second car is going to be traveling throughout the whole trip. We can't just assume it's traveling
         at its initial speed the entire time because it could collide with another car ahead of it and slow down.

    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    n = len(position)
    cars = [(position[i], speed[i]) for i in range(n)]
    cars.sort()
    fleet, current_fleet_time = 0, 0
    for i in reversed(range(n)):
        position, speed = cars[i]
        time_to_target = (target - position) / speed
        if time_to_target > current_fleet_time:
            # If the current car behind takes more time to reach the target than the head of the fleet, that means
            # the two cars are separated, so the current car creates a new fleet
            fleet += 1
            current_fleet_time = time_to_target
    return fleet


# Video explanation: https://youtu.be/Pr6T-3yB9RM
def car_fleet_v2(target, position, speed):
    """  Similar to the previous solution but using a stack to track the fleets of cars.

         Since the first vehicle will always lead a fleet, starting from the second vehicle, compare each vehicle's
         ideal arrival time with the arrival time of the fleet in front of it, i.e., stack[-1]. If its ideal arrival time
         is earlier, it will join that fleet. Otherwise, it will lead a new fleet, and we push its arrival time to the
         stack.

         Finally, the stack contains the arrival times of the fleets and the length of the stack is the number of
         distinct arrival times, i.e., the number of fleets.

         This problem fits the pattern of what we can call "allocating resources to overlapping events".
         In this type of problems, it's usually the case that we have to sort the items with respect to some feature and
         process them one at a time while constantly checking the previous items by popping from a stack.
         Many greedy problems require sorting and processing things in order while checking if the current item
         overlaps/dissolves into its predecessor.

    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    n = len(position)
    cars = [(position[i], speed[i]) for i in range(n)]
    cars.sort()
    stack = []
    for i in reversed(range(n)):
        position, speed = cars[i]
        time_to_target = (target - position) / speed
        if not stack or time_to_target > stack[-1]:
            stack.append(time_to_target)
        # If the current time_to_target is less than or equal to the previous time_to_target, then the current car joins
        # the previous fleet and gets dissolved into it (aka we don't need to do anything)
    return len(stack)

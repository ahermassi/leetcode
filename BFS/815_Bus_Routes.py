""" You are given an array routes representing bus routes where routes[i] is a bus route that the ith bus repeats
forever.

For example, if routes[0] = [1, 5, 7], this means that the 0th bus travels in the sequence 1 -> 5 -> 7 -> 1 -> 5 -> 7
-> 1 -> ... forever.
You will start at the bus stop source (You are not on any bus initially), and you want to go to the bus stop target.
You can travel between bus stops by buses only.

Return the least number of buses you must take to travel from source to target. Return -1 if it is not possible. """

from collections import defaultdict, deque


def num_buses_to_destination(routes, source, target):
    """ Instead of thinking of the stops as nodes (of a graph), think of the buses as nodes. We want to take the least
        number of buses, which is a shortest path problem, conducive to using a breadth-first search.

        For each of the bus stops, we maintain all the buses (bus routes) that go through it. To do that, we use a
        hash map, where bus stop number is the key and all the buses (bus routes) that go through it are added to a
        list.

        We use BFS where we process elements in a level-wise manner. We add the source bus stop to the queue. Next,
        when we enter the while loop, we add all the bus stops that are reachable by all the bus routes that go via the
        current stop. Thus, if we have the input as routes = [[1, 2, 7], [3, 6, 7]] and source as 6, then upon
        processing bus stop 6 we would add bus stops 3 and 7.

        With this approach, all the bus stops at a given level are "equal distance" from the start node in terms of
        number of buses that need to be changed. To avoid loops, we also maintain a hash set that stores the buses that
        we have already taken.

        It might also help to clearly state that the shortest route from one stop to another is not the priority.
        Example: If there's Bus 1 with the following stops: [1,2,3,4,5,6,7,8,9,10], and Bus 2 with the following stops:
        [2,7]
        If your goal is to go from stop 1 to stop 7: 1 => 7
        A potential answer/route could be 1->2->3->4->5->6->7 which uses 1 bus and 6 moves, or 1->2->7 which uses 2
        buses and just 2 moves.
        In this case the first route would be the answer because there's less buses in use.

    Time complexity: O(N), where N is the total number of stops in the routes. Let's say we start with 'source'. Now
    we travel the buses that are passing through 'source' and mark these buses as visited. Doing this marks all the
    stops in routes[i] (where i = buses visiting 'source') visited. This way we visited all the stops present in the
    routes[i]. Thus marking a total of nodes/stops present in routes.
    Space complexity: O(S + B), where S is the number of stops and B is the number of buses
    """
    if source == target:
        return 0
    routes = [set(route) for route in routes]
    stop_to_buses = defaultdict(list)
    # We need to record all the buses we can take at each stop so that we can find out all of the stops we can reach
    # when we take one of the buses. The key is the stop and the value is all of the buses we can take at this stop.
    for bus_number, stops in enumerate(routes):
        for stop in stops:
            stop_to_buses[stop].append(bus_number)
    queue = deque([(source, 0)])  # The queue is to record all of the stops we can reach when we take the buses
    buses_taken = set()  # Record the buses that have been taken before because we don't need to take them again
    while queue:
        cur_stop, distance = queue.popleft()
        if cur_stop == target:
            return distance
        # At each stop we can take at least one bus, so we need to traverse all of the buses at this stop in order to
        # get all of the stops that can be reached at this time.
        for bus in stop_to_buses[cur_stop]:
            if bus not in buses_taken:  # We don't want to travel in same bus as we might be stuck in a loop
                buses_taken.add(bus)
                # Now we are in a bus, we will travel to all the stops that the bus goes to
                for stop in routes[bus]:
                    queue.append((stop, distance + 1))
    return -1

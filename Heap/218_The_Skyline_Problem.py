""" View description on Leetcode. """

from heapq import heappush, heappop
import unittest2 as unittest


# Check out 6th comment on this thread (although it uses removal from heap, it explains the intuition behind the
# solution): https://leetcode.com/problems/the-skyline-problem/discuss/61193/Short-Java-solution

def get_skyline(buildings):
    """ By drawing most of the possible overlaps, we can find that all key points can be divided into two categories:
        entry points and exit points.
        For the entry point:
            - If the building entered at the moment is the tallest, then its starting point is a key point.
            - If it is not the tallest or the same height as the current tallest building, it means that the entry
              point is overshadowed by a taller building and there is no need to add the key point.
        For the exit point:
            - If the building is the current tallest, its departure will definitely cause the building that was lower
              than it to be exposed, so the corresponding key point height is the height of the building a little lower
              than the departing building.
            - Otherwise, its departure will have no effect on the skyline, so no update is required.
        First, consider the entry point. For the coordinates (L, R, H) of each building, we first sort by the left
        subscript, that is, the key is L. But when the lower left of the two buildings are the same, we should give
        priority to the higher building. Therefore, the key is (L, -H). Then, consider the exit point. The right
        subscript of the exit point can also be used as L and the entry point to be sorted together.
        In order to distinguish between the entry point and the exit point, we express the entry point as (L, -H, R)
        and the exit point as (R, 0, 0), so there are only three values ​​in the tuple of the entry point.
        Use an infinite vertical line x to scan from left to right. If max height changes, record [x, height] in res.
        First, sort the critical points by their left endpoints.
        We only push right end points onto the heap. Think of it as a proxy for the entire rectangle. The key is a
        negative height because heapq implements min-heap. The heap keeps track of the current max height.
        In the for loop, when we encounter a left end point that comes after the farthest end point of previous
        buildings (start >= heap[0][1]), we pop until all right endpoints that are smaller than the current left end
        point are gone. Interestingly, we don't traverse through the heap and remove a rectangle every time an incoming
        left endpoint comes along, because we only care about the max height, aka, heap[0][0].
        Check if the maximum height changes in heap after each iteration. If so, then add current max height and
        current coordinate to result array.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    start_events = [(left, -height, right) for left, right, height in buildings]
    end_events = [(right, 0, 0) for _, right, height in buildings]
    events = sorted(start_events + end_events)
    live_buildings, res = [(0, float('inf'))], []  # live_buildings: heap, [-height, ending position]
    previous_highest = 0
    for start, cur_height, end in events:
        while live_buildings[0][1] <= start:  # Pop buildings that have already ended
            heappop(live_buildings)
        if cur_height < 0:  # If it's the start-building event, make the building alive
            heappush(live_buildings, (cur_height, end))
        if previous_highest != -live_buildings[0][0]:
            previous_highest = -live_buildings[0][0]
            res.append([start, -live_buildings[0][0]])
    return res


class Test(unittest.TestCase):
    data = [([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]],
             [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]])]

    def test_get_skyline(self):
        for test_buildings, result in self.data:
            self.assertEqual(result, get_skyline(test_buildings))


if __name__ == '__main__':
    unittest.main()

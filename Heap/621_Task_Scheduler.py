""" Given a char array representing tasks CPU need to do. It contains capital letters A to Z where different letters
represent different tasks. Tasks could be done without original order. Each task could be done in one interval. For
each interval, CPU could finish one task or just be idle.
However, there is a non-negative cooling interval n that means between two same tasks, there must be at least n
intervals that CPU are doing different tasks or just be idle.
You need to return the least number of intervals the CPU will take to finish all the given tasks. """

from collections import Counter
from heapq import heappush, heappop
import unittest2 as unittest


def least_interval(tasks, n):
    """ The main idea is to schedule the most frequent tasks as frequently as possible. The reason for this is that
        if we run the most frequent task first, we have a better chance of not running into the idle state. So ideally
        the CPU needs to be idle as little as possible.
        Begin with scheduling the most frequent task. Then cool-off for n, and in that cool-off period schedule tasks
        in order of frequency, or if no tasks are available, then be idle.
        The trick is that Python does not have a max heap queue, so we must make every number's negative value when we
        add it into the heap.
        We start by picking up the largest task from the heap for current execution and increment the 'worktime as well.
        We also decrement its pending number of instances and if any more instances of the current task are pending,
        we store them in a temporary 'temp' list to be added later on back into the heap. We keep on doing so, till a
        cycle of cooling time has been finished. After every such cycle, we add the generated 'temp' list back to the
        heap for considering the most critical task again.
        We keep on doing so till the heap becomes totally empty.
        At the end of each while loop iteration, we update 'current_time'. If the (new) heap is not empty, we know that
        a full cycle of tasks and idle states has been completed. If the heap is empty, we only account for the actual
        work time of tasks because CPU can't be idle after finishing the execution of the complete set of tasks.
        You can see the idle state as a filler when the number of distinct tasks is less than the cycle length.
    Time complexity: O(N * n) where N is the number of tasks and n is the cool-off period
    Space complexity: O(1), will not be more than O(26) (tasks are capital letters A to Z)
    """
    counter, heap, cycle = Counter(tasks), [], n + 1
    for k, v in counter.items():
        heappush(heap, -v)  # Negative values create a max heap
    current_time = 0
    while heap:
        worktime, temp = 0, []
        for _ in range(cycle):
            if heap:
                instances = heappop(heap)
                worktime += 1
                if instances != -1:
                    temp.append(instances + 1)
        for instance in temp:
            heappush(heap, instance)
        current_time += cycle if heap else worktime
    return current_time


class Test(unittest.TestCase):
    data = [(['A', 'A', 'A', 'B', 'B', 'B'], 2, 8)]

    def test_least_interval(self):
        for test_tasks, test_n, result in self.data:
            self.assertEqual(result, least_interval(test_tasks, test_n))


if __name__ == '__main__':
    unittest.main()
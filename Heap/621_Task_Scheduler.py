""" Given a char array representing tasks CPU need to do. It contains capital letters A to Z where different letters
represent different tasks. Tasks could be done without original order. Each task could be done in one interval. For
each interval, CPU could finish one task or just be idle.
However, there is a non-negative cooling interval n that means between two same tasks, there must be at least n
intervals that CPU are doing different tasks or just be idle.
You need to return the least number of intervals the CPU will take to finish all the given tasks. """

from collections import Counter, defaultdict
from heapq import heappush, heappop
import unittest2 as unittest


def least_interval_v1(tasks, n):
    """ The main idea is to schedule the most frequent tasks as frequently as possible. The reason for this is that
        if we run the most frequent task first, we have a better chance of not running into the idle state. So ideally
        the CPU needs to be idle as little as possible.
        Begin with scheduling the most frequent task. Then cool-off for n, and in that cool-off period schedule tasks
        in order of frequency, or if no tasks are available, then be idle.
        The trick is that Python does not have a max heap queue, so we must make every number's negative value when we
        add it into the heap.
        We start by picking the largest task from the heap for current execution and increment the 'work_time' as well.
        We also decrement its pending number of instances, and if any more instances of the current task are pending,
        we store them in a temporary 'temp' list to be added later on back into the heap. We keep on doing so, till a
        cycle of cooling time has been finished. After every such cycle, we add the generated 'temp' list back to the
        heap for considering the most critical task again. If either the heap or the temporary heap list becomes empty
        during an iteration, it means there are no more tasks to schedule and we break early.
        We keep on doing so till the heap becomes totally empty.
        You can see the idle state as a filler when the number of distinct tasks is less than the cycle length.
    Time complexity: O(n * logN) ~= O(n * log(26)) ~= O(n), where N is the number of tasks and n is the cool-off period
    Space complexity: O(1), there will not be more than O(26) (tasks are capital letters A to Z)
    """
    counter, heap = Counter(tasks), []
    for task, instances in counter.items():
        heappush(heap, -instances)  # Negative values create a max heap
    cycle = n + 1
    work_time = 0
    while heap:
        temp = []
        for _ in range(cycle):
            work_time += 1
            if heap:
                instances = -heappop(heap)
                if instances != 1:
                    temp.append(instances - 1)
            if not heap and not temp:  # Check if we're out of tasks
                break
        # Because we transferred all of the items from the heap to temp, we're transferring them back to know if we
        # should continue
        for instance in temp:
            heappush(heap, -instance)
    return work_time


def least_interval_v2(tasks, n):
    """ The key is to find out how many idles we need.
        Let's first look at how to arrange them. It's not hard to figure out that we can do a 'greedy arrangement':
        always arrange tasks with most frequency first.
        E.g. we have the following tasks : 3 A, 2 B, 1 C, and we have n = 2. According to what we have above, we
        should first arrange A, and then B and C. Imagine there are 'slots' and we need to arrange tasks by putting
        them into these 'slots'. A should be put into slots 0, 3, 6 since we need to have at least n = 2 other tasks
        between two As. After A is placed, it looks like this:
            A ? ? A ? ? A
        where '?' is empty slots
        Now we can use the same method to arrange B and C. The finished schedule should look like this:
            A B C A B # A
        where '#' is idle
        Now we have a way to arrange tasks. But the problem only asks for the number of CPU intervals, so we don't need
        to actually arrange them. Instead, we only need to get the total idles we need and the answer to problem is:
            number of idles + number of tasks
        Same example: 3 A, 2 B, 1 C, n = 2. After arranging A, we have:
            A ? ? A ? ? A
        We can see that A separated the slots into (count(A) - 1) = 2 parts, where each part has length n. With the
        fact that A is the task with most frequency, it should need more idles than any other tasks. In this case, if
        we can get how many idles we need to arrange A, we will also get the number of idles needed to arrange all
        tasks. Calculating this is not hard. We first get the number of parts separated by A:
            part_count = count(A) - 1
        Then we can find the number of empty slots:
            emptySlots = part_count * n
        We can also get how many tasks we have to put into those slots:
            available_tasks = tasks.length - count(A)
        Now if we have emptySlots > availableTasks which means we have not enough tasks available to fill all empty
        slots, we must fill them with idles. Thus we have:
            idles = max(0, emptySlots - availableTasks)
        Almost done. One special case: what if there is more than one task with max frequency ?
        OK, let's look at another example: 3 A, 3 B, 2 C, 1 D, n = 3
        Similarly we arrange A first:
            A ? ? ? A ? ? ? A
        Now it's time to arrange B. We find that we have to arrange B like this:
            A B ? ? A B ? ? A B
        We need to put every B right after each A. Let's look at this in another way: Think of sequence 'A B' as a
        special task 'X', then we get:
            X ? ? X ? ? X
        Comparing to what we have after arranging A:
            A ? ? ? A ? ? ? A
        The only changes are the length of each parts (from 3 to 2) and available tasks:
            emptySlots = part_count * (n - number of tasks with same max frequency + 1)
            available_tasks = tasks.length - max frequency * number of tasks with same max frequency
    Time complexity: O(n)
    Space complexity: O(1)
    """
    counter = defaultdict(int)
    total_tasks, max_frequency, same_max_frequency = len(tasks), 0, 0
    for task in tasks:
        counter[task] += 1
        max_frequency = max(max_frequency, counter[task])
    for v in counter.values():
        if v == max_frequency:
            same_max_frequency += 1
    parts = max_frequency - 1
    empty_slots = parts * (n - same_max_frequency + 1)
    available_tasks = total_tasks - max_frequency * same_max_frequency
    idles = max(0, empty_slots - available_tasks)
    return total_tasks + idles


class Test(unittest.TestCase):
    data = [(['A', 'A', 'A', 'B', 'B', 'B'], 2, 8)]

    def test_least_interval(self):
        for test_tasks, test_n, result in self.data:
            self.assertEqual(result, least_interval_v1(test_tasks, test_n))
            self.assertEqual(result, least_interval_v2(test_tasks, test_n))


if __name__ == '__main__':
    unittest.main()
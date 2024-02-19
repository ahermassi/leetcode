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

         Begin with scheduling the most frequent task. Then cool-off for n, and in that cooldown period schedule tasks
         in order of frequency, or if no tasks are available, then be idle.

         We start by choosing the most frequent task from the heap for current execution and increment the 'work_units'.
         We also decrement the task's number of pending instances, and if any more instances of the current task are
         pending, we store them in a temporary 'remaining' list to be added later on back to the heap.

         We keep doing that until a cycle of cooling time has been finished. After every such cycle, we add the
         'remaining' list back to the heap for the next scheduling iteration.

         If either the heap or the temporary list becomes empty during an iteration, it means there are no more tasks
         left to schedule, and we break early.

         We can see the idle state as a filler when the number of remaining distinct tasks is less than the cycle length.

    Time complexity: O(n * logN) ~= O(n * log(26)) ~= O(n), where N is the number of tasks and n is the cooldown period
    Space complexity: O(1), there will not be more than O(26) (tasks are capital letters A to Z)
    """
    counter, heap = Counter(tasks), []
    for task, instances in counter.items():
        heappush(heap, -instances)  # Negative values create a max heap
    cycle, work_time = n + 1, 0
    while heap:
        remaining, work_units = [], 0
        for _ in range(cycle):
            # Increment 'work_units'. If a task is pending in the heap, it's going to be actual work time. Otherwise,
            # it's idle time.
            # Idle time is the time that is needed in the cycle because no task is available. It is the remaining cycle
            # length. Idle time should be only added if the priority queue is empty and 'remaining' list is not.
            work_units += 1
            if heap:
                instances = -heappop(heap)
                if instances > 1:
                    remaining.append(instances - 1)
            # Check if we're out of tasks. If at any point the heap is empty (no more tasks to extract) and 'remaining'
            # list is empty (no more tasks to put back in the heap), we break out of the current cycle because CPU
            # can't be idle after finishing the execution of the entire set of tasks.
            if not heap and not remaining:
                break
        # Because we transferred all the items from the heap to 'remaining', we're transferring them back for the next
        # iteration of scheduling
        for instance in remaining:
            heappush(heap, -instance)
        work_time += work_units
    return work_time


def least_interval_v2(tasks, n):
    """ The key is to find out how many idles we need, and only the most frequent characters can create idles.

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

            empty_slots = part_count * n

        We can also get how many tasks we have to put into those slots:

            remaining_tasks = tasks.length - count(A)

        Now if we have empty_slots > remaining_tasks it means we don't have enough tasks available to fill all empty
        slots, we must fill them with idles.

        What if we have more than n tasks with most frequency, and we got empty_slots negative?
        Like 3A, 3B, 3C, 3D, 3E, n = 2. In this case it seems like we can't put all B C s inside slots since we only
        have n = 2.

        Well n is actually the "minimum" length of each part required for arranging A. We can always make the length
        of part longer. E.g. 3A, 3B, 3C, 3D, 2E, n = 2. We can always first arrange A, B, C, D as:

            A B C D | A B C D | A B C D

        In this case we have already met the "minimum" length requirement for each part (n = 2).
        empty_slots < 0 means we have already got enough tasks to fill in each part to make arranged tasks valid.

        The problem actually requires us to make the "distance" between two same tasks up to at least n. Thus,
        if empty_slots is negative, it means that we even have remaining tasks to make the "distance" between same
        tasks longer than n. That is, no idle is needed.

        Thus, we have:

            idles = max(0, empty_slots - remaining_tasks)

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

        The only changes are the length of each part (from 3 to 2) and available tasks:

            empty_slots = part_count * (n - number of tasks with same max frequency + 1)
            remaining_tasks = tasks.length - max frequency * number of tasks with same max frequency

    Time complexity: O(n)
    Space complexity: O(1)
    """
    frequency = defaultdict(int)
    total_tasks, max_frequency, same_max_frequency = len(tasks), 0, 0
    for task in tasks:
        frequency[task] += 1
        if frequency[task] > max_frequency:
            max_frequency = frequency[task]
            same_max_frequency = 1
        elif frequency[task] == max_frequency:
            same_max_frequency += 1
    parts = max_frequency - 1
    part_length = n - (same_max_frequency - 1)
    empty_slots = parts * part_length
    remaining_tasks = total_tasks - max_frequency * same_max_frequency
    idles = max(0, empty_slots - remaining_tasks)
    return total_tasks + idles


class Test(unittest.TestCase):
    data = [(['A', 'A', 'A', 'B', 'B', 'B'], 2, 8)]

    def test_least_interval(self):
        for test_tasks, test_n, result in self.data:
            self.assertEqual(result, least_interval_v1(test_tasks, test_n))
            self.assertEqual(result, least_interval_v2(test_tasks, test_n))


if __name__ == '__main__':
    unittest.main()
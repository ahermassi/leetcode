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

         Begin with scheduling the most frequent task. Then cool-off for n, and during that cooldown period schedule
         tasks in order of frequency, and if no tasks are available then be idle.

         We start by choosing the most frequent task from the heap for current execution and increment the 'work_units'.
         We also decrement the task's number of pending instances, and if any more instances of the current task are
         pending, we store them in a temporary 'remaining' list to be added later back to the heap.

         We keep doing that until a cycle of cooling time passes. After every such cycle, we add the 'remaining' list
         back to the heap for the next scheduling iteration.

         If either the heap or the temporary list becomes empty during an iteration, it means there are no more tasks
         left to schedule, and we break early.

         The idle state can be seen as a filler when the number of remaining distinct tasks is less than the cycle's
         length.

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
            instances = -heappop(heap)
            # If a task is pending in the heap, it's going to be actual work time
            work_units += 1
            if instances > 1:
                remaining.append(instances - 1)
            # Check if we're out of tasks. If at any point the heap is empty (no more tasks to extract), we break out
            # of the current cycle.
            if not heap:
                break
        # Idle time is the time that is needed in the cycle because no task is available. It is the remaining cycle
        # length. Idle time should be only added if the priority queue is empty and remaining list is not.
        work_time += work_units if not remaining else cycle
        # Because we transferred all the items from the heap to remaining list, we're transferring them back for the
        # next round of scheduling.
        for instance in remaining:
            heappush(heap, -instance)
    return work_time


def least_interval_v2(tasks, n):
    """ The key is to find how many idles we need, and only the most frequent tasks can create idles.

         Let's first look at how to arrange the tasks. It's not hard to notice that we can do a 'greedy arrangement':
         always arrange the tasks with most frequency first.

         E.g. we have the following tasks : 3 A, 2 B, 1 C, and n=2. According to what we have above, we should first
         arrange A, and then B, and finally C. Imagine there are 'slots' and we need to arrange tasks by placing them
         into these 'slots'. A's should be put into slots 0, 3, 6 since we need to have at least n=2 other tasks between
         two consecutive A's. After A is placed, it looks like this:

                    A ? ? A ? ? A
         where '?' are empty slots.

         Now we can use the same method to arrange B's and C's. The finished schedule should look like this:

                    A B C A B # A
         where '#' is idle.

         Now we have a way to arrange tasks. But the problem only asks for the number of CPU intervals, so we don't need
         to actually arrange them. Instead, we only need to get the total idles needed and the answer to the problem
         becomes:

                    minimum CPU intervals = number of tasks + number of idles

         Same example: 3 A, 2 B, 1 C, n = 2. After arranging A's, we have:
                    A ? ? A ? ? A

         We can see that A separated the slots into (count(A) - 1) = 2 segments, where each segment has length n.
         With the fact that A is the most frequent task, it should need more idles than any other tasks. In this case,
         if we can calculate how many idles we need to arrange A's, we will also get the number of idles needed to
         arrange all the tasks. Calculating this is not hard. We first get the number of segments created by A's
         arrangements:

                    segments = count(A) - 1

         Then we can find the number of empty slots after arranging the A's:

                    empty_slots = segments * n

         We can also get how many tasks we have to put into those slots:

                    remaining_tasks = tasks.length - count(A)

         Now, if we have empty_slots > remaining_tasks it means we don't have enough tasks available to fill all empty
         slots, so we must fill them with idles.

         What if we have more than n tasks with the same most frequency, and we got empty_slots negative?
         Like 3A, 3B, 3C, 3D, 3E, n=2. In this case it seems like we can't put all B C s inside slots since we only
         have n=2.

         Well, n is actually the "minimum" length of each part required for arranging A's. We can always make the length
         of segments bigger. E.g. 3A, 3B, 3C, 3D, 2E, n=2. We can always first arrange A, B, C, D as:

                    A B C D | A B C D | A B C D

         In this case, we have already met the "minimum" length requirement for each segment (n=2).
         empty_slots < 0 means we already got enough tasks to fill in each segment to make arranged tasks valid.

         The problem actually requires us to make the "distance" between two same tasks up to at least n. Thus, if
         empty_slots is negative, it means that we even have remaining tasks to make the "distance" between the same
         tasks larger than n. That is, no idle is needed.

         Thus, we have:

                    idles = max(0, empty_slots - remaining_tasks)

         Almost done. One special case: what if there is more than one task with the same max frequency ? Let's look at
         another example: 3 A, 3 B, 2 C, 1 D, n=3
         Similarly we arrange A's first:

                    A ? ? ? A ? ? ? A

         Now it's time to arrange B's. We find that we have to arrange B's like this:

                    A B ? ? A B ? ? A B

         We need to put every B right after each A. Let's look at this in another way: Think of sequence 'A B' as a
         special task 'X', then we get:

                    X ? ? X ? ? X

         Comparing to what we have after arranging A's:

                    A ? ? ? A ? ? ? A

         The only changes are the length of each segment (from 3 to 2) and available tasks:

                    segment_length = (n + 1) - number of tasks with same max frequency
                    empty_slots = segments * segment_length
                    remaining_tasks = tasks.length - max frequency * number of tasks with same max frequency

    Time complexity: O(n)
    Space complexity: O(1)
    """
    frequency = Counter(tasks)
    max_frequency = max(frequency.values())
    same_max_frequency = 0
    for task, freq in frequency.items():
        same_max_frequency += 1 if freq == max_frequency else 0
    total_tasks = len(tasks)
    segments = max_frequency - 1
    segment_length = n + 1 - same_max_frequency
    empty_slots = segments * segment_length
    remaining_tasks = total_tasks - max_frequency * same_max_frequency
    idles = max(0, empty_slots - remaining_tasks)
    return total_tasks + idles
    # An alternate solution:
    # segments = max_frequency - 1
    # return max(segments * (n + 1) + same_max_frequency, total_tasks)
    # total time= (cycle length) * segments+ number maximum frequency tasks that are left
    # i.e. total time=(n+1) * segments +count_max frequency tasks
    # In scenarios where the total time is less than the number of tasks, the minimum time required would
    # be the number of tasks itself.


class Test(unittest.TestCase):
    data = [(['A', 'A', 'A', 'B', 'B', 'B'], 2, 8)]

    def test_least_interval(self):
        for test_tasks, test_n, result in self.data:
            self.assertEqual(result, least_interval_v1(test_tasks, test_n))
            self.assertEqual(result, least_interval_v2(test_tasks, test_n))


if __name__ == '__main__':
    unittest.main()
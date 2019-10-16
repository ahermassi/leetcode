""" Given a string S, check if the letters can be rearranged so that two characters that are adjacent to each other are
not the same.
If possible, output any possible result.  If not possible, return the empty string. """

from collections import Counter
from heapq import heappush, heappop
import unittest2 as unittest


def reorganize_string_v1(S):
    """ This is similar to 621- Task Scheduler problem, with the cooling interval is equal to 2.
        This is a greedy approach that tries to write the most common letter followed by the second most common letter
        and so on.
        We create a heap of (count, letter). The implementation stores negative counts because Python's heap is min
        heap. We pop the top two elements from the heap (representing different letters with positive remaining count),
        and then write the most frequent one that isn't the same as the most recent one written. After, we push the
        correct counts back onto the heap.
        At the end, we might have one element still on the heap, which must have a count of one. If we do, we'll add
        that to the answer too.
    Time complexity: O(N logA), where N is the length of the string and A the length of alphabet. Calculating the
    letter frequency which takes O(N) time, and building the max heap takes O(A logA) which is actually constant and
    not considered dominant if alphabet size is fixed. Rebuilding the string takes N steps and in each step the max
    heap takes at most O(logA) time to reorganize itself. So overall time complexity is O(N logA)
    Space complexity: O(A), if A is fixed this complexity is O(1)
    """
    counter, heap, res = Counter(S), [], ''
    if any(count > (len(S) + 1) / 2 for c, count in counter.items()):
        return ''  # The task is only impossible if the frequency of a letter exceeds (N+1) / 2
    for k, v in counter.items():  # Using negative values to create a max heap
        heappush(heap, [-v, k])
    while len(heap) >= 2:
        a_instance, a = heappop(heap)
        b_instance, b = heappop(heap)
        res += a + b
        if a_instance != -1:
            heappush(heap, [a_instance + 1, a])
        if b_instance != -1:
            heappush(heap, [b_instance + 1, b])
    return res if not heap else res + heap[0][1]


class Test(unittest.TestCase):
    data = [('aab', 'aba'), ('aaab', '')]

    def test_reorganize_string(self):
        for test_string, result in self.data:
            self.assertEqual(result, reorganize_string_v1(test_string))


if __name__ == '__main__':
    unittest.main()


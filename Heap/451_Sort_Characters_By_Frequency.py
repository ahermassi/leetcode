""" Given a string, sort it in decreasing order based on the frequency of characters. """

from collections import Counter
from heapq import heappush, heappop


def frequency_sort_v1(s):
    """ Use a max heap to store each character along with its frequency in the string. Pop elements from heap to
        construct final result.
    Time complexity: if we assume N is the length of the string, then O(N) to create hash map, O(N logN) in the worst
    case to build the heap (worst case == all characters are different so heap size is N), but since there are only 128
    different possible characters possible, we can argue that O(N logN) becomes O(N) since log(constant) = O(1).
    So overall time complexity is (N)
    Space complexity: O(N) for heap an counter
    """
    counter, heap, res = Counter(s), [], ''
    for key, value in counter.items():
        heappush(heap, (-value, key))
    while heap:
        repeat, chars = heappop(heap)
        res += chars * -repeat
    return res



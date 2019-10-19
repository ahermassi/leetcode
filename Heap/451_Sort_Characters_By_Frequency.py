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


def frequency_sort_v2(s):
    """ This solution is based on counting sort.
        Build a map of characters to the number of times it occurs in the string.
        Create an array where the index of the array represents how many times that character occurred in the string.
        Iterate from the end of the array to the beginning, and at each index, append each character to the return
        string that number of times.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    counter, res = Counter(s), ''
    bucket = [None] * (len(s) + 1)
    for key, value in counter.items():
        if not bucket[value]:
            bucket[value] = [key]
        else:
            bucket[value].append(key)
    for i in reversed(range(len(bucket))):
        if bucket[i]:
            for c in bucket[i]:
                res += c * i
    return res



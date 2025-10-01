""" Given a string, sort it in decreasing order based on the frequency of characters. """

from collections import Counter, defaultdict
from heapq import heappush, heappop


def frequency_sort_v1(s):
    """ Use a max heap to store each character along with its frequency in the string. Pop elements from heap to
        construct the final result.
    Time complexity: O(N + K logK), where N is the length of the string and K the number of unique characters in the
    string, then O(N) to create hash map, O(K logK) for the heap, which is O(N logN) in the worst case (worst case = all
    characters are different so heap size is N), but since there are only 128 different possible characters, we can
    argue that O(N logN) becomes O(N) since log(constant) = O(1). So overall time complexity is (N)
    Space complexity: O(N), for heap and hash map
    """
    counter, heap, res = Counter(s), [], []
    for char, count in counter.items():
        heappush(heap, (-count, char))
    while heap:
        count, char = heappop(heap)
        res.append(char * -count)
    return ''.join(res)


def frequency_sort_v2(s):
    """ This solution is based on bucket sort.

        Notice that because all the characters came out of a string of length n, the maximum frequency for any one
        character is n. This means that once we've determined all the letter frequencies using a hashmap, we can sort
        them in linear time using bucket sort.

            - Build a map of characters to the number of times they occur in the string.

            - Create an array where the index represents how many times that character occurred in the string.

            - While we could simply make the bucket array's size n, it's better to look for the maximum value
              (frequency) in the hashmap. That way, we only use the space we actually need and won't need to iterate
              over empty buckets.

            - Iterate from the end of the array to the beginning, and at each index append each character to the result
              string that number of times.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    counter, res = Counter(s), []
    max_frequency = max(counter.values())
    bucket = [[] for _ in range(max_frequency + 1)]
    for char, count in counter.items():
        bucket[count].append(char)
    for frequency in reversed(range(max_frequency + 1)):
        for char in bucket[frequency]:
            res.append(char * frequency)
    return ''.join(res)


def frequency_sort_v3(s):
    """ Create a hashmap 'counter' of character to character frequency for the input string. Then, iterate over
        'counter' to create a second hashmap 'substrings' where the key is the frequency and the value are the
        substrings of repeated strings with length as the frequency. Finally, look up all potential frequencies in
        decreasing order in 'substrings' and produce the final result.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    counter = Counter(s)
    substrings = defaultdict(list)
    for char, count in counter.items():
        substrings[count].append(char * count)
    max_frequency = max(counter.values())
    res = []
    for i in reversed(range(max_frequency + 1)):
        res.extend(substrings[i])
    return ''.join(res)



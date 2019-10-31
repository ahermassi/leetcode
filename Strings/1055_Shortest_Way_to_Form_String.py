""" From any string, we can form a sub sequence of that string by deleting some number of characters (possibly no
deletions).
Given two strings source and target, return the minimum number of sub sequences of source such that their concatenation
equals target. If the task is impossible, return -1. """

import bisect
from collections import defaultdict
import unittest2 as unittest


def shortest_way_v1(source, target):
    """ When the data needs to be processed in a certain order, think greedy. Here, greedy means exhausting all
        characters in the source before starting a new sub sequence.
        We traverse the target string while matching source string multiple times.
        i: index for target string
        j: index for source string
        We use a set to save all the characters in source, and if there exists a character from target which doesn't
        exist in the set, we exist early and return -1.
    Time complexity: O(N * M), where N is the length of source and M is the length of target
    Space complexity: O(M)
    """
    count, n = 0, len(target)
    chars = set(source)
    for c in target:
        if c not in chars:
            return -1
    i = 0
    while i < n:
        for j, c in enumerate(source):
            if i < n and c == target[i]:
                i += 1
            j += 1
        count += 1
    return count


def shortest_way_v2(source, target):
    """ We traverse the target string while matching source string multiple times.
        i: index for target string
        j: index for source string
        Improving space complexity: at the end of each loop, we want to ensure that i index moves forward instead of
        staying steady. Not moving forward means that the current character in target pointed at by i doesn't exist in
        source string.
    Time complexity: O(N * M), where N is the length of source and M is the length of target
    Space complexity: O(1)
    """
    res, n = 0, len(target)
    i = 0
    while i < n:
        ptr = i
        for j, c in enumerate(source):
            if i < n and c == target[i]:
                i += 1
            j += 1
        if i == ptr:
            return -1
        res += 1
    return res


def shortest_way_v3(source, target):
    """ The idea is to create an inverted index that saves the offsets of where each character occurs in source. The
        index data structure is represented as a hash map, where the key is the character, and the value is the
        (sorted) list of offsets where this character appears. To run the algorithm, for each character in target, use
        the index to get the list of possible offsets for this character. Iterate over target, searching for the next
        index in source of each char. We can use binary search to efficiently search for the next index. If the next
        index in source requires wrapping around to the start of source, increment result.
        count.
        Example with source = 'abcab', target = 'aabbaac'
        The inverted index data structure for this example would be:
            indices = {
                a: [0, 3] # 'a' appears at index 0, 3 in source
                b: [1, 4], # 'b' appears at index 1, 4 in source
                c: [2], # 'c' appears at index 2 in source
            }
        Initialize i = 0 (i represents the smallest valid next index) and res = 1 (number of passes through source).
        Iterate through the target string 'aabbaac'
        a => get the indices of character 'a' which is [0, 3]. Set i to 1.
        a => get the indices of character 'a' which is [0, 3]. Set i to 4.
        b => get the indices of character 'b' which is [1, 4]. Set i to 5.
        b => get the indices of character 'b' which is [1, 4]. Increment res to 2, and Set i to 2.
        a => get the indices of character 'a' which is [0, 3]. Set i to 4.
        a => get the indices of character 'a' which is [0, 3]. Increment res to 3, and Set i to 1.
        c => get the indices of character 'c' which is [2]. Set i to 3.
        We're done iterating through target so return the number of loops (3).
    Time complexity: O(N + M*logN), where N is the length of source and M is the length of target, O(N) to build the
    index, and O(logN) for each query. There are M queries, so the total runtime is O(N + M*logN)
    Space complexity: O(N), which is the space needed to store the index
    """
    indices = defaultdict(list)
    for i, c in enumerate(source):
        indices[c].append(i)
    res = 1
    index = 0  # Next index of source to check
    for c in target:
        if c not in indices:  # Cannot make target if char not in source
            return -1
        char_indices = indices[c]
        # bisect_left(A, x) returns the smallest index j s.t. A[j] >= x. If no such index j exists, it returns len(A)
        j = bisect.bisect_left(char_indices, index)
        if j == len(char_indices):  # This means that current index is past the index of last element in char_indices.
            # In other words, to select this character we need to wrap around to beginning of source.
            res += 1
            index = char_indices[0] + 1  # Next index in source to check
        else:
            index = char_indices[j] + 1  # Next index in source to check
    return res


class Test(unittest.TestCase):
    data = [('abc', 'abcbc', 2), ('abc', 'acdbc', -1), ('xyz', 'xzyxz', 3)]

    def test_shortest_way(self):
        for test_source, test_target, result in self.data:
            self.assertEqual(result, shortest_way_v1(test_source, test_target))
            self.assertEqual(result, shortest_way_v2(test_source, test_target))
            self.assertEqual(result, shortest_way_v3(test_source, test_target))


if __name__ == '__main__':
    unittest.main()

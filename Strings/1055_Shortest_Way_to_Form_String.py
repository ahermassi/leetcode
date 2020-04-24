""" From any string, we can form a sub sequence of that string by deleting some number of characters (possibly no
deletions).
Given two strings source and target, return the minimum number of sub sequences of source such that their concatenation
equals target. If the task is impossible, return -1. """

from bisect import bisect_left
from collections import defaultdict
import unittest2 as unittest


def shortest_way_v1(source, target):
    """ When the data needs to be processed in a certain order, think greedy. Here, greedy means exhausting all
        characters in the source before starting a new sub sequence.
        We traverse the target string while matching source string multiple times.
        i: index for target string
        j: index for source string
        Match characters in source and target by moving indices i and j. Every time we run out of characters in the
        source, we increase the number of sub-sequences and reset the source index (j = 0).
        We use a set to save all the characters in source, and if there exists a character from target which doesn't
        exist in the set, we exist early and return -1.
    Time complexity: O(N * M), where N is the length of source and M is the length of target
    Space complexity: O(M)
    """
    n, res = len(target), 0
    chars = set(source)
    i = 0
    while i < n:
        if target[i] not in chars:
            return -1
        for j, c in enumerate(source):
            if i < n and c == target[i]:
                i += 1
        res += 1
    return res


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
    n, res = len(target), 0
    i = 0
    while i < n:
        ptr = i
        for j, c in enumerate(source):
            if i < n and c == target[i]:
                i += 1
        if i == ptr:  # Unable to move forward in target string, which means the character doesn't exist in source
            return -1
        res += 1
    return res


def shortest_way_v3(source, target):
    """ The idea is to create an inverted index that saves the offsets of where each character occurs in source. The
        index data structure is represented as a hash map, where the key is the character, and the value is the
        (sorted) list of offsets where this character appears. To run the algorithm, for each character in target, use
        the hash map to get the list of possible indices for this character. Then search this list for next index which
        appears after the offset of the previous character. We can use binary search to efficiently search for the next
        index in our map. If the next index in source requires wrapping around to the start of source, increment the
        result count.
        Example with source = 'abcab', target = 'aabbaac'
        The inverted index data structure for this example would be:
            indices = {
                a: [0, 3] # 'a' appears at indices 0, 3 in source
                b: [1, 4], # 'b' appears at indices 1, 4 in source
                c: [2], # 'c' appears at index 2 in source
            }
        Initialize index = 0 (smallest valid next index), res = 0 (number of passes through source).
        Iterate through the target string 'aabbaac':
        a => get the indices of character 'a' which are [0, 3]. Set index to 1.
        a => get the indices of character 'a' which are [0, 3]. Set index to 4.
        b => get the indices of character 'b' which are [1, 4]. Set index to 5.
        b => get the indices of character 'b' which are [1, 4]. Increment res to 1, and set index to 2.
        a => get the indices of character 'a' which are [0, 3]. Set index to 4.
        a => get the indices of character 'a' which are [0, 3]. Increment res to 2, and set index to 1.
        c => get the indices of character 'c' which is [2]. Set index to 3.
        We're done iterating through target so return the number of loops (res + 1 = 3).
    Time complexity: O(N + M * logN), where N is the length of source and M is the length of target, O(N) to build the
    index, and O(logN) for each query. There are M queries, so the total runtime is O(N + M * logN)
    Space complexity: O(N), which is the space needed to store the index
    """
    indices = defaultdict(list)
    for i, c in enumerate(source):
        indices[c].append(i)
    res = 0
    index = 0  # Next index in source to check looking for the current character in target
    for c in target:
        if c not in indices:  # Cannot make target if char not in source
            return -1
        char_indices = indices[c]  # Where in source string does the current target character occur ?
        j = bisect_left(char_indices, index)  # bisect_left(A, x) returns the smallest index j such that A[j] >= x.
        # If no such index j exists, it returns len(A)
        if j == len(char_indices):  # This means that current index is past the index of last element in char_indices.
            # In other words, to match this character in source we need to wrap around to beginning of source.
            res += 1
            index = char_indices[0] + 1  # Next index in source to check looking for the current character in target
        else:
            index = char_indices[j] + 1
    return res + 1


# Following solution is not very intuitive

def shortest_way_v4(source, target):
    """ First, iterate through the source to find the characters that follow the current one. If there are more than
        one following character, consider the least index character.
        For source = 'abba' the table looks like this:
            {3: {'a': 4}, 2: {'a': 4, 'b': 3}, 1: {'a': 4, 'b': 2}, 0: {'a': 1, 'b': 2}}
        Then, iterate through the target characters and
        greedily construct target from source characters.
    Time complexity: O(N + M), where N is the length of source and M is the length of target
    Space complexity: O(N)
    """
    indices, n = {}, len(source)
    for i in reversed(range(n)):
        c = source[i]
        indices[i] = {} if i + 1 not in indices else indices[i + 1].copy()
        indices[i][c] = i + 1
    res = index = 0
    for c in target:
        if c not in indices[0]:  # indices[0] contains all characters in the source
            return -1
        if index == n or c not in indices[index]:  # If 'index' points to the last character of the source or the
            # current character does not exist in the possible set of characters indicated by 'index', this means a new
            # sub sequence has started
            index = 0
            res += 1
        index = indices[index][c]  # Update the index
    return res + 1  # After the last increment (two lines above), at least one valid character has been observed


class Test(unittest.TestCase):
    data = [('abc', 'abcbc', 2), ('abc', 'acdbc', -1), ('xyz', 'xzyxz', 3)]

    def test_shortest_way(self):
        for test_source, test_target, result in self.data:
            self.assertEqual(result, shortest_way_v1(test_source, test_target))
            self.assertEqual(result, shortest_way_v2(test_source, test_target))
            self.assertEqual(result, shortest_way_v3(test_source, test_target))
            self.assertEqual(result, shortest_way_v4(test_source, test_target))


if __name__ == '__main__':
    unittest.main()

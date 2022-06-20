""" A string S of lowercase letters is given. We want to partition this string into as many parts as possible so that
each letter appears in at most one part, and return a list of integers representing the size of these parts. """

from collections import defaultdict
import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=B7m8UmZE-vw


def partition_labels_v1(s):
    """ Since each character can appear only in one partition, we cannot form a partition that ends before the index of
         the last occurrence of one of the characters in the partition.

         Traverse the string and record the last index of each character and use it to denote the start of the next
         partition. Reset the left pointer at the start of each new partition. Store the window size as the result for
         each section.

        Consider the first label, say it's 'a'. The first partition must include it, and also the last occurrence of
        'a'. However, between those two occurrences of 'a', there could be other labels that make the minimum size of
        this partition bigger. For example, in 'abccaddbeffe', the minimum first partition is 'abccaddb'. This gives us
        the idea for the algorithm: For each letter encountered, process the last occurrence of that letter, extending
        the current partition [left, right] appropriately.

        We need a hash map last_occurrence[char] -> index of s where char occurs last. Then, let 'partition_start' and
        'partition_end' be the start and end of the current partition. If we are at a character c whose last
        occurrence falls at an index after 'partition_end', we'll extend the partition:
        partition_end = last_occurrence[c]. If we are at the end of the partition (i == partition_end), then we append a
        partition size to our answer, and set the start of our new partition to (i + 1).

        Imagine a bus moving forward, and imagine each character as a person yelling "I need to go that far!".
        If a newcomer yelled a farther position, we extend our expected ending position to that position. Eventually,
        if we reached a position that satisfied everybody in the bus at the moment, we partition and clear the bus.

    Time complexity: O(N), where N is the length of s
    Space complexity: O(1), as the hash map can't have more than 26 entries (alphabet size)
    """
    last_occurrence, res = {c: i for i, c in enumerate(s)}, []
    partition_start = partition_end = 0
    for i, c in enumerate(s):
        # This is the right end of the smallest partition we're looking for. This index guarantees that all the
        # previous characters don't occur outside the window.
        partition_end = max(partition_end, last_occurrence[c])
        if i == partition_end:  # When we hit the right end, store the partition size and start over
            res.append(partition_end - partition_start + 1)
            partition_start = i + 1  # Next partition starts just after the previous one
    return res


def partition_labels_v2(s):
    """ We can treat this problem essentially as an interval merging problem. This is similar to 56- Merge Intervals.

         Basically, we can take an indices range for all the characters in the string and save it in a map. This yields
         a list of intervals that is already sorted by first element (since we process the characters of the string fom
         left to right). Finally, we build the result by merging the intervals and calculating the range length of each
         merged interval.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    indices = defaultdict(list)
    for i, c in enumerate(s):
        # Even though we're collecting all the occurrences of each character, we're only interested in the first and
        # last occurrences
        indices[c].append(i)
    intervals = list(indices.values())
    merged = []
    for interval in intervals:
        start, end = interval[0], interval[-1]
        if not merged or start > merged[-1][-1]:
            merged.append([start, end])  # Start a new partition
        else:
            merged[-1][-1] = max(merged[-1][-1], end)  # Extend the current partition
    return [interval[-1] - interval[0] + 1 for interval in merged]


class Test(unittest.TestCase):
    data = [('ababcbacadefegdehijhklij', [9, 7, 8])]

    def test_partition_labels(self):
        for test_string, result in self.data:
            self.assertEqual(result, partition_labels_v1(test_string))
            self.assertEqual(result, partition_labels_v2(test_string))


if __name__ == '__main__':
    unittest.main()
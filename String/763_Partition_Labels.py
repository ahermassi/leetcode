""" A string S of lowercase letters is given. We want to partition this string into as many parts as possible so that
each letter appears in at most one part, and return a list of integers representing the size of these parts. """

from collections import defaultdict
import unittest2 as unittest


# Video explanation: https://youtu.be/B7m8UmZE-vw
def partition_labels_v1(s):
    """ Since each character can appear in only one partition, any single partition can't end before the maximum of last
         occurrence indices of all the characters in that partition.

         Traverse the string and record the last index of each character and use it to denote the start of the next
         partition. Reset the left pointer at the start of each new partition. Store the window size as the result for
         each section.

         Consider the first character, say 'a'. The first partition must include it, bust must also include the last
         occurrence of 'a'. However, between those two occurrences of 'a', there are other characters that could extend
         this partition. This gives us the idea for the algorithm:

                    For each character along the way, find the last occurrence of that character and extend the current
                    partition [start, end] respectively.

         We need a hashmap {last_occurrence[char] -> index of s where char occurs last}. Then, let 'partition_start' and
         'partition_end' be the start and end of the current partition.

            - If we are at a character c whose last occurrence falls at an index after 'partition_end', we extend the
               current partition: partition_end = last_occurrence[c].

            - If we are at the end of the partition (i == partition_end), then we record the partition size and set the
               start of the new partition to i+1.

         Imagine a bus moving forward, and imagine each character as a person yelling "I need to go that far!".
         If a newcomer yelled a farther destination, we extend the expected ending destination to that location.
         Eventually, if we reached a location that satisfied everybody in the bus at the moment, we partition and clear
         the bus.

    Time complexity: O(N), where N is the length of s
    Space complexity: O(1), as the hashmap can't have more than 26 entries (alphabet size)
    """
    last_occurrence = {c: i for i, c in enumerate(s)}
    partition_start = partition_end = 0
    res = []
    for i, c in enumerate(s):
        # This is the right end of the smallest partition we're looking for. This index guarantees that all the
        # previous characters don't fall outside the window.
        partition_end = max(partition_end, last_occurrence[c])
        if i == partition_end:
            # When we hit the right end, store the partition size and start over
            res.append(partition_end - partition_start + 1)
            partition_start = i + 1  # Next partition starts just after the current one
    return res


def partition_labels_v2(s):
    """ We can model this problem as an interval merging. This is similar to 56- Merge Intervals.

         Basically, we can create a range of indices for all the characters in the string. This yields a list of
         intervals that is already sorted by the first element of each interval (since we process the characters of the
         string fom left to right). We then build the result by merging the intervals and calculating the range size of
         each merged interval.

         Alternatively, we can keep track of the start and end positions of "virtual" intervals.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    indices = defaultdict(list)
    for i, c in enumerate(s):
        # Even though we're collecting all the occurrences of each character, we're only interested in the first and
        # last occurrences
        indices[c].append(i)
    ranges = [[values[0], values[-1]] for values in indices.values()]
    merged = []
    for start, end in ranges:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])  # Start a new partition
        else:
            merged[-1][1] = max(merged[-1][1], end)  # Extend the current partition
    return [rng[-1] - rng[0] + 1 for rng in merged]
    # Alternatively:
    # res = []
    # start, end = ranges[0]
    # for a, b in ranges:
    #     if a > end:
    #         res.append(end - start + 1)
    #         start = a
    #     end = max(end, b)
    # res.append(end - start + 1)
    # return res


class Test(unittest.TestCase):
    data = [('ababcbacadefegdehijhklij', [9, 7, 8])]

    def test_partition_labels(self):
        for test_string, result in self.data:
            self.assertEqual(result, partition_labels_v1(test_string))
            self.assertEqual(result, partition_labels_v2(test_string))


if __name__ == '__main__':
    unittest.main()
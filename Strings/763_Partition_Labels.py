""" A string S of lowercase letters is given. We want to partition this string into as many parts as possible so that
each letter appears in at most one part, and return a list of integers representing the size of these parts. """

from collections import defaultdict
import unittest2 as unittest


def partition_labels_v1(S):
    """ Traverse the string and record the last index of each char and use it to denote the start of the next section.
        Reset the left pointer at the start of each new section. Store the window size as the result for each section.
        Consider the first label, say it's 'a'. The first partition must include it, and also the last occurrence of
        'a'. However, between those two occurrences of 'a', there could be other labels that make the minimum size of
        this partition bigger. For example, in 'abccaddbeffe', the minimum first partition is 'abccaddb'. This gives us
        the idea for the algorithm: For each letter encountered, process the last occurrence of that letter, extending
        the current partition [left, right] appropriately.
        We need a hash map last_index[char] -> index of S where char occurs last. Then, let 'left' and 'right' be the
        start and end of the current partition. If we are at a character c that occurs last at some index after 'right',
        we'll extend the partition right = last_index[c]. If we are at the end of the partition (i == right), then
        we'll append a partition size to our answer, and set the start of our new partition to (i + 1).
    Time complexity: O(N), where N is the length of S
    Space complexity: O(1), as the hash map can never have more than 26 entries (alphabet size)
    """
    last_index, res = {c: i for i, c in enumerate(S)}, []
    left = right = 0
    for i, c in enumerate(S):
        right = max(right, last_index[c])  # This is the right end of the smallest partition we're looking for. This
        # index guarantees that all the previous characters don't occur outside the window
        if i == right:  # When we hit the right end, store the partition length and start over
            res.append(right - left + 1)
            left = i + 1  # Next partition starts just after the previous one
    return res


def partition_labels_v2(S):
    """ We can treat this problem essentially as an interval merging problem. This is similar to 56- Merge Intervals.
        Basically, we can take a range for all the characters in the string and save it in a map. Then we convert
        the map values to a sorted list. Finally, we build the result by merging the intervals and calculating the
        range length of each merged interval.
    Time complexity: O(N logN), the complexity of sorting
    Space complexity: O(N)
    """
    indices = defaultdict(list)
    for i, c in enumerate(S):
        indices[c].append(i)
    intervals = sorted(indices.values())
    merged = []
    for interval in intervals:
        if not merged or merged[-1][-1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][-1] = max(merged[-1][-1], interval[-1])
    return [i[-1] - i[0] + 1 for i in merged]


class Test(unittest.TestCase):
    data = [('ababcbacadefegdehijhklij', [9, 7, 8])]

    def test_partition_labels(self):
        for test_string, result in self.data:
            self.assertEqual(result, partition_labels_v1(test_string))
            self.assertEqual(result, partition_labels_v2(test_string))


if __name__ == '__main__':
    unittest.main()
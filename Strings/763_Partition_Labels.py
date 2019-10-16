""" A string S of lowercase letters is given. We want to partition this string into as many parts as possible so that
each letter appears in at most one part, and return a list of integers representing the size of these parts. """

import unittest2 as unittest


def partition_labels_v1(S):
    """ Traverse the string and record the last index of each char and use it to denote the start of the next section.
        Reset the left pointer at the start of each new section. Store the difference of right and left pointers + 1
        as in the result for each section.
    Time complexity: O(N), where N is the length of S
    Space complexity: O(1) as the hash map can never have more than 26 entries (alphabet size)
    """
    last_index, res = {c: i for i, c in enumerate(S)}, []
    left = right = 0
    for i, c in enumerate(S):
        right = max(right, last_index[c])  # This is the right end of smallest partition we're looking for. This
        # index guarantees that all the previous characters don't occur past the index
        if i == right:  # When we hit the right end, store the partition length and start over
            res.append(right - left + 1)
            left = right + 1  # Next partition starts just after previous one
    return res


class Test(unittest.TestCase):
    data = [('ababcbacadefegdehijhklij', [9, 7, 8])]

    def test_partition_labels(self):
        for test_string, result in self.data:
            self.assertEqual(result, partition_labels_v1(test_string))


if __name__ == '__main__':
    unittest.main()
""" Given two strings s and t, return true if s is a subsequence of t, or false otherwise.

A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the
characters without disturbing the relative positions of the remaining characters. (i.e., "ace" is a subsequence of
"abcde" while "aec" is not). """

from bisect import bisect_left
from collections import defaultdict
import unittest2 as unittest


# Video explanation: https://youtu.be/99RVfqklbCE
def is_subsequence_v1(s, t):
    """ We iterate through the source and target strings, respectively with a pointer. Each pointer marks a position
         that we progress on the matching of the characters.

         We designate two pointers for iteration, with j pointer referring to the source string and i to the target
         string. We move the pointers accordingly on the following two cases:

            - If source[j] == target[i]: we found a match. Hence, we move both pointers one step forward.
            - If source[j] != target[i]: no match is found. We then move only i pointer on the target string.

        The iteration would terminate when either of the pointers exceeds its boundary.

        At the end of the iteration, the result solely depends on the fact that whether we have consumed all the
        characters in the source string. If so, we have found a suitable match for each character in the source string.
        Therefore, the source string is a subsequence of the target string.

    Time complexity: O(M), where M is the length of the target string. At each iteration, we would consume one character
    from the target string and optionally one character from the source string. Iterations end when either of the
    strings becomes empty. In the worst case, we would have to scan the entire target string.
    Space complexity: O(1), the counter can hold at most 26 characters (or 128 characters)
    """
    n, m = len(t), len(s)
    i = j = 0
    while i < n and j < m:
        if t[i] == s[j]:
            j += 1
        i += 1
    return j == m


def is_subsequence_v2(s, t):
    """ Let us now look at the follow-up question raised in the problem description, which we cite as follows:

                    If there are lots of incoming S, say S_, S_2, ..., and you want to check one by one to see if T has
                    its subsequence. In this scenario, how would you change your code?

        In the above scenario, we would expect several incoming source strings, but a constant target string. We are
        asked to match each of the source strings against the target string.

        If we apply the previous algorithm, for each match, the overall time complexity would be O(M). In other words,
        regardless of the source strings, in the worst case, we have to scan the target string repeatedly, even though
        the target string remains the same.

        Now with the bottleneck identified, we could ask ourselves if we could do something about it.

        The reason we scan the target string is to look for the next character that matches a given character in the
        source string. In essence, this is a lookup operation in the array data structure.

        To speed up the lookup operation, the hashmap could come in handy, since it has a O(1) time complexity for its
        lookup operation.

        Indeed, we could build a hashmap out of the target string, with each unique character as key and the indices of
        its appearance as value. Moreover, we should pre-compute this hashmap once and then reuse it for all the
        following matches.

        With this hashmap, rather than scanning through the entire target string, we could instantly retrieve all the
        relevant positions in the target string to look at, given a character from the source string.

        Essentially, the algorithm with hashmap remains rather similar to the previous approach, i.e. we still need to
        iterate through the source string to find the matches, and more importantly, we still do the match in the greedy
        manner.

            - First, build a hashmap out of the target string. Each key is a unique character in the target string, and
               its corresponding value would be a list of indices where the character appears in the target string.

            - We then iterate through the source string. This time, rather than keeping two pointers, we need only one
               pointer on the target string. The pointer marks the progress on the target string.
               The pointer on the target string should move monotonically, i.e. in no case, we would move the pointer to
               an earlier position.

            - We use the pointer to check if an index is suitable or not. For instance, for the character a whose
               corresponding indices are [0, 3], we need to pick an index out of all the appearances as a match.
               Suppose at a certain moment, the pointer is located at index 1. Then, the suitable greedy match would be
               the index 3, which is the first index that is larger than the current position of the target pointer.

        Given a list of indices for a matched character, in order to find the suitable index, we could simply do a
        linear search. Since the list of indices is sorted, we could also apply binary search on the list to locate the
        desired index faster.

        !!! IMPORTANT !!!
        bisect_left gives the index to which an element is to be inserted as to maintain the sorted order of the array.
        For example, a = [1,3,5,7,9] then bisect_left(a, 6) gives 3 as the output. However, it becomes a little tricky
        when the element that is being inserted is already present in the array. In such a case the element is inserted
        in the leftmost index possible. For instance a = [1,3,5,7,9] then bisect_left(a, 7) gives 3 as the output,
        meaning the new 7 is inserted to the right of the already existing 7.
        Coming to how it is used in this algorithm, t_pointer stores the index (of the target string) where we found the
        previous character match. Hence, for the match that we are currently considering, if we can insert t_pointer in
        the sorted list, we can say that there's a matching alphabet.

    Time complexity: O(M + N logM), where N is the length of each source string and M is the length of the target
    string. First, we build a hashmap out of the target string (only once), which would take O(M) time complexity.
    Then, we scan through the source string, and look up the corresponding indices in the hashmap. The lookup operation
    in hashmap is constant. However, to find the suitable index would take O(N logM) with the binary search.
    Space complexity: O(M), we build a hashmap that consists of the indices for each character in the target string.
    Hence, the size of values (indices) in hashmap would be M. In the worst case, we might have as many keys as the
    values, i.e. each character corresponds to a unique index.
    """
    char_indices = defaultdict(list)
    for i, c in enumerate(t):
        char_indices[c].append(i)
    t_pointer = 0
    for i, c in enumerate(s):
        if c not in char_indices:
            return False
        indices = char_indices[c]
        index = bisect_left(indices, t_pointer)
        if index >= len(indices):
            return False
        t_pointer = indices[index] + 1
    return True


class Test(unittest.TestCase):
    data = [('abc', 'ahbgdc', True), ('axc', 'ahbgdc', False)]

    def test_can_construct(self):
        for s, t, result in self.data:
            self.assertEqual(result, is_subsequence_v1(s, t))
            self.assertEqual(result, is_subsequence_v2(s, t))


if __name__ == '__main__':
    unittest.main()
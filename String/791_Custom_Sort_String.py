""" S and T are strings composed of lowercase letters. In S, no letter occurs more than once.
S was sorted in some custom order previously. We want to permute the characters of T so that they match the order that
S was sorted. More specifically, if x occurs before y in S, then x should occur before y in the returned string.
Return any permutation of T (as a string) that satisfies this property. """

import unittest2 as unittest


def custom_sort_string_v1(S, T):
    """ Good old bucket sort. We construct a character to index hash map for string S. Then, as we iterate over the
        characters of string T, we place each one in its corresponding bucket based on its ordering in the indices map.
        We end up with substrings of T according to the order of string S. The result is their concatenation.
        Note that we create a 'bucket' array of length (length of S + 1) to avoid having empty buckets when S has less
        than 26 characters.
    Time complexity: O(N + M), where N is the length of S and M is the length of T
    Space complexity: O(M), we count at most 26 different lowercase letters in the hash map, but the buckets array has
    the same length as T
    """
    indices, n = {c: i for i, c in enumerate(S)}, len(S)
    bucket = [[] for _ in range(n + 1)]
    for c in T:
        if c not in S:  # Characters that don't occur in S can be placed anywhere, so we add them to the last bucket
            bucket[-1].append(c)
        else:
            bucket[indices[c]].append(c)
    res = [''.join(chars) for chars in bucket]
    return ''.join(res)

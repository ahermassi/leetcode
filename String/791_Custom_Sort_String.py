""" S and T are strings composed of lowercase letters. In S, no letter occurs more than once.
S was sorted in some custom order previously. We want to permute the characters of T so that they match the order that
S was sorted. More specifically, if x occurs before y in S, then x should occur before y in the returned string.
Return any permutation of T (as a string) that satisfies this property. """

from collections import Counter


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


def custom_sort_string_v2(S, T):
    """ Let's first write to our answer the elements of T that occur in S, in order of S. After, we'll write any
        elements of T we didn't write. This obviously keeps all the ordering relationships we wanted.
        In the second write, the order doesn't matter because those elements aren't in S, so there are no ordering
        relationships these elements have to satisfy.
        The trick is to count the frequency of characters of T. After we have some counter[char] = (the number of
        occurrences of char in T), we can write these elements in the order we want.
        The order is S + (characters not in S in any order).
    Time complexity: O(N + M)
    Space complexity: O(M)
    """
    counter, res = Counter(T), []
    for c in S:  # Write all T characters that occur in S, in the order of S
        res.append(c * counter[c])
        del counter[c]  # Denotes that we do not need to write 'c' to our answer anymore
    for c in counter:  # Write all remaining characters that don't occur in S and are left in the hash map
        res.append(c * counter[c])
    return ''.join(res)

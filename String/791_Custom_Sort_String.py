""" order and str are strings composed of lowercase letters. In order, no letter occurs more than once.
order was sorted in some custom order previously. We want to permute the characters of str so that they match the order
that order was sorted. More specifically, if x occurs before y in order, then x should occur before y in the returned
string.
Return any permutation of str (as a string) that satisfies this property. """

from collections import Counter


def custom_sort_string_v1(order, str):
    """ Good old bucket sort. We construct a character to index hash map for string 'order'. Then, as we iterate over
        the characters of string 'str', we place each one in its corresponding bucket based on its ordering in the
        indices map. We end up with substrings of 'str' according to the order of string 'order'. The result is their
        concatenation.
        Note that we create a 'bucket' array of length (length of order + 1) to avoid having empty buckets when 'order'
        has less than 26 characters.
    Time complexity: O(N + M), where N is the length of order and M is the length of str
    Space complexity: O(M), we count at most 26 different lowercase letters in the hash map, but the buckets array has
    the same length as order
    """
    indices, n = {c: i for i, c in enumerate(order)}, len(order)
    bucket = [[] for _ in range(n + 1)]
    for c in str:
        if c not in indices:  # Characters that don't occur in 'order' can be placed anywhere, so we add them to the
            # last bucket
            bucket[-1].append(c)
        else:
            bucket[indices[c]].append(c)
    res = [''.join(chars) for chars in bucket]
    return ''.join(res)


def custom_sort_string_v2(order, str):
    """ Let's first write to our answer the elements of 'str' that occur in 'order', in order of 'order'. After, we'll
        write any elements of 'str' we didn't write. This obviously keeps all the ordering relationships we wanted.
        In the second write, the order doesn't matter because those elements aren't in order, so there are no ordering
        relationships these elements have to satisfy.
        The trick is to count the frequency of characters of 'str'. After we have some counter[char] = (the number of
        occurrences of char in str), we can write these elements in the order we want.
        The order is 'order' + (characters not in 'order' in any order).
    Time complexity: O(N + M)
    Space complexity: O(M)
    """
    counter, res = Counter(str), []
    for c in order:  # Write all str characters that occur in order, in the order of 'order'
        res.append(c * counter[c])
        del counter[c]  # Denotes that we do not need to write 'c' to our answer anymore
    for c in counter:  # Write all REMAINING characters that don't occur in order and are left in the hash map
        res.append(c * counter[c])
    return ''.join(res)

""" Given a string, we can 'shift' each of its letter to its successive letter, for example: 'abc' -> 'bcd'. We can
keep 'shifting' which forms the sequence:
'abc' -> 'bcd' -> ... -> 'xyz'
Given a list of strings which contains only lowercase alphabets, group all strings that belong to the same shifting
sequence. """

from collections import defaultdict


def group_strings(strings):
    """ The key to this problem is how to identify strings that are in the same shifting sequence. Basically we need
        to form some sort of key for each word to group them. This is similar to 49- Group Anagrams.
        Consider 'acf' and 'pru'. Now notice the difference between each two consecutive characters.
        acf = 0->2->3, pru = 0->2->3. So these two form the same group. So in this case, we can simply use integers
        ASCII difference to form a key. Therefore, the key can be represented as a tuple of the "gaps" between adjacent
        characters. Characters map to integers (e.g. ord('a') = 97). For example, 'abc' maps to (1,1) because
        ord('b') - ord('a') = 1 and ord('c') - ord('b') = 1
        Then we build a hash map using the above shifting feature string as key and strings that share the shifting
        feature as value. We store all the strings that share the same shifting feature in a list.
        A final note, since the problem statement has given that 'az' and 'ba' belong to the same shifting sequence,
        if s[i] - s[i-1] is negative, we need to add 26 to it to make it positive and give the correct result.
    Time complexity: O(ab), where a is the total number of strings and b is the length of the longest string
    Space complexity: O(a), as the most space we would use is the space required for the strings and the keys of our map
    """
    groups = defaultdict(list)
    for string in strings:
        n = len(string)
        gaps = ()
        for i in range(1, n):
            gap = (ord(string[i]) - ord(string[i - 1])) % 26
            gaps += (gap, )  # This is how to append to a tuple
        groups[gaps].append(string)  # We can a use a tuple of integers as map key unlike the list of integers
    return groups.values()


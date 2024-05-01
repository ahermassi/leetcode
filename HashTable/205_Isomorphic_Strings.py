""" Given two strings s and t, determine if they are isomorphic.
Two strings are isomorphic if the characters in s can be replaced to get t.
All occurrences of a character must be replaced with another character while preserving the order of characters.
No two characters may map to the same character but a character may map to itself. """

import unittest2 as unittest


# Video explanation: https://youtu.be/7yF-U1hLEqQ
def is_isomorphic_v1(s, t):
    """ Matching the order is easy. Since we iterate over the two strings and do some sort of comparison from left to
         right, the task of ensuring that the characters order is the same in both strings will take care of itself.

         We process the two strings from left to right. At each step, we consider two characters at a time from each of
         the two strings and compare them. We need two dictionaries instead of one since we need one-to-one mapping from
         string s to string t and vice versa.
         There are 3 cases we need to handle here:

            1- The characters don't have mappings, so we create their mappings.

            2- The characters already have mappings, then we're good to go.

            3- A mapping already exists for one of the characters, but it doesn't map to the other character. In this
                 case, we can conclude that the given strings are not isomorphic.

        For example, s= 'egg' and t = 'add', we need to create the mappings {'e' -> 'a', 'g' -> 'd'} and
        {'a' -> 'e', 'd' -> 'g'}. When we encounter a character for the first time, we map it to the corresponding
        character at the same index in the other string. If we encounter that character later again, then we check its
        current mapping and compare it to the current character of the other string. If they don't match, then the
        strings can't be isomorphic.

    Time complexity: O(N), where N is the length of s (and t)
    Space complexity: O(1), the hashmaps can't store more than the size of the alphabet characters
    """
    n = len(s)
    s_mapping, t_mapping = {}, {}
    for i in range(n):
        s_char, t_char = s[i], t[i]
        if (s_char in s_mapping and s_mapping[s_char] != t_char) or \
                (t_char in t_mapping and t_mapping[t_char] != s_char):
            return False
        s_mapping[s_char] = t_char
        t_mapping[t_char] = s_char
    return True


def is_isomorphic_v2(s, t):
    """ This approach is based on the idea that the two given strings, if isomorphic, will in some share a similar
         "structure" or "fingerprint". If we have two isomorphic strings, we can replace the characters in the first
         string with the corresponding mapped characters to get the second string. The idea we explore here is the
         following:

                    Is there any string transformation we can apply to both strings such that to check for
                    isomorphism, we simply check if their transformed versions are exactly the same?

        For each character in a given string, we replace it with the index of that character's first occurrence in the
        string. For a string like 'paper', the transformed string will be '01034'. The character 'p' occurs first at
        index 0, so we replace all occurrences of 'p' with '0'. Similar modifications are made for the other characters.

        Now let's look at 'title'. The transformed string would be '01034' which is the same as that of 'paper'.
        This confirms the isomorphic nature of both strings.

        However, we should be mindful of transformations that use both one and two-digit numbers. Under these
        circumstances, the transformed strings can be misinterpreted. For example, 'stenographic's and 'logarithmsxox'
        both map to '123456789110', yet they are not isomorphic. Therefore, to avoid confusion, we add a delimiter to
        help differentiate the transformed digits.

        Note that this solution is more scalable if we want to form groups of isomorphic strings given a list of
        strings. The transformation would serve as key of the hashmap.

    Time complexity: O(N), where N is the length of s (and t)
    Space complexity: O(1), the hashmaps can't store more than the size of the alphabet characters
    """

    def transform(string):
        indices, values = {}, []
        for i, c in enumerate(string):
            if c not in indices:
                indices[c] = i
            values.append(indices[c])
        return ','.join(map(str, values))

    return transform(s) == transform(t)


class Test(unittest.TestCase):
    data = [
        ('egg', 'add', True),
        ('foo', 'bar', False),
        ('paper', 'title', True)
        ]

    def test_is_isomorphic(self):
        for test_string1, test_string2, result in self.data:
            self.assertEqual(result, is_isomorphic_v1(test_string1, test_string2))
            self.assertEqual(result, is_isomorphic_v2(test_string1, test_string2))


if __name__ == '__main__':
    unittest.main()
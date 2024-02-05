""" Given two strings s and t, determine if they are isomorphic.
Two strings are isomorphic if the characters in s can be replaced to get t.
All occurrences of a character must be replaced with another character while preserving the order of characters.
No two characters may map to the same character but a character may map to itself. """

import unittest2 as unittest


# Video explanation: https://youtu.be/7yF-U1hLEqQ
def is_isomorphic(s, t):
    """ Matching the order will be easy. Since we will iterate over the two strings and do some sort of comparison from
         left to right, the task of ensuring that the character order is the same in both strings will take care of
         itself.

         We will process both of the strings from left to right. At each step, we take one character at a time from the
         two strings and compare them. There are three cases we need to handle here:

            1- If the characters don't have a mapping, we add one in the dictionary and move on.

            2- The characters already have a mapping in the dictionary. If that is the case, then we're good to go.

            3- The final case is when a mapping already exists for one of the characters, but it doesn't map to the
                 other character. In this case, we can safely conclude that the given strings are not isomorphic,
                 and we can return.

        The above three cases only care about one-way-mapping i.e. mapping characters from the first string to the
        second one only. Don't we need the mapping from the other side as well?

        We will need two dictionaries instead of one since we need one-to-one mapping from the string s to string t and
        vice versa.

        For example, s= 'egg' and t = 'add', we need to construct the mapping 'e' -> 'a', 'a' -> 'e', 'g' -> 'd', and
        'd' -> 'g'. When we encounter a character for the first time, we map it with the corresponding current character
        of the other string. If we encounter that character later, then we go and fetch the previous mapping and compare
        it to the current character of the other string. If they match, then fine. Otherwise, the strings can't be
        isomorphic.

    Time complexity: O(N), where N is the length of s and t
    Space complexity: O(1), the hash maps can't store more than the size of the alphabet characters
    """
    s_mapping, t_mapping = {}, {}
    n = len(s)
    for i in range(n):
        s_char, t_char = s[i], t[i]
        if s_char not in s_mapping and t_char not in t_mapping:
            s_mapping[s_char] = t_char
            t_mapping[t_char] = s_char
        elif (s_char in s_mapping and s_mapping[s_char] != t_char) or \
                (t_char in t_mapping and t_mapping[t_char] != s_char):
            return False
    return True


class Test(unittest.TestCase):
    data = [
        ('egg', 'add', True),
        ('foo', 'bar', False),
        ('paper', 'title', True)
        ]

    def test_is_isomorphic(self):
        for test_string1, test_string2, result in self.data:
            self.assertEqual(result, is_isomorphic(test_string1, test_string2))


if __name__ == '__main__':
    unittest.main()
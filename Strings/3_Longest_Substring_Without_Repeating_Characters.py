""" Given a string, find the length of the longest substring without repeating characters. """

import unittest2 as unittest


def length_of_longest_substring(s):
    """ Define a mapping of the characters to its index. Then we can skip the characters immediately when we found a
        repeated character.
    Time complexity : O(N)
    Space complexity: O(N)
    """
    d, ans, start = {}, 0, 0
    for i, c in enumerate(s):
        if c in d:
            start = max(start, d[c] + 1)  # After we do start = usedChar[s[i]] + 1, there could be characters whose
            # last seen indexes stored in usedChar are from before start. We don't want to consider those characters
            # as repeats because we are only considering the substring from start to i each iteration.
            # Here's an example: "tmmzuxta"
            # Two characters are repeated: t and m. Because of the repeated m, your start will be 2. Now, when you're
            # at the second occurrence of t, this check ensures that you don't go into the if just because you've
            # seen it before. In this case, you have seen it before BUT you saw it before you started the count.
        ans = max(ans, i - start + 1)
        d[c] = i
    return ans


class Test(unittest.TestCase):
    data = [('abcabcbb', 3), ('bbbbb', 1), ('pwwkew', 3)]

    def test_length_of_longest_substring(self):
        for test_string, result in self.data:
            self.assertEqual(result, length_of_longest_substring(test_string))


if __name__ == '__main__':
    unittest.main()
""" Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string "". """

import unittest2 as unittest


def longest_common_prefix_v1(strings):
    """ Look at each character sequentially while all strings share that character respectively.
    Time complexity: O(N)
    Space complexity: O(N) because the length of prefix list linearly varies with N
    """
    i = 0
    longest_prefix = ''
    prefix = [string[i:i+1] for string in strings]  # Using [i:i+1] to circumvent index out of bound error
    while len(set(prefix)) == 1 and '' not in prefix:  # While all strings start with same character
        longest_prefix += prefix[0]
        i += 1
        prefix = [string[i:i + 1] for string in strings]
    return longest_prefix


class Test(unittest.TestCase):
    data = [(['flower', 'flow', 'flight'], 'fl'),
            (['dog', 'racecar', 'car'], '')
            ]

    def test_longest_common_prefix(self):
        for test_array, result in self.data:
            self.assertEqual(result, longest_common_prefix_v1(test_array))


if __name__ == '__main__':
    unittest.main()

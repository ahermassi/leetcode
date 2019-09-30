""" Compare two version numbers version1 and version2.
If version1 > version2 return 1; if version1 < version2 return -1;otherwise return 0.
You may assume that the version strings are non-empty and contain only digits and the . character. """
from itertools import zip_longest

import unittest2 as unittest


def compare_version_v1(version1, version2):
    """ Pretty straightforward. Mapping int() to individual strings gets rid of leading zeroes ('01' -> 1).
    Time complexity: O(N + M) where N is the length of version1 and M is the length of version2
    Space complexity: O(max(N, M))
    """
    version1 = list(map(int, version1.split('.')))
    version2 = list(map(int, version2.split('.')))
    d = len(version2) - len(version1)
    version1.extend([0] * d)
    version2.extend([0] * -d)  # Watch that cool trick over there ! A negative multiplication factor has no effect
    for i in range(len(version1)):
        if version1[i] < version2[i]:
            return -1
        if version1[i] > version2[i]:
            return 1
    return 0


def compare_version_v2(version1, version2):
    """ Same as above, but using zip_longest.
    Time complexity: O(N + M)
    Space complexity: O(max(N, M))
    """
    version1 = map(int, version1.split('.'))
    version2 = map(int, version2.split('.'))
    for v1, v2 in zip_longest(version1, version2, fillvalue=0):
        if v1 < v2:
            return -1
        if v1 > v2:
            return 1
    return 0


class Test(unittest.TestCase):
    data = [
        ('0.1', '1.1', -1), ('1.0.1', '1', 1), ('7.5.2.4', '7.5.3', -1), ('1.0', '1.0.0', 0)
    ]

    def test_compare_version(self):
        for test_version1, test_version2, result in self.data:
            self.assertEqual(result, compare_version_v1(test_version1, test_version2))
            self.assertEqual(result, compare_version_v2(test_version1, test_version2))


if __name__ == '__main__':
    unittest.main()

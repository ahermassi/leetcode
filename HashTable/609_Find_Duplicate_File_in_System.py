""" Read description on Leetcode """

from collections import defaultdict

import unittest2 as unittest


def find_duplicate(paths):
    """" After parsing, we have some path and content. Let's store a map M[content] = [path1, path2, ...]. At the
        end, we want all values in this map with length > 1.
    Time complexity: O(N * M) where N is the length of paths list and M is the length of longest path
    Space complexity: O(N * M) for hash map and returned result
    """
    d = defaultdict(list)
    for path in paths:
        data = path.split()
        directory, files = data[0], data[1:]
        for file in files:
            name, content = file.split('(')
            d[content].append(directory + '/' + name)
    return [v for v in d.values() if len(v) > 1]

# Follow up questions:
# https://leetcode.com/problems/find-duplicate-file-in-system/discuss/104120/Follow-up-questions-discussion


class Test(unittest.TestCase):
    data = [(['root/a 1.txt(abcd) 2.txt(efgh)', 'root/c 3.txt(abcd)', 'root/c/d 4.txt(efgh)', 'root 4.txt(efgh)'],
             [['root/a/2.txt', 'root/c/d/4.txt', 'root/4.txt'], ['root/a/1.txt', 'root/c/3.txt']])]

    def test_find_duplicate(self):
        for test_paths, result in self.data:
            self.assertEqual(result, find_duplicate(test_paths))


if __name__ == '__main__':
    unittest.main()

""" Given a collection of numbers that might contain duplicates, return all possible unique permutations. """

from collections import Counter
import unittest2 as unittest


def permute_unique_v1(nums):
    """ We can use hash map to check whether the element was already taken.
    Time complexity: O(N * N!)
    Space complexity: O(N)
    """

    def dfs(index):
        if index == n:
            res.append(path[:])
            return
        for num in counter:
            if counter[num] == 0:
                continue
            path.append(num)
            counter[num] -= 1
            dfs(index + 1)
            path.pop()
            counter[num] += 1

    counter = Counter(nums)
    n, res, path = len(nums), [], []
    dfs(0)
    return res


class Test(unittest.TestCase):
    data = [([1, 1, 2], [[1, 1, 2], [1, 2, 1], [2, 1, 1]])]

    def test_permute_unique(self):
        for test_nums, result in self.data:
            self.assertEqual(result, permute_unique_v1(test_nums))


if __name__ == '__main__':
    unittest.main()

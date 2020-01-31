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

# https://leetcode.com/problems/permutations-ii/discuss/18594/Really-easy-Java-solution-much-easier-than-the-solutions-with-very-high-vote
# https://ibb.co/k4zv00
# https://ibb.co/ncMm7f


def permute_unique_v2(nums):
    """ Sort the array to make sure we can skip the same value.
        Use an extra boolean array 'used' to indicate whether the value is added to 'path'.
        When an array element has the same value as its previous, we can use this element only if its previous was
        used.
    Time complexity: O(N * N!)
    Space complexity: O(N)
    """

    def dfs(index):
        if index == n:
            res.append(path[:])
            return
        for i in range(n):
            if used[i] or i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            path.append(nums[i])
            used[i] = True
            dfs(index+1)
            used[i] = False
            path.pop()

    nums.sort()
    n = len(nums)
    path, res, used = [], [], [False] * n
    dfs(0)
    return res


class Test(unittest.TestCase):
    data = [([1, 1, 2], [[1, 1, 2], [1, 2, 1], [2, 1, 1]])]

    def test_permute_unique(self):
        for test_nums, result in self.data:
            self.assertEqual(result, permute_unique_v1(test_nums))
            self.assertEqual(result, permute_unique_v2(test_nums))


if __name__ == '__main__':
    unittest.main()

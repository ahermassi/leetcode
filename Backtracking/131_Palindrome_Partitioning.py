""" Given a string s, partition s such that every substring of the partition is a palindrome.
Return all possible palindrome partitioning of s. """

import unittest2 as unittest


def partition_v1(s):
    """ We will take 'snapshots' of snippets as we advance through the string and see if they can add to the
        decomposition that we want to build.
        Our Choice: The start and the end of a 'snapshot' that we want to add to a decomposition we are working on.
        Our Constraints: Each piece of the decomposition must be a palindrome, we cannot choose and advance on a
        non-palindrome snippet.
        Our Goal: Decompose the whole string. When our decomposition progress index is the length of the array then we
        know that we have achieved this.
    Time complexity: O(N * 2^N), we are basically taking subsets so (2^N) and the O(N) time to copy array to our
    answer. This is a rare worst case where all decompositions turn out to be palindromic (a string of all 1 character).
    Our best case becomes greatly improved.
    Space complexity: O(N), at worst we will always go N stack frames deep in our recursion since an all single
    character decomposition is always a palindromic decomposition.
    """

    def dfs(index, path):
        if index == n:
            res.append(path)
            return
        for i in range(index, n):  # Take every snippet from 'index' to the end of the string. This is our 'possibility
            # space' that we can recurse into.
            if is_palindrome(index, i):  # Only recurse if the snippet from 'index' (inclusive) to s.length()
                # (inclusive) is a palindrome
                dfs(i + 1, path + [s[index:i + 1]])  # Take the snippet and add it to our decomposition 'path', then
                # advance progress 1 past right bound of the palindromic snippet which is 'index + 1'

    def is_palindrome(left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    n, res = len(s), []
    dfs(0, [])
    return res


def partition_v2(s):
    """ Same solution but with a clearer backtracking.
    Time complexity: O(N * 2^N)
    Space complexity: O(N)
    """

    def dfs(index, path):
        if index == n:
            res.append(path[:])  # Append a copy of path because the same path reference is used by all recursive calls
            return
        for i in range(index, n):
            if is_palindrome(index, i):
                path.append(s[index:i + 1])  # Choose
                dfs(i + 1, path)  # Recurse
                path.pop()  # Backtrack, un-choose. We are done searching, remove the snippet from our 'path'. Next
                # loop iteration will try another snippet in this stack frame.

    def is_palindrome(left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    n, res = len(s), []
    dfs(0, [])
    return res


class Test(unittest.TestCase):
    data = [('aab', [['a', 'a', 'b'], ['aa', 'b']])]

    def test_partition(self):
        for test_s, result in self.data:
            self.assertEqual(result, partition_v1(test_s))
            self.assertEqual(result, partition_v2(test_s))


if __name__ == '__main__':
    unittest.main()

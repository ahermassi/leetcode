""" Given a string s, partition s such that every substring of the partition is a palindrome.
Return all possible palindrome partitioning of s. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=4ykBXGbonlA

def partition_v1(s):
    """ The aim is to partition the string into all possible palindrome combinations. To achieve this, we must generate
         all possible substrings of a string by partitioning at every index until we reach the end of the string.

         The first thing that comes to mind is Depth First Search. In Depth First Search, we recursively expand
         potential candidate until the defined goal is achieved. After that, we backtrack to explore the next potential
         candidate.

         In the backtracking algorithm, we recursively traverse over the string in depth-first search fashion. For each
         recursive call, the beginning index of the string is given as 'index'.

            - Iteratively generate all possible substrings beginning at index. The i pointer iterates from index till
               the end of the string.

            - For each of the substrings generated, check if it is a palindrome.

            - If the substring is a palindrome, the substring is a potential candidate. Add substring to the path and
               perform a depth-first search on the remaining substring. If current substring ends at index j, j+1 becomes
               the start index for the next recursive call.

            - Backtrack if start index is equal to the string length and add the path to the result.

        We will take 'snapshots' or snippets as we advance through the string and see if they can add to the
        decomposition that we want to build.

        Our Choice: The start and the end of a snapshot that we want to add to a decomposition we are working on.

        Our Constraints: Each piece of the decomposition must be a palindrome, and we cannot choose and advance on a
        non-palindrome snippet.

        Our Goal: Decompose the whole string. When our decomposition progress index is the length of the string, then we
        know that we have achieved this.

    Time complexity: O(N * 2^N), we are basically taking subsets so (2^N). It is the number of possible partitioning
    (each partitioning is a way to partition the string into substrings). For each partitioning, we do two things: build
    the substrings for that partition and check whether each substring in that partitioning is a palindrome or not.
    O(N * 2^N) is a rare worst case where all decompositions turn out to be palindromic (for example, a string of all
    1 character like 'aaaaa'). Our best case becomes greatly improved.
    Note: The number 2^N in complexity analysis above is in fact the number of nodes in the search tree - NOT the number
    of substrings. It is the number of possible partitioning (each partitioning is a way to partition the string into
    substrings). This can be derived as follows:
    Imagine the string as a sequence of N chars separated by a pipe between neighbors, such as a string
    "abcde" = a|b|c|d|e. Such a representation will have N-1 pipes - in this example, 4 pipes.
    If we want the partitioning to have 4 substrings, then we can ask, "how many ways can we select 3 pipes out of the 4
    pipes?" - answer is 4 choose 3, i.e. 4C3 = 4. The 4 ways to partition are:
    { {"a", "b", "c", "de"}, {"a", "b", "cd", "e"}, {"a", "bc", "d", "e"}, {"ab", "c", "d", "e"}
    Arguing like the above, the total number of ways to partition this example is when we ask all questions "how many
    ways can we select 0 or 1 or 2 or 3 or 4 pipes?" = 4C0 + 4C1 + 4C2 + 4C3 + 4C4 = 24 = 16
    In general, a string of length N will have N-1C0 + N-1C1 + ... +N-1CN-2 = 2N-1 = 2N-1 = O(2^N) partitioning.
    So to summarize: For a string of length N, there will be (N - 1) intervals between characters. For every interval, we
    can cut it or not cut it, so there will be 2^N ways to partition the string. For every partition way, we need to check
    if it is palindrome, which is O(N).
    Space complexity: O(N), at worst we will always go N stack frames deep in our recursion since an all single
    character decomposition is always a palindromic decomposition.
    """

    def dfs(index, path):
        if index == n:
            res.append(path)
        for i in range(index, n):  # Take every snippet from 'index' to the end of the string. This is our 'possibility
            # space' that we can recurse into.
            if is_palindrome(index, i):  # Only recurse if the snippet from 'index' (inclusive) to current index i
                # (inclusive) is a palindrome
                dfs(i + 1, path + [s[index:i + 1]])  # Take the snippet and add it to our decomposition 'path', then
                # advance/progress 1 past right bound of the palindromic snippet which is (i + 1)

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

    def dfs(index):
        if index == n:
            res.append(path[:])  # Append a copy of path because the same path reference is used by all recursive calls
        for i in range(index, n):
            if is_palindrome(index, i):
                path.append(s[index:i + 1])  # Choose
                dfs(i + 1)  # Recurse
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
    path = []
    dfs(0)
    return res


class Test(unittest.TestCase):
    data = [('aab', [['a', 'a', 'b'], ['aa', 'b']])]

    def test_partition(self):
        for test_s, result in self.data:
            self.assertEqual(result, partition_v1(test_s))
            self.assertEqual(result, partition_v2(test_s))


if __name__ == '__main__':
    unittest.main()

""" Given a string s, partition s such that every substring of the partition is a palindrome.
Return all possible palindrome partitioning of s. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=4ykBXGbonlA
# Video explanation: https://youtu.be/3jvWodd7ht0
def partition_v1(s):
    """ The aim is to partition the string into all possible palindrome combinations. To achieve this, we must generate
         all possible substrings of the string by partitioning at every index until we reach the end of the string. Each
         generated substring is considered as a potential candidate if it's a palindrome.

         The first idea is to generate all possible substrings of the given string and expand each possibility if it is
         a potential candidate. The first thing that comes to mind is Depth-First Search. In Depth-First Search, we
         recursively expand potential candidates until the defined goal is achieved. After that, we backtrack to explore
         the next potential candidate.

         The backtracking algorithm consists of the following steps:

            - Choose: choose the potential candidate. Here, the potential candidates are all substrings that could be
               generated from the given string.

            - Constraint: define a constraint that must be satisfied by the chosen candidate. In this case, the
               constraint is that the substring must be a palindrome.

            - Goal: we define the goal that determines if we have found the required solution and must backtrack. Here,
               the goal is achieved if we have reached the end of the string.

         In the backtracking algorithm, we recursively traverse over the string using depth-first search. At each
         recursive call, the start index of the string is given as 'index'.

            - Iteratively generate all possible substrings starting at 'index'. The i pointer iterates from 'index' to
               the end of the string.

            - For each of the generated substrings, check if it is a palindrome.

            - If the substring is a palindrome, the substring is a potential candidate. Add the substring to the path
               and perform a depth-first search on the remaining substring. If current substring ends at index j, j+1
               becomes the start index for the next recursive call.

            - Backtrack if start index is equal to the string length and add the path to the result.

        We take 'snapshots' or snippets as we advance through the string and see if they can add to the decomposition
        that we want to build.

            - Choice: the start and the end of a snapshot that we want to add to a decomposition we are working on.

            - Constraint: each piece of the decomposition must be a palindrome, and we cannot choose and advance on a
               non-palindromic snippet.

            - Goal: decompose the whole string. When the decomposition progress index is the length of the string,
               then we know that we achieved the goal.

    Time complexity: O(N * 2^N), we are basically taking subsets so (2^N). It is the number of possible partitioning
    (each partitioning is a way to partition the string into substrings). For each partitioning, we do two things: build
    the substrings for that partition and check whether each substring in that partitioning is a palindrome or not.
    O(N * 2^N) is a rare worst case where all decompositions turn out to be palindromic (for example, a string of all
    1-character like 'aaaaa'). The best case becomes greatly improved.
    Note: The number 2^N in complexity analysis above is in fact the number of nodes in the search tree - NOT the number
    of substrings. It is the number of possible partitionings (each partitioning is a way to partition the string into
    substrings). This can be derived as follows:
    Imagine the string as a sequence of N characters separated by a pipe between neighbors, such as a string
    "abcde" = a|b|c|d|e. Such representation will have N-1 pipes - in this example, 4 pipes.
    If we want the partitioning to have 4 substrings, then we can ask, "how many ways can we select 3 pipes out of the 4
    pipes?" - answer is 4 choose 3, i.e. 4C3 = 4. The 4 ways to partition are:
    { {"a", "b", "c", "de"}, {"a", "b", "cd", "e"}, {"a", "bc", "d", "e"}, {"ab", "c", "d", "e"}
    Arguing like the above, the total number of ways to partition this example string is when we ask all questions
    "how many ways can we select 0 or 1 or 2 or 3 or 4 pipes?" = 4C0 + 4C1 + 4C2 + 4C3 + 4C4 = 16.
    In general, a string of length N will have N-1C0 + N-1C1 + ... +N-1CN-2 = 2N-1 = 2N-1 = O(2^N) partitioning.
    So to summarize: for a string of length N, there will be N-1 intervals between characters. For every interval, we
    can cut it or not cut it, so there will be 2^N ways to partition the string. For every partition way, we need to
    check if it is palindrome, which is O(N).
    Space complexity: O(N), at worst we always go N stack frames deep in the recursion since an all single character
    decomposition is always a palindromic decomposition.
    """

    def dfs(index, path):
        if index == n:
            res.append(path)
        for i in range(index, n):
            # Take every snippet from 'index' to the end of the string. This is the 'possibility space'.
            if is_palindrome(index, i):
                # Only recurse if the snippet from 'index' (inclusive) to current index i (inclusive) is a palindrome.
                # Take the snippet and add it to the current decomposition 'path', then advance 1 past the right
                # bound of the palindromic snippet which is i+1
                dfs(i + 1, path + [s[index:i + 1]])

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
    """ Same solution but with an explicit backtracking template.

    Time complexity: O(N * 2^N)
    Space complexity: O(N)
    """

    def dfs(index):
        if index == n:
            # Append a copy of path because the same path reference is used by all recursive calls
            res.append(path[:])
        for i in range(index, n):
            if is_palindrome(index, i):
                path.append(s[index:i + 1])  # Choose
                dfs(i + 1)  # Recurse
                path.pop()  # Backtrack, undo the choice. We are done searching, remove the snippet from the
                # 'path'. Next loop iteration will try another snippet in this stack frame.

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


def partition_v3(s):
    """ Backtracking + Dynamic Programming.

         This approach uses a similar backtracking algorithm. However, the previous approaches perform one extra
         iteration to determine if a given substring is a palindrome. We are repeatedly iterating over the same
         substrings multiple times and the result is always the same. There are overlapping sub-problems, and we could
         further optimize the algorithm by using Dynamic Programming to determine if a string is a palindrome in
         constant time.

         A given string s starting at index 'start' and ending at index 'end' is a palindrome if the following two
         conditions are satisfied :

            1- The characters at 'start' and 'end' indices are equal
            2- The substring starting at index start+1 and ending at index end−1 (inclusive) is a palindrome

        Let N be the length of the string. To determine if a substring starting at index 'start' and ending at index
        'end' is a palindrome, we use a 2-dimensional array dp of size N * N where:

                   dp[start][end] = true if s[start:end+1] is a palindrome.
                   Otherwise, dp[start][end] = false

        Also, we must update the dp array if we find that the current substring is a palindrome.

        The logic is similar to the DP solution of 5- Longest Palindromic Substring.

    Time complexity: O(2^N), in the worst case there could be 2^N possible substrings. However, we are eliminating one
    additional iteration to check if the substring is a palindrome.
    Space complexity: O(N^2), for the call stack and dp array
    """
    def dfs(index, path):
        if index == n:
            res.append(path)
        for i in range(index, n):
            if s[index] == s[i] and (i - index <= 1 or dp[index + 1][i - 1]):
                dp[index][i] = True
                dfs(i + 1, path + [s[index:i + 1]])
                # How is dp[index+1][i-1] available even when we are at position 'index'? i always starts from
                # 'index'' which is trying to add s[index] to the path. Since a single character is a palindrome,
                # and the program recursively calls dfs(index+1) when i==index, therefore, when the call returns from
                # index+1, dp[index+1] is already set.

    n, res = len(s), []
    dp = [[False] * n for _ in range(n)]
    dfs(0, [])
    return res


class Test(unittest.TestCase):
    data = [('aab', [['a', 'a', 'b'], ['aa', 'b']])]

    def test_partition(self):
        for test_s, result in self.data:
            self.assertEqual(result, partition_v1(test_s))
            self.assertEqual(result, partition_v2(test_s))
            self.assertEqual(result, partition_v3(test_s))


if __name__ == '__main__':
    unittest.main()

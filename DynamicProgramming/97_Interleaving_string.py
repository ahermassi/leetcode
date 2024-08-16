""" Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of s1 and s2.

An interleaving of two strings s and t is a configuration where s and t are divided into n and m
substrings
 respectively, such that:

s = s1 + s2 + ... + sn
t = t1 + t2 + ... + tm
|n - m| <= 1
The interleaving is s1 + t1 + s2 + t2 + s3 + t3 + ... or t1 + s1 + t2 + s2 + t3 + s3 + ...
"""


def is_interleave(s1, s2, s3):
    """ Top-Down Dynamic Programming.

         We can take all possible substrings of s1 and s2 and check if s3 can be formed by interleaving them. At each
         step, we have two options: choose a character from s1 or s2.

         Let's define a helper recursive function dfs(i, j, k). that returns whether s3[k:] can be formed from
         interleaving s1[i:] and s2[j:]. Then the two choices can be represented as:

            - dfs(i + 1, j, k + 1): choose a character at ith index from s1
            - dfs(i, j + 1, k + 1): choose a character at jth index from s2

        Actually, we can make this choice more smartly. Instead of considering all possibilities, we can make
        either/both choice(s) only when it matches the character at the kth index of s3.

        The recursion ends when either of the two strings s1 or s2 has been fully processed. If, let's say, the string
        s1 has been fully processed, we only compare the remaining portion of s2 with the remaining portion of s3.

        !!! IMPORTANT !!!
        memo[i][j] stores a 1/0 depending on whether we can use s1[i:] and s2[j:] to interleave s3[i+j:].
        Consider the following example: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac".
        When we are at the state dfs(1, 1), we're asking the following question: can s1[1:] and s2[2:] be used to
        interleave the rest of s3? Notice that when i=1 and j=2, it means 3 characters have been used up, one character
        from s1 and 2 characters from s2. So now the interleaving check needs to skip the first 3 characters of s3 and
        set the index to 3 = i + j = 1 + 2.
        For this reason, we can consider the DFS variable k as a derivative of i and j: k = i + j. Thus, it's not one of
        the dimensions of the cache.

    Time complexity: O(N * M), where N is the length of s1 and M is the length of s2
    Space complexity: O(N * M)
    """

    def dfs(i, j, k):
        if i == n and j == m:
            return k == l
        if i == n:
            return s2[j:] == s3[k:]
        if j == m:
            return s1[i:] == s3[k:]
        if (i, j) in memo:
            return memo[(i, j)]
        use_s1 = (s1[i] == s3[k] and dfs(i + 1, j, k + 1))
        use_s2 = (s2[j] == s3[k] and dfs(i, j + 1, k + 1))
        memo[(i, j)] = use_s1 or use_s2
        return memo[(i, j)]

    n, m, l = len(s1), len(s2), len(s3)
    if n + m != l:
        return False
    memo = {}
    return dfs(0, 0, 0)
""" Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of s1 and s2.

An interleaving of two strings s and t is a configuration where s and t are divided into n and m
substrings
 respectively, such that:

s = s1 + s2 + ... + sn
t = t1 + t2 + ... + tm
|n - m| <= 1
The interleaving is s1 + t1 + s2 + t2 + s3 + t3 + ... or t1 + s1 + t2 + s2 + t3 + s3 + ...
"""


def is_interleave_v1(s1, s2, s3):
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


def is_interleave_v2(s1, s2, s3):
    """ Top-Down Dynamic Programming.

         As mentioned above, DFS variable k is a derivative of i and j, i.e. i + j = k. So we no longer need to pass k
         to the DFS.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def dfs(i, j):
        if i == n and j == m:
            return True
        if i == n:
            return s2[j:] == s3[i + j:]
        if j == m:
            return s1[i:] == s3[i + j:]
        if (i, j) in memo:
            return memo[(i, j)]
        use_s1 = s1[i] == s3[i + j] and dfs(i + 1, j)
        use_s2 = s2[j] == s3[i + j] and dfs(i, j + 1)
        memo[(i, j)] = use_s1 or use_s2
        return memo[(i, j)]

    n, m, l = len(s1), len(s2), len(s3)
    if n + m != l:
        return False
    memo = {}
    return dfs(0, 0)


# Video explanation: https://youtu.be/3Rw3p9LrgvE
def is_interleave_v3(s1, s2, s3):
    """ Bottom-Up Dynamic Programming.

         Let dp[i][j] be whether s1[i:] and s2[j:] can be used to interleave s3. Let's say the character just included
         i.e. either at ith index of s1 or at jth index of s2 matches the character at index k=i+j+1.

        If the character just included (say x) which matches the character at kth index of s3, is the character at ith
        index of s1, we need to keep x at the first position in the resultant interleaved string formed so far. Thus,
        in order to use string s1 and s2 up to indices i and j to form a resultant string of length i+j+2 which is a
        suffix of s3, we need to ensure that the strings s1 and s2 up to indices i+1 and j respectively obey the same
        property.

        Similarly, if we just included the jth character of s2, which matches with the kth character of s3, we need to
        ensure that the strings s1 and s2 up to indices i and j+1 also obey the same property.

        Based on the above rules, we have the transition function:

                    dp[i][j] = (s1[i] == s3[i + j] and dp[i + 1][j]) OR (s2[j] == s3[i + j] and dp[i][j + 1])

         TODO: define more base cases to get rid of i < n and j < m checks.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m, l = len(s1), len(s2), len(s3)
    if n + m != l:
        return False
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[n][m] = True
    for i in reversed(range(n)):
        for j in range(m, -1, -1):
            use_s1 = i < n and s1[i] == s3[i + j] and dp[i + 1][j]
            use_s2 = j < m and s2[j] == s3[i + j] and dp[i][j + 1]
            dp[i][j] = use_s1 or use_s2
    return dp[0][0]
""" Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:

'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).
The matching should cover the entire input string (not partial). """


def is_match_v1(s, p):
    """ Top-Down Dynamic Programming.

        The first idea here is a recursion. It is a relatively straightforward approach but quite time consuming
        because of huge recursion depth for long input strings.

        The base cases that we need to check is when the pattern index reaches the end of the pattern, then we need to
        verify that the string index has also reached the end of the string, because the matching should cover the
        entire input string (not partial). Also if the string index reaches the end of the string, then the current
        pattern's wildcard needs to be '*' since '*' can match an empty sequence of characters and the rest of the
        pattern has to match an empty string as well.

        If the current characters of pattern and string match or if the current pattern's wildcard is '?', then compare
        the next characters.

        If the current pattern's wildcard is '*', then there are two possible situations:
            - '*' matches no characters, and hence we move the pattern index forward.
            - '*' matches one or more characters, and so we move the string index forward and keep the pattern index
              at its position.

        In all other cases, no match is possible and False can be returned right away.

    Time complexity: O(N * M), where N is the length of s and M is the length of p
    Space complexity: O(N * M), size of the memoization cache
    """

    def dfs(s_index, p_index):
        if (s_index, p_index) in memo:
            return memo[(s_index, p_index)]
        if p_index == m:
            # If we don't check s_index == n then there is a case that we use the entire pattern but not fully
            # match the string s. For example: s = "aa", p = "a".
            return s_index == n
        if s_index == n:
            # This is basically saying that if the string s has been exhausted, then the only way to match is for the
            # current pattern's wildcard to be '*' as well as the subsequent characters (next iterations will come here)
            memo[(s_index, p_index)] = p[p_index] == '*' and dfs(s_index, p_index + 1)
            return memo[(s_index, p_index)]
        cur_s, cur_p = s[s_index], p[p_index]
        if cur_p == '?' or cur_s == cur_p:
            res = dfs(s_index + 1, p_index + 1)
        elif cur_p == '*':
            res = dfs(s_index, p_index + 1) or dfs(s_index + 1, p_index)
        else:
            return False
        memo[(s_index, p_index)] = res
        return res

    n, m = len(s), len(p)
    memo = {}
    return dfs(0, 0)


def is_match_v2(s, p):
    """ Bottom-Up Dynamic Programming.

        The idea would be to reduce the problem to simpler sub-problems. For example, there is a string 'adcebdk' and
        a pattern '*a*b?k', and we want to compute if there is a match for them. We could notice that it seems to be
        more simple for short strings and patterns and so it would be logical to relate a match dp[p_len][s_len] with
        the lengths p_len and s_len of input pattern and string, respectively.

        Let's go further and introduce:

                dp[i][j] = whether the substring from index 0 to i-1 of the original string s matches with the
                subpattern from index 0 to j-1 of the original pattern p. In other words, whether the first i
                characters of s match with the first j character of the pattern p

        It turns out that we could compute dp[i][j] knowing a match without the last characters, i.e. dp[i-1][j-1].

        Initialize dp[0][0] = True. This is because if the length of the pattern and matching string is 0 then they
        are equal or they are a match.

        We fill the first row of dp which tells us if the matching string length is zero, then up to which index the
        pattern matches the empty string. We know that it is only possible if the pattern character at that point is
        '*', and if anything else comes other than a '*' then we break.

        If the last characters are the same or pattern character is '?', then:
                                dp[i][j] = dp[i-1][j-1]

        If the pattern is '*', then we can either use it to match the current character and in that case it would be
        equal to dp[i-1][j], and if we match the empty string with '*' then it is equal to dp[i][j-1]:
                                dp[i][j] = dp[i-1][j] or dp[i][j-1]

        Why dp[i][j] = dp[i-1][j] or dp[i][j-1] ? The idea is:

        If dp[i-1][j] == True --> s(0-->i-2) matches with p(0-->j-1). Now p[j-1] == '*', so at the end of s we can
        add another or more k chars to match '*', making dp[i][j] or even dp[i+k][j] True.

        If dp[i][j-1] == True --> s(0-->i-1) matches with p(0-->j-2). Now p[j-1] == '*', so add this to p, and '*' can
        match none in s. We don't need to add anything to s, we can see now dp[i][j] = True.

        Is dp[i - 1][j] True? If yes, it means the current subpattern p[0...j-1] we have matches the substring
        s[0... i-2]. Then will p[0...j-1] match with s[0... i-1]? The answer is yes, because '*" can match any sequence
        of characters, so it's able to match one more character s[i - 1].

        Is dp[i][j - 1] True? If yes, it means the current substring s[0...i-1] matches with the subpattern p[0...j-2].
        Therefore, if we add one more '* 'into the subpattern, it will also match as '*' can match empty sequence.

        Example: s = 'xxx', p = 'xx*'
        For i=2, j=2:
        dp[1][2] means we use '*' to match s[2], can we match the remaining sequence in s if we reuse '*' in p?
        dp[2][1] means if we don't use '*' to match any characters at all, our s[2] would have to match p[1];
        i.e. the characters before '*' in p would have to match characters in s so far, meaning dp[i][j-1].

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m = len(s), len(p)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for j in range(1, m + 1):
        if p[j - 1] != '*':
            break
        dp[0][j] = True
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == '?':
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                dp[i][j] = dp[i-1][j] or dp[i][j-1]
    return dp[n][m]


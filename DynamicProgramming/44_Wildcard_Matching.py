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

""" Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.

You have the following three operations permitted on a word:

Insert a character
Delete a character
Replace a character
"""


# Video explanation: https://youtu.be/XYi2-LPrwm4
# Video explanation: https://www.youtube.com/watch?v=MiqoA-yF-0M
def min_distance_v1(word1, word2):
    """ Top-Down Dynamic Programming.

         There are different types of "edit distance" each having different types of operations to transform one string
         to another. In this problem, we are referring to Levenshtein distance.

         The Levenshtein distance finds edit distances by allowing three types of transformation operations: addition,
         deletions, and replacements.

         Let us start by first identifying the ground rules.

            - If the two strings are the same, the edit distance is zero.
               word1 = "abcd", word2 = "abcd"
               Edit Distance = 0
               word1 is equal to word2; no need to add, remove or replace any character.

         - The operations (add/delete/replace) are performed if and only if a character at a certain position in word1
            is not equal to the corresponding character in word2.
            word1 = "abc", word2 = "abe"
            The words are not the same. The character at 3rd position in word1 c is different from the character in
            word2 e. In this case, we have to perform some operation in word1 to transform it into word2.
            There are 3 options: delete c from word1, insert e into word1, or replace c with e in word1.

        The goal is to choose an option such that word1 is transformed into word2 by applying the minimum number of
        operations. From this, we can conclude that:

                    Edit distance to transform word1 to word2 = Minimum (
                                number of operations after deleting from word1,
                                number of operations after inserting in word1,
                                number operations after replacing in word1)
                                + 1

        The +1 is to account for the current operation.

        Whenever there is a mismatch between 2 characters in the strings, we have to try all possible operations and
        choose the best among all.

            - Start by comparing every character in word1 and word2. Let's track the current character index as i for
               word1 and j for word2.

            - If the characters in the current position match, move to the next index. No operation is performed.

            - If the characters in their current position do not match, we must delete, insert or replace a character
               in word1. We must try all three operations and find the minimum.

        Let's define a recursive function dfs(i,j), which finds the edit distance for word1 starting at index i and
        word2 starting at j. Let's derive the recurrence relation for each possible operation.

            - Replace word1[i] with word2[j]: recurrence relation 1 + dfs(i+1, j+1)

            - Insert word2[j] in word1: recurrence relation 1 + dfs(i, j+1)

            - Delete word1[i]: recurrence relation 1 + dfs(i+1, j)

        In the end, the minimum of all the above operations will be the minimum edit distance.

        Base cases:

        If word1 is an empty string, there could be zero or more characters left in word2. The only possible operation
        is to add the characters of word2 in word1. The edit distance is the number of characters in word2.

        If word2 is an empty string, there could be zero or more characters left in word1. The only possible operation
        is to delete all the remaining characters in word1. The edit distance is the number of characters in word1.

        The important thing to note is that we are simulating the edit operations by moving i and j around, not actually
        changing the input strings.

        c1 = sample, c2 = example
        i = 0 (s), j = 0 (e)
        Replace the current character with the character we need from word2. We then increment i and j to look at the
        next characters --> dfs(i+1, j+1)

        c1 = eample, c2 = example
        i = 1 (a), j = 1 (x)
        Delete removes the first character, shifting the word 1 character to left. Since we do not actually delete the
        character, incrementing i simulates skipping this character --> dfs(i+1, j)

        c1 = sample, c2 = example
        i = 1 (a) , j = 0 (e)
        Insert is the opposite of delete. We insert the character we need, shifting the word 1 to the right. Since we do
        not actually add a character, leave i alone. It's the similar as doing c1 = e + c1. Since we added e, i+1 would
        point to s --> dfs(i, j+1)

        We enable the algorithm to cache or memorize the result of every operation, so that every time before computing
        the result for a problem, we can look if the result is already present in the cache. The following is an example
        of a recursion call tree. The recursive calls with multiple invocations are highlighted.

        dfs("horse", "hello")
	        dfs("orse", "ello")
		        dfs("orse", "llo")
			        dfs("orse", "lo")
			        dfs("rse", "llo") <-
			        dfs("rse", "lo")
		        dfs("rse", "ello")
			        dfs("rse", "llo") <-
			        dfs("se", "ello")
			        dfs("se", "llo") <<-
		    dfs("rse", "llo")
			    dfs("rse", "llo") <-
			    dfs("se", "llo") <<-
			    dfs("se", "lo")

        Summary:

        Base case: word1 = "" or word2 = ""    --> return length of other string
        Recursive case: word1[i] == word2[j]  --> recurse on word1[i+1:] and word2[j+1:]
        Recursive case: word1[i] != word2[j]   --> recurse by inserting, deleting, or replacing

    Time complexity: O(N * M), where N is the length of string word1 and M is the length of string word2. As the
    memoization approach uses the cache, for every combination of word1 and word2 the result is computed only once.
    Space complexity: O(N * M)
    """

    def dfs(i, j):
        # minimum number of operations to convert word1[i:] to word2[j:]
        if i == n:
            return m - j
        if j == m:
            return n - i
        if (i, j) in memo:
            return memo[(i, j)]
        if word1[i] == word2[j]:
            memo[(i, j)] = dfs(i + 1, j + 1)
        else:
            delete = dfs(i + 1, j)
            replace = dfs(i + 1, j + 1)
            insert = dfs(i, j + 1)
            memo[(i, j)] = min(delete, replace, insert) + 1
        return memo[(i, j)]

    n, m = len(word1), len(word2)
    memo = {}
    return dfs(0, 0)


def min_distance_v2(word1, word2):
    """ Bottom-Up Dynamic Programming.

         Let dp[i][j] be the minimum number of operations required to convert word1[i:] to word2[j:].

         If the characters at current indexes in word1 and word2 are the same, the edit distance will be the same as the
         result of word1[i+1:] and word2[j+1:].

         If the characters at current indexes in word1 and word2 are different, the edit distance will bethe minimum of
         3 operations:

            - Add a character at index i in word1. Example, word1 = a and word2 = qa, i=j=0
               If we add q in word1, the edit distance for word1 = a and word2 = qa will be equal to the edit distance
               for word1 = a and word2 = a plus one.
               The result of the sub-problem word1 = a and word2 = a can be referred from dp[i][j+1].

            - Delete the character at index i in word1. Example, word1 = qa and word2 = a, i=j=0
               If we delete q in word1, the edit distance for word1 = qa and word2 = a will be equal to the edit
               distance for word1 = a and word2 = a plus one.
               The result of the sub-problem word1 = a and word2 = a can be referred from dp[i+1][j].

            - Replace a character at word1Index in word1. Example, word1 = qa and word2 = wa, i=j=0
               If we replace q in word1, the edit distance for word1 = qa and word2 = qa will be equal to the edit
               distance for word1 = a and word2 = a plus one.
               The result of the sub-problem word1 = a and word2 = a can be referred from dp[i+1][j+1].

         Based on these rules, we have the transition function:

                    dp[i][j] = dp[i + 1][j + 1]; if word1[i] == word2[j]
                              OR
                               = 1 + min(dp[i + 1][j], dp[i + 1][j + 1], dp[i][j + 1]); otherwise

        Base cases:
        The last row and last column of the table have known values since if one string is empty, we simply add the
        length of the non-empty string since that is the minimum number of edits necessary to arrive at equivalent
        strings.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m = len(word1), len(word2)
    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][m] = n - i
    for j in range(m + 1):
        dp[n][j] = m - j
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if word1[i] == word2[j]:
                dp[i][j] = dp[i + 1][j + 1]
            else:
                dp[i][j] = 1 + min(dp[i + 1][j], dp[i + 1][j + 1], dp[i][j + 1])
    return dp[0][0]


def min_distance_v3(word1, word2):
    """ Bottom-Up Dynamic Programming.

         Let dp[i][j] be the minimum number of operations required to convert word1[:i+1] to word2[:j+1], i.e. convert
         the first i characters in word1 to the first j characters in word2.

         If the characters at current indexes in word1 and word2 are the same, the edit distance will be the same as the
         result of word1 ending at i-1 and word2 ending at j-1.

         If the characters at current indexes in word1 and word2 are different, the edit distance will bethe minimum of
         3 operations:

            - Add a character at index i in word1. Example, word1 = a and word2 = aq, i=0, j=1
               If we add q in word1, the edit distance for word1 = a and word2 = aq will be equal to the edit distance
               for word1 = a and word2 = a plus one.
               The result of the sub-problem word1 = a and word2 = a can be referred from dp[i][j-1].

            - Delete the character at index i in word1. Example, word1 = aq and word2 = a, i=0, j=1
               If we delete q in word1, the edit distance for word1 = aq and word2 = a will be equal to the edit
               distance for word1 = a and word2 = a plus one.
               The result of the sub-problem word1 = a and word2 = a can be referred from dp[i-1][j].

            - Replace a character at word1Index in word1. Example, word1 = aq and word2 = aw, i=0, j=1
               If we replace q in word1, the edit distance for word1 = aq and word2 = aw will be equal to the edit
               distance for word1 = a and word2 = a plus one.
               The result of the sub-problem word1 = a and word2 = a can be referred from dp[i-1][j-1].

         Based on these rules, we have the transition function:

                    dp[i][j] = dp[i - 1][j - 1]; if word1[i] == word2[j]
                              OR
                               = 1 + min(dp[i - 1][j], dp[i - 1][j - 1], dp[i][j - 1]); otherwise

        Base cases:
        The first row and column of the table have known values since if one string is empty, we simply add the length
        of the non-empty string since that is the minimum number of edits necessary to arrive at equivalent strings.

        Summary:

        When word1[i]=word2[j] , clearly dp[i][j]=dp[i−1][j−1].
        It means that 0∼i−1 of word1 and 0∼j−1 of word2 have been matched.

        When word1[i]!=word2[j] , then dp[i][j]=min(dp[i−1][j−1],dp[i−1][j],dp[i][j−1])+1.
            --> Replacement: since 0∼i−1 of word1 and 0∼j−1 of word2 are the same, so just replace the current
                   character.
            --> Deletion: If 0∼i−1 of word1 and 0∼j of word2 are the same, so we should use dp[i−1][j].
            --> Insertion: If 0∼i of word1 and 0∼j−1 of word2 are the same, so we should use dp[i][j−1].

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m = len(word1), len(word2)
    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        # Need to delete i characters to become ""
        dp[i][0] = i
    for j in range(m + 1):
        # Need to insert j characters to become word2[:j]
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i - 1][j - 1], dp[i][j - 1])
    return dp[n][m]


def min_distance_v4(word1, word2):
    """ Space-optimized Bottom-Up Dynamic Programming.

         Since we build the dp matrix row by row, we only need access to the previous and current dp states. We can
         optimize the space to use only two arrays.

    Time complexity: O(N * M)
    Space complexity: O(M)
    """
    n, m = len(word1), len(word2)
    cur = [float('inf')] * (m + 1)
    pre = [float('inf')] * (m + 1)
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0:
                cur[j] = j
            elif j == 0:
                cur[j] = i
            elif word1[i - 1] == word2[j - 1]:
                cur[j] = pre[j - 1]
            else:
                cur[j] = 1 + min(pre[j], cur[j - 1], pre[j - 1])
        cur, pre = pre, cur
    return pre[m]
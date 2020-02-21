""" Given n, how many structurally unique BST's (binary search trees) that store values 1 ... n? """


def num_trees_v1(n):
    """ Brute force. TLE
        Suppose you are given 1..n, and you want to generate all binary search trees. How do you do it? Suppose you put
        number i on the root, then simply:
            Generate all BST on the left branch by running the same algorithm with 1..(i-1)
            Generate all BST on the right branch by running the same algorithm with (i+1)..n.
            Take all combinations of left branch and right branch, and that's it for i on the root.
        Then you let i go from 1 to n.
        The only problem is, it's very slow, because for large n, you'll need to calculate num_trees(i) many many times,
        where i is a small number. Naturally, to speed it up, you just use memoization.
    Time complexity: O(2^n)
    """
    if n <= 1:
        return 1
    result = 0
    for i in range(1, n + 1):
        left_trees = num_trees_v1(i - 1)
        right_trees = num_trees_v1(n - i)
        result += left_trees * right_trees
    return result


def num_trees_v2(n):
    """ Top-down dynamic programming: recursion + memoization.
    Time complexity: O(2^n)
    """

    def helper(n):
        if n in memo:
            return memo[n]
        res = 0
        for i in range(1, n + 1):
            left = helper(i - 1)
            right = helper(n - i)
            res += left * right
        memo[n] = res
        return res

    memo = {0: 1, 1: 1}
    return helper(n)


# Check out this article: https://leetcode.com/articles/unique-binary-search-trees/
# Watch: https://www.youtube.com/watch?v=GgP75HAvrlY

def num_trees_v3(n):
    """ Bottom-up dynamic programming.
        Given a sequence 1..n, to construct a Binary Search Tree (BST) out of the sequence, we could enumerate each
        number i in the sequence, and use the number as the root. Naturally, the sub sequence 1..(i-1) on its left side
        would lay on the left branch of the root, and similarly the right sub sequence (i+1)..n lay on the right branch
        of the root. We then can construct the subtree from the sub sequence recursively. Through the above approach,
        we could ensure that the BST that we construct are all unique, since they have unique roots.
        The problem is to calculate the number of unique BST.
        Let:
            dp[n]: the number of unique BST for a sequence of length n
            F(i,n), 1 <= i <= n: the number of unique BST rooted at i, and the sequence ranges from 1 to n
        As we can see, dp(n) is the actual function we need to calculate in order to solve the problem, and dp(n) can
        be derived from F(i, n), which at the end, would recursively refer to dp(n).
        We can see that the total number of unique BST dp(n) is the sum of F(i) using each number i as a root:
            dp(n) = F(1, n) + F(2, n) + ... + F(n, n)
        Given a sequence 1..n, we pick a number i out of the sequence as the root, then the number of unique BST with
        the specified root F(i), is the cartesian product of the number of BST for its left and right subtrees.
        For example, F(3,7): the number of unique BST tree with number 3 as its root. To construct an unique BST out of
        the entire sequence [1, 2, 3, 4, 5, 6, 7] with 3 as the root, which is to say, we need to construct a unique
        BST out of its left sub sequence [1, 2] and another BST out of the right sub sequence [4, 5, 6, 7], and then
        combine them together (i.e. cartesian product). The tricky part is that we could consider the number of unique
        BST out of sequence [1, 2] as dp(2), and the number of of unique BST out of sequence [4, 5, 6, 7] as dp(4).
        Therefore, F(3,7) = dp(2) * dp(4).
            F(i,n) = dp(i-1) * dp(n-i)	1 <= i <= n
        Combining the above two formulas, we obtain the recursive formula for dp(n):
            dp(n) = dp(0) * dp(n-1) + dp(1) * dp(n-2) + … + dp(n-1) * dp(0)
        In terms of calculation, we need to start with the lower number, since the value of dp(n) depends on the values
        of dp(0)..dp(n-1)
        Visualization:

        n = 0;     null
        dp[0] = 1

        n = 1;      1
        dp[1] = 1

        n = 2;    1__       			 __2
    	    	      \					/
    		         dp[1]	   	    dp[1]

        dp[2] = 1 + 1 = 2

        n = 3;    1__				      __2__	                   __3
    		         \		            /       \			      /
    		      dp[2]		        dp[1]        dp[1]		 dp[2]

        dp[3] = 2 + 1 + 2  = 5

        n = 4;    1__  					__2__					   ___3___
    		         \				  /        \				  /		  \
    		         dp[3]		 dp[1]         dp[2]		  dp[2]        dp[1]

                 __4
               /
           dp[3]

        dp[4] = 5 + 2 + 2 + 5 = 14
        And  so on...
    Time complexity: O(n^2)
    Space complexity: O(n), the storage to keep all the intermediate solutions
    """
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        for j in range(1, i + 1):
            dp[i] += dp[j - 1] * dp[i - j]
    return dp[n]

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
    if n == 0 or n == 1:
        return 1
    result = 0
    for i in range(1, n + 1):
        left_trees = num_trees_v1(i - 1)
        right_trees = num_trees_v1(n - i)
        result += left_trees * right_trees
    return result


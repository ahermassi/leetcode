""" Given two integers n and k, return all possible combinations of k numbers out of 1 ... n. """


def combine_v1(n, k):
    """ Here is a backtrack function which takes a first integer to add 'index' and a current combination 'path'
        as arguments.
            - If the current combination is done, add it to output
            - Iterate over the integers from 'index' to n
                - Add integer i into the current combination
                - Proceed to add more integers into the combination
                - Backtrack by removing i from 'path' (while implicit here, it can be made explicit)
    Time complexity: O(choose(n, k)), the umber of combinations to build
    Space complexity: O(choose(n, k))
    """

    def dfs(index, path):
        if len(path) == k:
            res.append(path)
            return
        for i in range(index, n + 1):
            dfs(i + 1, path + [i])

    res = []
    dfs(1, [])
    return res

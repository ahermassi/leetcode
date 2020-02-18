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
    Space complexity: O(k), for call stack
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


def combine_v2(n, k):
    """ Optimized version of the previous algorithm.
        In fact, we should not continue exploring when we know that there won't be enough numbers left between 'index'
        and n to fill the needed k slots. If n = 10, k = 5, and we're in the outermost level of recursion, we choose
        only i = 1...6 , because if we pick i = 7 and call dfs() we only have 8, 9, 10 to pick from, so at most we will
        get [7, 8, 9, 10] although we need 5 elements.
    Time complexity: O(choose(n, k))
    Space complexity: O(k)
    """

    def dfs(index, path):
        if len(path) == k:
            res.append(path)
            return
        remaining = k - len(path)
        i = index
        while i <= n and remaining <= n - i + 1:  # (n - i + 1) is the number of possible integers between i and n
            dfs(i + 1, path + [i])
            i += 1

    res = []
    dfs(1, [])
    return res

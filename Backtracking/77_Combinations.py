""" Given two integers n and k, return all possible combinations of k numbers out of 1 ... n. """


# Video explanation: https://youtu.be/q0s6m7AiM7o
def combine_v1(n, k):
    """ We are given that n <= 20. Typically, problems that ask to find "all of something" with low bounds can be solved
         with backtracking.

         Backtracking is a general algorithm for finding all (or some) solutions to some computational problems which
         incrementally builds candidates to the solution and abandons a candidate ("backtracks") as soon as it
         determines that the candidate cannot lead to a valid solution.
         It is due to this backtracking behavior that backtracking algorithms are often much faster than the brute
         force search algorithm, since they eliminate many unnecessary explorations.

         Overall, the enumeration of candidates is done in two levels:

            1- At the first level, the function is implemented as recursion. At each occurrence of recursion, the
                 function is one step further to the final solution.
            2- At the second level, within the recursion, we have an iteration that allows us to explore all the
                 candidates that are of the same progress to the final solution.

        The range of elements we are working with is [1, n]. To generate a combination one element at a time, we will
        use an array 'path'' that represents the current combination we are building.

        To start, we add the first element 1, so we have path = [1]. We are locking in this 1, and we will now find all
        combinations that start with 1.

        To find all combinations that start with 1, we start by adding the first element after 1, which is 2. We now
        have path = [1, 2]. We are locking in this 2, and we will now find all combinations that start with [1, 2].

        This continues until we reach the target length k. Let's say that we have finished finding all combinations that
        start with [1, 2]. Now what? We BACKTRACK by removing the 2, and we have path = [1] again. Now, we add the
        second element that comes after 1, which is 3. We have path = [1, 3], and now we need to find all combinations
        that start with [1, 3].

        Once we find all the combinations that start with [1], we backtrack by removing the 1 from path and adding the
        next element. We have path = [2], and now we need to find all combinations that start with 2.

        This process is recursive in nature. Each time we add an element, we solve a new version of the problem (find
        all combinations that start with the PREFIX path). The initial version of the problem is to find all
        combinations that start with [], which represents all possible combinations.

        The best way to think about the backtracking process is by modeling it as a tree. Imagine the solution space as
        a tree, with each node representing a version of path. Label each node with a number that represents the last
        number in path. Moving to a child is like adding the child's label to path.

        To prevent duplicate combinations like [1, 2] and [2, 1], a node only has children with labels greater than its
        own. The root node represents an empty []. From the root, every node's path represents the path taken from the
        root. The nodes at depth k represent the answer combinations.

        Solving this problem is equivalent to "traversing" this tree. The easiest way to perform the traversal is by
        using recursion and passing path as an argument.

        Refer to 46- Permutations for details about a similar process.

    Time complexity: O(choose(n, k)), the number of combinations to build. The number of combinations of length k
    from a set of n elements is equal to the binomial coefficient, also known as "n choose k": n!/(k! * (n-k)!)
    Space complexity: O(k), for the call stack
    """

    def compute_combinations_at_index(index, path):
        if len(path) == k:
            res.append(path)
            return
        for i in range(index, n + 1):
            compute_combinations_at_index(i + 1, path + [i])

    res = []
    compute_combinations_at_index(1, [])
    return res


def combine_v2(n, k):
    """ Optimized version of the previous algorithm.

         In fact, we should not continue exploring when we know that there won't be enough numbers left between 'index'
         and n to reach a path length of k. We should avoid paths like these as they are a waste of time.

         For example, if n = 10, k = 5, and we're in the outermost level of recursion, we choose only i = 1...6 ,
         because if we pick i = 7 and call dfs() we only have 8, 9, 10 to choose from, so at most we will get
         [7, 8, 9, 10] although we need 5 elements.

         At each node, we have path.length elements so far. We need to reach k elements. Therefore, we can calculate
         needed = k - curr.length as the number of elements we still need to add.

         The range of numbers we are considering in the subtree is [index, n]. The size of this range is
         remaining = n - index + 1.

         Finally, we can calculate available = remaining - needed. This value represents the count of numbers available
          to us as children. We should only consider children in the range [index, index + available] instead of the
          range [index, n]. If we moved to a child outside this range, like index + available + 1, then we will run out
          of numbers to use before reaching a length of k.

    Time complexity: O(choose(n, k))
    Space complexity: O(k)
    """

    def dfs(index, path):
        if len(path) == k:
            res.append(path)
            return
        needed = k - len(path)
        remaining = n - index + 1
        available = remaining - needed
        for i in range(index, index + available + 1):
            dfs(i + 1, path + [i])
            i += 1

    res = []
    dfs(1, [])
    return res

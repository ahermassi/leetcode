""" Given a collection of candidate numbers (candidates) and a target number (target), find all unique combinations in
candidates where the candidate numbers sum to target.

Each number in candidates may only be used once in the combination.

Note: The solution set must not contain duplicate combinations. """


def combination_sum(candidates, target):
    """  This is an extension or variation of the earlier problem 39- Combination Sum. Despite all the differences,
          the key algorithm to solve the combination sum problems remains the same, which is  backtracking.

          We incrementally build the combination by adding numbers one at a time, and once we find the current
          combination is not valid, we backtrack (by abandoning the last number we added to the combination) and try
          another candidate.

          There are two differences between this problem and the earlier problem:

            - Each number in the input is not unique. The implication of this difference is that we need some mechanism
               to avoid generating duplicate combinations.

            - Each number can be used only once. The implication of this difference is that once a number is chosen as
               a candidate in the combination, it will not appear again as a candidate later.

        We start off by sorting the input, which could group all the same numbers together. In addition, we need to do
        some tricks with the index of the iteration in order to avoid generating duplicated combinations.

        Once we sort the input array, the occurrences of each unique number would be adjacent to each other. When we
        want to move the index forward, in order to choose the next number to be added to the combination, we need to
        skip certain positions in order to avoid the generation of duplicated combinations. We skip the position if the
        following two conditions are met:

            - i > index: we will pick the number at the current index into the combination, regardless the other
               conditions. This is important, since the iteration should allow us to select multiple instances of a
               unique number into the combination.

            - candidates[i] == candidates[i-1]: we will skip the occurrences of duplicate numbers in-between.

    We optimize the backtracking by adopting the measure of early stopping, i.e. once the sum of current combination
    exceeds the target, we can stop the exploration for the rest of the numbers. Because all the numbers are positive,
    the sum of combination will increase monotonically. It is needless to explore more combinations whose sum goes
    beyond the desired target.

    How does (if i > index and candidates[i] == candidates[i - 1]: continue) help skip duplicate combinations?

    i > index means position 'index'' has been processed, and we have found all the combinations starting from position
    using dfs(). Therefore, if candidates[i] == candidates[i-1] (first time around it evaluates
    candidates[index+1] == candidates[index]),  there is no need to process position i+1 as it will provide combinations
    which have already been found by dfs() from position i-1 hence we skip the step to avoid duplicate combinations.

    Consider the following example: candidates = [1, 1, 1, 2, 2], target 4. Without that condition, we will get 3
    identical combinations:
    [1, 1, 2, 2] from indices [0, 1, 3, 4] of the candidates;
    [1, 1, 2, 2] from indices [0, 2, 3, 4] of the candidates;
    [1, 1, 2, 2] from indices [1, 2, 3, 4] of the candidates.

    i > index: Before explaining this, first recall what index is. index points to the index which we start with in the
    first place before entering the for loop. It is the starting value from which we started picking up numbers. Since
    it's the starting point, so we will definitely take this number. i indicates the index which we are currently
    processing. In one recursive call stack, the value of index is not going to change but the value of i will keep on
    changing. i > index means that we are currently considering a position which is greater than index.

    Now, in the second condition candidates[i] == candidates[i - 1], we are considering an index which is greater than
    'index', meaning we have already used the number which is at index, so if the number after index has the same
    value, then we won't consider it again because that will be a duplicate combination.

    i > index prevents candidates = [1, 1, 1, 2] and target = 3 from generating duplicate [1, 2].
    Backtracking starts at index = 0 (i.e. starts with [1]), and we want to find all combinations which add up to 3,
    mainly [1, 1, 1] and [1, 2]. Once we are done with i = 0, we move on to i = 1. However, since when i = 1, we also
    start with [1] (but with one less 1 compared to i = 0), we don't want to consider starting with another [1] because
    it will probably end up with a duplicate combination. In this case, we will get another [1,2].
    Hence, the condition is like saying - "Hmmmm, I have seen 1 before. It's literally the last i I considered (since
    candidates is sorted), so I better keep incrementing i until i no longer points to a value equal to its
    predecessor".

    Time complexity: O(2^N), in the worst case, the algorithm will exhaust all possible combinations from the input
    array. The runtime of this problem is bounded by the total number of possible combinations of "candidates", because
    we can only use the elements found in the list once. To generate all possible combinations with a list of size N,
    for every index in the list, we have two options - either pick the value at this index or don't pick it. So we have
    2 options for N indices, resulting in 2^N. In 39- Combination Sum, we are not bounded by the number of elements in
    the list. You can use any element in "candidates" an unlimited number of times.
    Space complexity: O(N), for call stack
    """

    def dfs(index, combination, remaining):
        if remaining == 0:
            res.append(combination)
            return
        for i in range(index, n):
            if candidates[i] > remaining:
                break
            if i > index and candidates[i] == candidates[i - 1]:
                continue
            dfs(i + 1, combination + [candidates[i]], remaining - candidates[i])

    n, res = len(candidates), []
    candidates.sort()
    dfs(0, [], target)
    return res

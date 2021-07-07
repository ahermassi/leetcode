""" The chess knight has a unique movement, it may move two squares vertically and one square horizontally, or two
squares horizontally and one square vertically (with both forming the shape of an L).

We have a chess knight and a phone pad as shown below, the knight can only stand on a numeric cell.

Given an integer n, return how many distinct phone numbers of length n we can dial.
You are allowed to place the knight on any numeric cell initially and then you should perform n - 1 jumps to dial a
number of length n. All jumps should be valid knight jumps.

As the answer may be very large, return the answer modulo 109 + 7. """


def knight_dialer_v1(n):
    """ How can we count phone numbers without generating them? It can be done, but not without an additional insight.
        Notice how the count of numbers that can be generated from a given starting position in N hops is equal to the
        sum of the counts of hops that can be generated starting from each of its neighbors in (N - 1) hops.
        Stated mathematically as a recurrence relation, it looks like this:

            T(P, N) =         Σ           T(p, N-1)
                      {p ∈ neighbors(P)}

            where P is a starting position

        This is intuitively obvious when we consider what happens with one hop: 6, for instance, has 3 neighbors
        (1, 7, and 0) and in zero hops we can reach one number for each, so we can only dial three numbers starting
        from 6.
    Time complexity: O(2^N), every call to dfs() recursively calls dfs() at least twice, because each key has at least
    two neighbors. Since we recurse a number of times equal to the desired number of hops, and the number of calls to
    dfs() at least doubles with each call, we’re left with a runtime complexity of at least exponential time.
    Space complexity: O(N)
    """

    def dfs(i, j, remaining_hops):
        # dfs(i, j, x) returns the number of phone numbers we can dial starting from cell (i,j) with x hops
        if not 0 <= i < 4 or not 0 <= j < 3 or (i == 3 and j != 1):
            # The last condition guarantees that we don't land on a non-numeric cell ('*' or '#')
            return 0
        if remaining_hops == 1:  # The cell we're standing at counts for the last remaining hop to make
            return 1
        res = 0
        for x, y in directions:
            res += dfs(i + x, j + y, remaining_hops - 1)
        return res

    directions = [(-1, 2), (-2, 1), (-1, -2), (-2, -1), (1, 2), (2, 1), (1, -2), (2, -1)]
    res = 0
    for i in range(4):
        for j in range(3):
            res += dfs(i, j, n)
    return res % (10 ** 9 + 7)

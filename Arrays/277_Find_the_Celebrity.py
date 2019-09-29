""" Read description on Leetcode """


def knows(i, j):
    pass


def find_celebrity_v1(n):
    """ It is inductive that we can find the candidate and check whether it is up to standard or not.
        How do we decide the candidate?
        We are sure that if A knows B, A cannot be the celebrity while B may be, i.e., B is the candidate. Since there
        is only one celebrity, one loop is enough to decide the candidate.
        How do we check whether the candidate is up to standard?
        According to the definition of a celebrity, if !knows(i, candidate) || knows(candidate, i) exists, the
        candidate is not qualified.
        The moment you realize a call to knows(i,j) eliminates either i or j the problem is solved. knows(i,j) == true
        then i can't be a celebrity. since a celebrity knows nobody and knows(i,j) == false then j can't be a celebrity
        since everyone must know the celebrity.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    candidate = 0
    for i in range(1, n):
        if knows(candidate, i):
            candidate = i
    # We've established that candidate does not know anyone AFTER it
    # Let's establish that candidate is known by, but does not know everyone BEFORE it
    for i in range(candidate):
        if knows(candidate, i):
            return -1
    # Last thing we don't know: Does everyone after candidate know candidate ?
    for i in range(candidate + 1, n):
        if not knows(i, candidate):
            return -1
    return candidate

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
        Notice this interesting property: for any two persons A and B, the possible candidate is always mutually
        exclusive. i.e. only one person of A and B can be candidate. Because if A knows B, A cannot be celebrity; if A
        doesn't know B, B cannot be be celebrity.
        With the above property, traversing and checking every person with a current candidate will filter out all
        'bad guys'.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    candidate = 0
    for i in range(1, n):
        if knows(candidate, i):  # If true, then 'candidate' cannot be the real celebrity because real celebrity should
            # know nobody. If false, then i cannot be the celebrity because celebrity should be known by everyone.
            candidate = i
    # We've established that candidate does not know anyone AFTER him.
    # Let's establish that candidate doesn't know anyone BEFORE him and is known by EVERYONE.
    for i in range(n):
        if i < candidate and (knows(candidate, i) or not knows(i, candidate)):
            return -1
        elif i > candidate and not knows(i, candidate):  # From the first loop we already know that the candidate does
            # not know people ahead of them, so we can just check that everyone ahead of the candidate knows the
            # candidate
            return -1
    return candidate

    # Can be also written:
    # candidate = 0
    # for i in xrange(n):
    #     if knows(candidate, i):
    #         candidate = i
    # for i in range(candidate):
    #     if knows(candidate, i):
    #         return -1
    # for i in range(n):
    #     if not knows(i, candidate):
    #         return -1
    # return candidate


def find_celebrity_v2(n):
    """ Stack based solution. The idea is to push all people to the stack, and then start popping every 2 people.
        If a knows b, so a is not the celebrity, but b may be. If a doesn't know b, so b is not the celebrity, but a
        may be. The only remaining stack element is a potential celebrity. Double check if they are.
    Time complexity: O(n)
    Space complexity: O(n)
    """
    stack = [i for i in range(n)]
    while len(stack) > 1:
        a, b = stack.pop(), stack.pop()
        if knows(a, b):
            stack.append(b)
        else:
            stack.append(a)
    candidate = stack.pop()
    for i in range(n):
        if i != candidate and (knows(candidate, i) or not knows(i, candidate)):
            return -1
    return candidate

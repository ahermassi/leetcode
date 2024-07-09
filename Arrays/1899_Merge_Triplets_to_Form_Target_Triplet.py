""" A triplet is an array of three integers. You are given a 2D integer array triplets, where triplets[i] = [ai, bi, ci]
describes the ith triplet. You are also given an integer array target = [x, y, z] that describes the triplet you want
to obtain.

To obtain target, you may apply the following operation on triplets any number of times (possibly zero):

Choose two indices (0-indexed) i and j (i != j) and update triplets[j] to become [max(ai, aj), max(bi, bj), max(ci, cj)].
For example, if triplets[i] = [2, 5, 3] and triplets[j] = [1, 7, 5], triplets[j] will be updated to
[max(2, 1), max(5, 7), max(3, 5)] = [2, 7, 5].
Return true if it is possible to obtain the target triplet [x, y, z] as an element of triplets, or false otherwise.
 """


# Video explanation: https://www.youtube.com/watch?v=kShkQLQZ9K4
def merge_triplets_v1(triplets, target):
    """ There are 2 key insights that are crucial to solving this problem:

            1- Any triplet with an element larger than the target at that index cannot possibly be combined to form the
                 solution, as any operation wouldn't bring the corresponding element down to target element.
            2- The target's element has to exist in at least one of the remaining candidate triplets for the solution to
                 be possible

        One common pitfall in solving this problem is not properly filtering out triplets that cannot contribute to
        forming the target. A key misunderstanding might be to consider any triplet with at least one matching element
        as a potential contributor. However, ANY element in a triplet that exceeds the corresponding element in the
        target disqualifies the entire triplet, as it can never be part of a valid combination to achieve the target.

        So, the idea is to take as many triplets as possible, but keeping in mind that some of them are forbidden, that
        is if we pick this triplet, then maximum in one of the 3 triplet's elements will be greater that what we need to
        form.

            - Iterate over each of the given triplets and check if all its elements are less than or equal to the
               corresponding elements at the same index in the target.

            - If a triplet's element exceeds the target, it cannot contribute to forming the target triplet.

            - For eligible triplets, check if any (or all) of its elements matches with the corresponding element(s) at
               the same index in the target triplet.

            - The target triplet can be formed if we find matches for all its 3 elements. If we can find all three
               matching numbers, we can combine the corresponding triplets (no more than three needed) to get to the
               target.

        Without an early break, the solution would unnecessarily process all triplets even after finding the match.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    a, b, c = target
    a_found, b_found, c_found = False, False, False
    for x, y, z in triplets:
        if x <= a and y <= b and z <= c:
            if x == a:
                a_found = True
            if y == b:
                b_found = True
            if z == c:
                c_found = True
        if a_found and b_found and c_found:
            return True
    return False


def merge_triplets_v2(triplets, target):
    """ Similarly to the previous approach, we consider only triplets that do not exceed the target in any dimension.
         Then, we greedily apply the "merge" operation using all qualified triplets.

         Keeping track of the maximum values that match the target is not just about finding the target values in the
         triplets but ensuring that these values can co-exist in a way that forms the target triplet, given the
         operation's constraints.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    a = b = c = 0
    for x, y, z in triplets:
        if x <= target[0] and y <= target[1] and z <= target[2]:
            a = max(a, x)
            b = max(b, y)
            c = max(c, z)
        if [a, b, c] == target:
            return True
    return False

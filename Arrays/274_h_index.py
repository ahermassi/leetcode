""" Given an array of integers citations where citations[i] is the number of citations a researcher received for their
ith paper, return the researcher's h-index.

According to the definition of h-index on Wikipedia: The h-index is defined as the maximum value of h such that the
given researcher has published at least h papers that have each been cited at least h times. """


def hIndex_v1(citations):
    """

    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    n = len(citations)
    citations.sort()
    for i, citation in enumerate(citations):
        if citation >= n - i:
            return n - i
    return 0


def hIndex_v2(citations):
    """ Counting Sort.

        The h-index is defined as the number of papers with citations greater than or equal to the number. So assume n
        is the total number of papers, if we have n+1 buckets, numbered from 0 to n, then for any paper with citations
        corresponding to the index of the bucket, we increment the count for that bucket. The only exception is that for
        papers with a number of citations greater than n, we put in the nth bucket.

        Then we iterate from the back to the front of the buckets. Whenever the total count exceeds the index of the
        bucket, it means that we have the index number of papers that have citations greater than or equal to the index.
        This number is the h-index.

        The reason we scan from the end of the array is that we are looking for the largest number. For example, given
        citations = [3,0,6,5,1], we have 6 buckets to contain how many papers have the corresponding index.

        NOTE:
        One difference between Bucket Sort and Counting Sort is:
            - Bucket sort puts objects or keys in buckets. Each bucket may need to be further sorted using other sorting
               algorithms.
            - Counting sort puts the number of occurrences (an integer) in buckets. Buckets don't need further sorting.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    n = len(citations)
    buckets = [0 for _ in range(n + 1)]  # buckets[i] = number of papers with i citations
    for citation in citations:
        if citation >= n:
            # If the number of citations for a paper is >= the maximum possible h-index (i.e. total number of papers),
            # then we know for sure that such maximum h-index is possible, and we have to keep a count of those.
            # Papers with more citations than the number of papers will be counted as though they have
            # number-of-papers citations.
            # Example, citations = [3, 0, 6, 1, 5]. Maximum possible h-index is 5 (i.e. number of papers). We can
            # clearly see that citations with 6 and 5 are >= 5 (maximum possible h-index). So we need to keep
            # incrementing the count of buckets[n=6].
            #
            # Else, we just keep incrementing the count of that citation.
            buckets[n] += 1
        else:
            # Update the count of how many papers have "citation" citations
            buckets[citation] += 1
    count = 0
    for i in reversed(range(len(buckets))):
        # Accumulate the total number of citations up to each index
        count += buckets[i]
        if count >= i:
            # The count of papers with more than i citations is >= i
            return i
    return 0

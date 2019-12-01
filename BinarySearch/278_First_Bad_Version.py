def is_bad_version(version):
    pass


def first_bad_version(n):
    """ Classic binary search. However:
        When is_bad_version(mid) is False, we know that all versions preceding and including mid are all good. So we set
        left = mid + 1 to indicate that the new search space is the interval [mid + 1, right] (inclusive).
        When is_bad_version(mid) is True, mid may or may not be the first bad version, but we can tell for sure that
        all versions after mid can be discarded. Therefore we set right = mid as the new search space of interval
        [left, mid] (inclusive).
        Scenario #1: isBadVersion(mid) => false
        1 2 3 4 5 6 7 8 9
        G G G G G G B B B       G = Good, B = Bad
        |       |       |
        left    mid    right
        Scenario #2: isBadVersion(mid) => true
        1 2 3 4 5 6 7 8 9
        G G G B B B B B B       G = Good, B = Bad
        |       |       |
        left    mid    right
        Note that binary search can be used because if we model the problem as an array [good, good, good, bad, bad]
        where 'good' means is_bad_version(arr[i]) == False and 'bad' means is_bad_version(arr[i]) == True, the array is
        sorted. (every version after a bad version is bad)
    Time complexity: O(log n), the search space is halved each time
    Space complexity: O(1)
    """
    left, right = 1, n
    while left < right:
        mid = (left + right) // 2
        if not is_bad_version(mid):
            left = mid + 1
        else:
            right = mid
    return left

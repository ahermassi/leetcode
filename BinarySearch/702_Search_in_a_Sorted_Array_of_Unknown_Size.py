""" Given an integer array sorted in ascending order, write a function to search target in nums.  If target exists,
then return its index, otherwise return -1. However, the array size is unknown to you. You may only access the array
using an ArrayReader interface, where ArrayReader.get(k) returns the element of the array at index k (0-indexed).
You may assume all integers in the array are less than 10000, and if you access the array out of bounds,
ArrayReader.get will return 2147483647. """


def search_v1(reader, target):
    """ The array is sorted, i.e. we could try to fit into a logarithmic time complexity. That means two sub-problems,
        and both should be done in a logarithmic time:
            - Define search limits, i.e. left and right boundaries for the search
            - Perform binary search in the defined boundaries
        To define search boundaries, the idea is quite simple. Let's take two first indices, 0 and 1, as left and right
        boundaries. If the target value is not among these zeroth and the first element, then it's outside the
        boundaries, on the right. That means that the left boundary could moved to the right, and the right boundary
        should be extended. To keep logarithmic time complexity, let's extend it twice as far: right = right * 2.
        If the target now is less than the right element, we're done, the boundaries are set. If not, repeat these two
        steps till the boundaries are established.
    Time complexity: O(logT), where TT is the index of target value
    Space complexity: O(1)
    """
    left, right = 0, 1
    while reader.get(right) < target:
        left, right = right, right * 2
    while left <= right:
        mid = (left + right) // 2
        if reader.get(mid) == target:
            return mid
        if reader.get(mid) < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

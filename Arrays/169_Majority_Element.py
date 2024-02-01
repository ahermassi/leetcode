""" Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊
n/2 ⌋ times.
You may assume that the array is non-empty and the majority element always exist in the array. """

from collections import defaultdict

import unittest2 as unittest


def majority_element_v1(nums):
    """ We know that the majority element occurs more than ⌊N/2⌋ times, and a hashmap allows us to count element
         occurrences efficiently.

    Time complexity: O(N/2) in the best case where all instances of the majority element appear at the beginning of
    the input, and O(N) in the worst case
    Space complexity: O(N), at most the hashmap can contain N−⌊N/2⌋ associations, so it occupies O(N) space. This is
    because an arbitrary array of length N can contain N distinct values, but nums is guaranteed to contain a majority
    element, which will occupy (at minimum) ⌊N/2⌋+1 array indices.
    """
    n, counter = len(nums), defaultdict(int)
    for num in nums:
        counter[num] += 1
        if counter[num] > n // 2:
            return num


def majority_element_v2(nums):
    """ If the elements are sorted in monotonically increasing (or decreasing) order, the majority element can be found
         at index ⌊N/2⌋. In other words, if the array was rearranged such that all the occurrences of the majority
         element were put together, this sequence of occurrences will occupy more than half of the array's size, and so
         the ⌊N/2⌋th element will always be the majority element.

    Time complexity: O(N logN), for sorting
    Space complexity: O(N), for sorting
    """
    nums.sort()
    return nums[len(nums) // 2]


# Video explanation: https://youtu.be/7pnhv842keE
def majority_element_v3(nums):
    """ Boyer-Moore voting algorithm.

         If we had some way of counting instances of the majority element as +1 and instances of any other element
         as −1, summing them would make it obvious that the majority element is indeed the majority element.

         Essentially, what Boyer-Moore does is look for a suffix of nums where suf[0] is the majority element in that
         suffix. To do this, we maintain a count, which is incremented whenever we see an instance of the current
         candidate for majority element and decremented whenever we see anything else. Whenever the count drops to 0, we
         effectively forget about everything in nums up to the current index and consider the current number as the
         candidate for majority element.

         It is not immediately obvious why we can get away with forgetting prefixes of nums - consider the following
         examples (pipes are inserted to separate runs of non-zero count):

         Example 1: [7, 7, 5, 7, 5, 1 | 5, 7 | 5, 5, 7, 7 | 7, 7, 7, 7]

         Here, the 7 at index 0 is selected to be the first candidate for majority element. count will eventually reach
         0 after index 5 is processed, so the 5 at index 6 will be the next candidate. In this case, 7 is the true
         majority element, so by disregarding this prefix, we are ignoring an equal number of majority and minority
         elements - therefore, 7 will still be the majority element in the suffix formed by throwing away the first
         prefix.

         Example 2: [7, 7, 5, 7, 5, 1 | 5, 7 | 5, 5, 7, 7 | 5, 5, 5, 5]

         Now, the majority element is 5 (we changed the last run of the array from 7s to 5s), but the first candidate is
         still 7. In this case, the candidate is not the true majority element, but we still cannot discard more
         majority elements than minority elements (this would imply that count could reach -1 before we reassign
         a candidate, which is obviously false).

         Therefore, given that it is impossible (in both cases) to discard more majority elements than minority
         elements, we are safe in discarding the prefix and attempting to solve the majority element problem for the
         suffix. Eventually, a suffix will be found for which count does not hit 0, and the majority element of that
         suffix will necessarily be the same as the majority element of the overall array.

         The intuition is that we can group entries into two subgroups: Those containing the majority element, and those
         that do not hold the majority element. Since the first subgroup is given to be larger in size than the second,
         if we see two entries that are different, at most one can be the majority element. By discarding both, the
         difference in size of the first subgroup and second subgroup remains the same, so the majority of the
         remaining entries remains unchanged.

         Looking at the idea of this algorithm, it first assumes candidates and then performs verification. There is a
         strong assumption that there must be a number with more than half of the count. This assumption guarantees that
         even if the count is reset to 0 by other elements, the majority element will eventually regain the lead.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    count, candidate = 0, None
    for num in nums:
        if count == 0:
            candidate = num
        if num == candidate:
            count += 1
        else:
            count -= 1
    return candidate


class Test(unittest.TestCase):
    data = [([3, 2, 3], 3), ([2, 2, 1, 1, 1, 2, 2], 2)]

    def test_majority_element(self):
        for test_array, result in self.data:
            self.assertEqual(result, majority_element_v1(test_array))
            self.assertEqual(result, majority_element_v2(test_array))
            self.assertEqual(result, majority_element_v3(test_array))


if __name__ == '__main__':
    unittest.main()

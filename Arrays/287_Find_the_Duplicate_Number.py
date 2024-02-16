""" Given an array nums containing n + 1 integers where each integer is between 1 and n (inclusive), prove that at
least one duplicate number must exist. Assume that there is only one duplicate number, find the duplicate one. """

import unittest2 as unittest

# Proving that at least one duplicate must exist in nums is an application of the pigeonhole principle. Here,
# each number in nums is a "pigeon" and each distinct number that can appear in nums is a "pigeonhole." Because there
# are n+1 numbers and n distinct possible numbers, the pigeonhole principle implies that if you were to put each of
# the n +  pigeons into nn pigeonholes, at least one of the pigeonholes would have 2 or more pigeons.


def find_duplicate_v1(nums):
    """ In an unsorted array, duplicate elements may be scattered across the array. However, in a sorted array,
         duplicate numbers will be next to each other.

         This approach modifies individual elements and does not use constant space, and hence does not meet the problem
         constraints. However, it utilizes a fundamental concept that can help solve similar problems.

    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    nums.sort()
    n = len(nums)
    for i in range(1, n):
        if nums[i] == nums[i - 1]:
            return nums[i]


def find_duplicate_v2(nums):
    """ As we traverse the array, we need a way to "remember" values that we've seen. If we come across a number that
         we've seen before, we've found the duplicate.

         In order to achieve linear time complexity, we need to be able to insert elements into a data structure and
         look them up in constant time. An efficient way to record the seen values is by adding each number to a set as
         we iterate over the nums array.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)


def find_duplicate_v3(nums):
    """ Negative Marking

         This approach temporarily modifies individual elements and thus does not satisfy the problem constraints.
         However, this approach is intuitive and utilizes a technique that is useful to know. Furthermore, the
         underlying concept lends itself to solving similar problems. As such, we can further practice this technique on
         other problems such as 41- First Missing Positive.

         There are (n + 1) positive integers in the array, all in the range [1, n]. Since the array contains only
         positive integers, we can track each number num that has been seen before by flipping the sign of the number
         located at index |num|, where || denotes absolute value.

         For example, if the input array is [1, 3, 3, 2], then for 1 flip the number at index 1, making the array
         [1, -3, 3, 2]. Next, for -3 flip the number at index 3, making the array [1,-3, 3, -2]. Finally, when we reach
         the second 3, we'll notice that nums[3] is already negative, indicating that 3 has been seen before and hence
         is the duplicate number.

            - Iterate over the array, evaluating each number. Let's call the current number cur.

            - Since we use negative marking, we must ensure that cur is positive (i.e. if cur is negative, then use its
               absolute value).

            - Check if nums[cur] is negative.
               If it is, then we have already performed this operation for the same number, and hence cur is the
               duplicate number.
               Otherwise, flip the sign of nums[cur] (i.e. make it negative). Move to the next element and repeat.

         Once we've identified the duplicate, we could just return it. However, even though we were not able to meet the
         problem constraints, we can show that we are mindful of the constraints by restoring the array. This is done
         by changing all negative numbers to positive (not done here).

    Time complexity: O(N)
    Space complexity: O(1)
    """
    for num in nums:
        val = abs(num)
        if nums[val] < 0:
            return val
        nums[val] = -nums[val]

# Video explanation: https://www.youtube.com/watch?v=wjYnzkAhcNk


def find_duplicate_v4(nums):
    """ Floyd's Tortoise and Hare (Cycle Detection)

        The idea is to reduce the problem to 142- Linked List Cycle II:

                Given a linked list, return the node where the cycle begins.

        First, where does the cycle come from? Let's use the function f(x) = nums[x] to construct the sequence:
        x, nums[x], nums[nums[x]], nums[nums[nums[x]]], ....
        Each new element in the sequence is an element in nums at an index equal to the value of the previous element.

        If we start from x = 0, such a sequence will produce a linked list with a cycle. The cycle appears because nums
        contains duplicates. The duplicate node is a cycle entrance.

        Now the problem is to find the entrance of the cycle.

        Floyd's algorithm consists of two phases and uses two pointers, usually called tortoise and hare.

        In phase 1, hare = nums[nums[hare]] is twice as fast as tortoise = nums[tortoise]. Since the hare goes fast,
        it would be the first to enter the cycle and run around the cycle. At some point, the tortoise enters the cycle
        as well, and since it's moving slower the hare catches up to the tortoise at some intersection point.
        Note that the intersection point is not the cycle entrance in the general case.

        In phase 2, we give the tortoise a second chance by slowing down the hare, so that it now moves at the speed of
        tortoise: tortoise = nums[tortoise], hare = nums[hare]. The tortoise is back at the starting position, and the
        hare starts from the intersection point.
        The tortoise and the (slowed down) hare will meet at the entrance of the cycle. Full proof is at
        142- Linked List Cycle II.

        The intuition here is that:

        Because each number in nums is in the range [1, n] and nums has (n + 1) numbers which means indices are in the
        range [0, n], then each number will necessarily point to an index that exists. Therefore, the list can be
        traversed infinitely, which implies that there is a cycle. Why? By contradiction. If we cannot reach a cycle,
        that is to say, we always meet a new index, and then meet a new index, but there is only a finite number of
        indices. So, we will reach a cycle.

        Additionally, because 0 cannot appear as a value in nums, nums[0] cannot be part of the cycle because there is
        no value in nums that can take BACK to 0. Therefore, traversing the array in this manner from nums[0] is
        equivalent to traversing a cyclic linked list: nums[a] = b can be seen as a.next = b

        As there is always a duplicate number in nums, nums[i] will always be a valid index in nums.
        This guarantees that at least one cycle will exist. If there was not a duplicate in nums then nums[i] would
        eventually equate to an out-of-range index. nums[0] is not reachable from any nums[i] which means that if
        another cycle exists other than the one containing the duplicate number, it will not contain nums[0].
        All of this means that if we begin at nums[0] we will eventually enter the cycle containing the duplicate number.

        If there is no duplicate in the array, we can map each index to each number in this array. In other words, we
        can have a mapping function f(index) = number.
        For example, let's assume nums = [2,1,3], then the mapping function is 0->2, 1->1, 2->3: 3 numbers in the
        range [1, 3].
        If we start from index = 0, we can get a value according to this mapping function, and then we use this value
        as a new index and, again, we can get the other new value according to this new index. We repeat this process
        until the index exceeds the array. Actually, by doing so, we can get a sequence. Using the above example again,
        the sequence we get is 0->2->3. Because index=3 exceeds the array's size, the sequence terminates!

        However, if there is duplicate in the array, the mapping function is many-to-one.
        For example, let's assume nums = [2,1,3,1] (4 numbers in the range [1, 3]), then the mapping function is
        0->2, {1,3}->1, 2->3. Then the sequence we get definitely has a cycle: 0->2->3->1->1->1->1->1->........
        The starting point of this cycle is the duplicate number.

        Note: We need second loop because in first loop both pointers might end up at the same index and hence we will
        get a number which might not be a duplicate. The first loop just gives us the intersection of the indices,
        while the second loop returns the index of the duplicate number.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    tortoise = hare = nums[0]  # tortoise = hare = 0 is also correct
    while True:
        tortoise, hare = nums[tortoise], nums[nums[hare]]
        if tortoise == hare:
            break
    # Find the entrance to the cycle
    tortoise = nums[0]  # tortoise = 0 is also correct
    while tortoise != hare:
        tortoise, hare = nums[tortoise], nums[hare]
    return tortoise


def find_duplicate_v5(nums):
    """ Binary search based on pigeonhole principle.

        Originally, there are (n + 1) objects and n holes. This condition complies to pigeonhole principle, so at least
        one hole has two objects, that is one number appears twice.

        Consider an array that has n distinct numbers in the range [1,n]. For example: [1,2,3,4,5]. If we pick any one
        of these 5 numbers and count how many numbers are less than or equal to it, the answer will be equal to that
        number. So in [1,2,3,4,5], if we pick the number 4, there's exactly 4 numbers that are less than or equal to 4.
        If we pick 3, there's exactly 3 numbers that are less than or equal to 3, and so on.

        However, when we have duplicates in the array, this count will exceed the number at some point.
        For example, in [4,3,4,5,2,4,1], 3 has 3 numbers less than or equal to it. But, the duplicate number will
        have a count of numbers less than or equal to itself, that is greater than itself. In this example, 4, which is
        the duplicate, has 6 numbers that are less than or equal to it. Hence, the smallest number that satisfies
        this property is the duplicate number.

        Consider an example: [4,6,4,2,1,4,3,5]. This has (n + 1) elements in the range [1, n], where n = 7.
        Take each number from 1 to 7 and count how many numbers are less than or equal to it. In our example,
        count_less_than_or_equal(1,2,3,4,5,6,7) = (1,2,3,6,7,8,8). If we performed a linear scan, we would find that
        the number 4 is the first number to have its count exceed the actual number (i.e. 6 > 4) - hence 4 is the duplicate.

        A linear scan based approach would require an overall O(n^2) time complexity in the worst case, since we'd need
        to iterate over each of the n numbers and then compare it to every element to generate a count of equal or lower
        numbers. Fortunately, count_less_than_or_equal() is monotonic (its values are always in non-decreasing order),
        and hence it is an excellent candidate for binary search.

        In the binary search approach, instead of doing a linear scan from 1 to n, we can apply a binary search with a
        goal of finding the smallest number that satisfies the aforementioned property.

        Each time we select a number 'mid' (which is the one in the middle), we count all the numbers equal to or less
        than 'mid'. Then, if the count is more than 'mid', the search space will be [1 .. mid] otherwise [mid+1 .. n].
        We do this until search space is only one number.

        Or less formally:

        We know that the whole range is 'too crowded' and thus that the first half or the second half of the range is
        too crowded (if both weren't, then neither would be the whole range). So we check to know whether the first
        half is too crowded, and if it isn't, we know that the second half is.

        Note that although the numbers in nums are not ordered, their RANGE OF POSSIBLE VALUES is still ordered.
        That's why binary search can still be used.

        Note:
        To observe the monotonicity of count_less_than_or_equal(), consider the evaluation: "For a given number,
        the count of numbers less than or equal to it exceeds the number itself". Going back to our example, we had
        derived: count_less_than_or_equal(1,2,3,4,5,6,7) = (1,2,3,6,7,8,8).
        If we now take the first number and apply said evaluation, we get false (since count_less_than_or_equal(1) == 1,
        which is not greater than 1).
        Applying this evaluation to all counts, we get (false, false, false, true, true, true, true). Observe how this
        remains false in the beginning, and switches to true starting from number 4 (i.e. the duplicate), after which
        point it remains true for all further numbers. It's for this reason that binary search is applicable: We try to
        locate the first number that makes one of the halves 'crowded'.

        Formally, the count for each number must include itself plus the count of all numbers less than itself. Since
        a number cannot have a negative count, each number N must have a count greater than or equal to the count
        of N-1. Since count_less_than_or_equal(N) >= count_less_than_or_equal(N-1), count_less_than_or_equal() must be
        monotonically increasing.

        Example: nums = [2, 6, 4, 1, 3, 1, 5]

        left = 1, right = 6 --> mid = 3, count = 4: There is 4 strictly positive integers less than or equal to 3
        --> The duplicate has to be between left and 3

        left = 1, right = 3 --> mid = 2, count = 3: There is 3 strictly positive integers less than or equal to 2
        --> The duplicate has to be between left and 2

        left = 1, right = 2 --> mid = 1, count = 2: There is 2 strictly positive integers less than or equal to 1
        --> The duplicate has to be between left and 1

        left = 1, right = 1: exit and return 1.

    Time complexity: O(N logN), the outer loop uses binary search to identify a candidate - this runs in O(log N)
    time. For each candidate, we iterate over the entire array which takes O(N) time
    Space complexity: O(1)
    """
    left, right = 1, len(nums) - 1  # We use binary search on the range of possible NUMBERS, so left starts from 1 not 0
    while left < right:
        mid = (left + right) // 2
        count = sum(num <= mid for num in nums)
        if count <= mid:
            left = mid + 1
        else:
            right = mid
    return left


class Test(unittest.TestCase):
    data = [([1, 3, 4, 2, 2], 2), ([3, 1, 3, 4, 2], 3)]

    def test_find_duplicate(self):
        for test_array, result in self.data:
            self.assertEqual(result, find_duplicate_v1(test_array))
            self.assertEqual(result, find_duplicate_v2(test_array))
            self.assertEqual(result, find_duplicate_v3(test_array))


if __name__ == '__main__':
    unittest.main()

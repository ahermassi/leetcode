""" Given an array consists of non-negative integers, your task is to count the number of triplets chosen from the
array that can make triangles if we take them as side lengths of a triangle. """

import unittest2 as unittest


def triangle_number(nums):
    """ The condition for the triplets (a, b, c), representing the lengths of the sides of a triangle, to form a valid
        triangle is that the sum of any two sides should always be greater than the third side alone. i.e. a + b > c,
        b + c > a, a + c > b.
        The simplest method to check this is to consider every possible triplet in the given array and checking if the
        triplet satisfies the three inequalities mentioned above.
        If we sort the given array, we can solve the given problem in a better way. This is because, if we consider a
        triplet (a, b, c)such that a ≤ b ≤ c, we need not check all the three inequalities for checking the validity of
        the triangle formed by them. But, only one condition a + b > c would suffice. This happens because c ≥ b and
        c ≥ a. Thus, adding any number to c will always produce a sum which is greater than either a or b considered
        alone. Thus, the inequalities a + c > b and b + c > a are satisfied implicitly by virtue of the property
        a < b < c.
        After that, we can use three pointers (i, j, k and i < j < k) to solve the problem, similarly to 3Sum. The way
        we do in 3Sum is that we first fix pointer i and then scan j and k. If nums[j] + nums[k] is too large, k--,
        otherwise j++. Once we complete the scan, we increase pointer i and repeat.
        For this problem, once we sort the input array, the key is that given nums[k], we count the combination of i
        and j where nums[i] + nums[j] > nums[k] (so that they can form a triangle). If nums[i] + nums[j] is larger than
        nums[k], we know that there will be (j - i) combinations.
        Let's take the following array for example:
         i                  j   k
        [3, 19, 22, 24, 35, 82, 84]
        Because 3 + 82 > 84 and the numbers between 3 and 82 are always larger than 3, we can quickly tell that there
        will be (j - i) combinations which can form the triangle, and they are:
        3,  82, 84
        19, 82, 84
        22, 82, 84
        24, 82, 84
        35, 82, 84
        Now let's fix k again and point to 35:
         i          j   k
        [3, 19, 22, 24, 35, 82, 84]
        Because 3 + 24 < 35, if we move j to the left, the sum will become even smaller, so we have to move pointer i
        to the next number 19, and now we find that 19 + 24 > 35, and we don't need to scan 22, we know that 22 must
        be valid!
    Time complexity: O(N^2)
    Space complexity: O(N), for the sort
    """
    nums.sort()
    n, res = len(nums), 0
    for k in reversed(range(n)):
        i, j = 0, k - 1
        while i < j:
            if nums[i] + nums[j] > nums[k]:
                res += j - i
                j -= 1
            else:
                i += 1
    return res


class Test(unittest.TestCase):
    data = [([2, 2, 3, 4], 3)]

    def test_triangle_number(self):
        for test_nums, result in self.data:
            self.assertEqual(result, triangle_number(test_nums))


if __name__ == '__main__':
    unittest.main()

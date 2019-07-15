from collections import Counter

import unittest2 as unittest

""" Given two arrays arr1 and arr2, the elements of arr2 are distinct, and all elements in arr2 are also in arr1.
Sort the elements of arr1 such that the relative ordering of items in arr1 are the same as in arr2.  Elements that 
don't appear in arr2 should be placed at the end of arr1 in ascending order. """


def relative_sort_array_v1(arr1, arr2):
    arr1.sort()
    result = []
    for i in range(len(arr2)):
        for j in range(len(arr1)):
            if arr1[j] == arr2[i]:
                result.append(arr2[i])
    for j in range(len(arr1)):
        if arr1[j] not in arr2:
            result.append(arr1[j])
    return list(result)


def relative_sort_array_v2(arr1, arr2):
    result = []
    counter = Counter(arr1)  # Count the occurrence of each number
    for i in arr2:
        if counter[i]:
            result.extend([i] * counter.pop(i))  # Extend the list by that number * its occurrence, and then pop it
    for i in range(1001):  # 0 <= arr1[i] <= 1000 as per problem requirements; this loop guarantees increasing order
        # of remaining numbers
        if counter[i]:
            result.extend([i] * counter.pop(i))
    return result


class Test(unittest.TestCase):
    data = [[2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]]

    def test_relative_sort_array(self):
        self.assertEqual([2, 2, 2, 1, 4, 3, 3, 9, 6, 7, 19], relative_sort_array_v2(self.data[0], self.data[1]))


if __name__ == '__main__':
    unittest.main()

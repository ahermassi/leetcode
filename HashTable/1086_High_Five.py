""" Given a list of scores of different students, return the average score of each student's top five scores in the
order of each student's id. """

import unittest2 as unittest


def high_five(items):
    """ Use a set to store the distinct students ids. Pretty straightforward calculations.
    Time complexity: O(N log N). First for loop is O(N); second for loop runs for O(1000) as the IDs of the students are
    between 1 and 1000 (constant time) followed by O(N) operation (scores list) and O(N log N) operation (Timsort).
    Space complexity: O(N)
    """
    students_ids, result = set(), []
    for l in items:
        students_ids.add(l[0])
    for student_id in students_ids:
        scores = [l[1] for l in items if l[0] == student_id]
        scores.sort()
        top_five = scores[-5:]
        average = sum(top_five) // 5
        result.append([student_id, average])
    return result


class Test(unittest.TestCase):
    data = [([[1, 91], [1, 92], [2, 93], [2, 97], [1, 60], [2, 77], [1, 65], [1, 87], [1, 100], [2, 100], [2, 76]],
             [[1, 87], [2, 88]])]

    def test_high_five(self):
        for test_array, result in self.data:
            self.assertEqual(result, high_five(test_array))


if __name__ == '__main__':
    unittest.main()

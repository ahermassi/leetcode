""" Some people will make friend requests. The list of their ages is given and ages[i] is the age of the ith person.
Person A will NOT friend request person B (B != A) if any of the following conditions are true:
age[B] <= 0.5 * age[A] + 7
age[B] > age[A]
age[B] > 100 && age[A] < 100
Otherwise, A will friend request B.
Note that if A requests B, B does not necessarily request A.  Also, people will not friend request themselves.
How many total friend requests are made? """

from collections import Counter
import unittest2 as unittest


def num_friend_requests_v1(ages):
    """ Instead of processing all 20000 people, we can process pairs of (age, count) representing how many people are
        that age. Since there are only 120 possible ages, this is a much faster loop.
        For each pair (age_a, count_a), (age_b, count_b), if the conditions are satisfied with respect to age, then
        count_a * count_b friend requests are made from people of age age_a to people with age age_b.
        If age_a == age_a, then we over counted: we should have count_a * (count_a - 1) pairs of people making friend
        requests instead, as we cannot friend request ourselves.
        Note that the three rules could be merged into one:
            The Person with age age_a can request person with age age_b if: age_b is in range ( 0.5 * A + 7, A ]
        age_b > 100 and age_a < 100 is redundant as the condition is already covered by the second rule.
    Time complexity: O(N + A^2), where  is the number of people and A is the number of ages
    Space complexity: O(A)
    """
    counter = Counter(ages)
    res = 0
    for age_a, counter_a in counter.items():
        for age_b, counter_b in counter.items():
            if 0.5 * age_a + 7 < age_b <= age_a:
                res += counter_a * (counter_b - (age_a == age_b))
    return res


class Test(unittest.TestCase):
    data = [([16, 16], 2), ([16, 17, 18], 2), ([20, 30, 100, 110, 120], 3)]

    def test_num_friend_requests(self):
        for test_ages, result in self.data:
            self.assertEqual(result, num_friend_requests_v1(test_ages))


if __name__ == '__main__':
    unittest.main()

""" Suppose you have a random list of people standing in a queue. Each person is described by a pair of integers (h, k),
where h is the height of the person and k is the number of people in front of this person who have a height greater
than or equal to h. Write an algorithm to reconstruct the queue. """

import unittest2 as unittest


def reconstruct_queue(people):
    """ Let's start from the simplest case, when all guys (h, k) in the queue are of the same height h, and differ by
        their k values only (the number of people in front who have a greater or the same height). Then the solution
        is simple: each guy's index is equal to his k value. The guy with zero people in front takes the place number 0,
        the guy with 1 person in front takes the place number 1, and so on and so forth.
        Let's now consider a queue with people of two different heights: 7 and 6. For simplicity, let's have just one
        6-height guy. First follow the strategy above and arrange guys of height 7. Now it's time to find a place for
        the guy of height 6. Since he is 'invisible' for the 7-height guys, he could take whatever place without
        disturbing 7-height guys order. However, for him the others are visible, and hence he should take the position
        equal to his k-value, in order to have his proper place.
        This idea is easy to extend for the case of numerous guys of height 6. Just sort them by k-values, as it was
        done before for 7-height guys, and insert them one by one in the positions equal to their k-values.
        The following strategy could be continued recursively:
            - Sort the tallest guys in the ascending order by k-values and then insert them one by one into output
              queue at the indexes equal to their k-values.
            - Take the next height in the descending order. Sort the guys of that height in the ascending order by
              k-values and then insert them one by one into output queue at the indexes equal to their k-values.
            - And so on and so forth.
        k is only determined by people with equal or larger height, so it makes sense to insert in non-increasing order
        of height. Because when we insert some person with height h and count k, we know that we have found its correct
        position RELATIVE TO people with equal and larger height. When we later insert other people with equal or
        smaller height, we know that it will not affect this relative position. So the answer is right after we insert
        all people.
        Suppose we take only the tallest persons, all having the same maximum height. Their second values must be 0, 1,
        2, 3... with no gaps at all, because they only count each other. Therefore, if there were no other persons at
        all, their second value must be their final index. What about the persons with second maximum height then?
        Suppose there are only tallest persons and just one more person who has slightly smaller height. What would be
        his position? Well, since he obviously only count tallest persons, his position would still be his second value.
        The next person of the same height counts only the previous person and all the tallest ones, but since they are
        all already in the queue, his second value would also be his index.
        We could go on forever like that because each time we put a person in the queue and go to the next person, all
        persons counted by the next one are already there, so we instantly know the right index and we know that the
        person we put in the queue doesn't really care about where we put all subsequent persons because they are
        outside of his selection criteria.
        Example: people = [[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]
        First, we sort it: people = [[7,0], [7,1], [6,1], [5,0], [5,2], [4,4]].
        After that, we iterate over it and copy each element into 'res'.
        1st element: We insert [7,0] at 0 in 'res': [[7,0]]
        2nd element: We insert [7,1] at 1 in 'res': [[7,0], [7,1]]
        3rd element: We insert [6,1] at 1 in 'res': [[7,0], [6,1], [7,1]]
        (Notice how it moved all elements at index 1 or greater to the right 1)
        4th element: We insert [5,0] at 0 in 'res': [[5,0], [7,0], [6,1], [7,1]]
        (Notice how, although we have inserted another element in front of [6,1], the new element is not taller or the
        same height so it doesn't matter)
        5th element: We insert [5,2] at 2 in 'res': [[5,0], [7,0], [5,2], [6,1], [7,1]]
        6th element: We insert [4,4] at 4 in 'res': [[5,0], [7,0], [5,2], [6,1], [4,4], [7,1]]
    Time complexity: O(N logN + N^2) = O(N^2)
    Space complexity: O(N), for the sort
    """
    people.sort(key=lambda x: (-x[0], x[1]))
    res = []
    for height, k in people:
        res.insert(k, [height, k])
    return res


class Test(unittest.TestCase):
    data = [([[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]], [[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]])]

    def test_reconstruct_queue(self):
        for test_people, result in self.data:
            self.assertEqual(result, reconstruct_queue(test_people))


if __name__ == '__main__':
    unittest.main()

""" Given an array w of positive integers, where w[i] describes the weight of index i, write a function pickIndex
which randomly picks an index in proportion to its weight. """


from random import randint


class Solution(object):
    """ To understand the problem better, let us imagine that there is a line in the space, we then project each index
        into the line according to its weight, i.e. an index with a large weight would occupy a broader range on the
        line compared to a small weight.
        Now, let us throw a ball randomly onto the line, then it is safe to say there is a good chance that the ball
        will fall into the range occupied by the index with the highest weight.
        To throw a ball on the line is to find an offset to place the ball. Let us call this offset target.
        Once we randomly generate the target offset, the task is now boiled down to finding the range that this target
        falls into.
        Let us rephrase the problem now. Given a list of offsets (i.e. prefix sums) and a target offset, our task is
        to fit the target offset into the list so that the ascending order is maintained.
        The intuition behind this solution is the following:
        If we have an array [a, b, c], then we can visualize this same array as: ([0] * a) + ([1] * b) + ([2] * c),
        where 0, 1, 2 are the indices of the array. That's how the weights a, b, c affect the random choice of an index:
            The probability of randomly picking index 0 is a / (a + b + c)
            The probability of randomly picking index 1 is b / (a + b + c)
            The probability of randomly picking index 2 is c / (a + b + c)
        We use the prefix sum array to get the index.
        Example: w = [2, 5, 3, 4] => prefix_sum_array = [2, 7, 10, 14]
        index:      0   1    2     3
                  [  |     |   |        ]
        prefix    1  2     7   10       14
        [1, 2) region belongs to index 0, [3,7) region belongs to 1 ... etc. As we can see, the size of region that
        each index get is proportional to its weight.
        The prefix sum array [2, 7, 10, 14] can also be interpreted this way:
            First 2 elements belong to index 0
            Elements after 2nd and up to and including 7th belong to index 1
            Elements after 7th and up to and including 10th belong to index 2
            Elements after 10th and up to and including 14th belong to index 3
        Then we get a random value 'rand' in range [1, 14], and use binary search to determine which region it falls
        in so that we can tell that the "owner" of that region is the index we want to return.
            rand in [1, 2] --> return 0, with probability 2 / 14
            rand in [3, 7] --> return 1, with probability 5 / 14
            rand in [8, 10] --> return 2, with probability 3 / 14
            rand in [11, 14] --> return 3, with probability 4 / 14
    Time complexity: O(N) pre-processing, O(logN) for pick_index
    Space complexity: O(N)
    """

    def __init__(self, w):
        self.weights = w
        n = len(w)
        for i in range(1, n):
            self.weights[i] += self.weights[i - 1]

    def pick_index(self):
        """ Note that mapping the possible range of indices to [1, w[-1]] is like using bisect_left, while mapping the
            range to [0, w[-1] - 1] is like using bisect_right.
        """
        weights = self.weights
        rand = randint(1, weights[-1])
        left, right = 0, len(weights) - 1
        while left < right:
            mid = (left + right) // 2
            if rand > weights[mid]:
                left = mid + 1
            else:
                right = mid
        return left


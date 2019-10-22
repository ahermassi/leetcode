""" Given an array w of positive integers, where w[i] describes the weight of index i, write a function pickIndex
which randomly picks an index in proportion to its weight. """


from random import randint


class Solution(object):
    """ The intuition behind this solution is the following:
        If we have an array [a, b, c], then we can imagine this same array as: ([0] * a) + ([1] * b) + ([2] * c), where
        0, 1, 2 are the indices of the array. That's how the weights a, b, c affect the random choice of an index:
            The probability of randomly picking index 0 is a / (a + b + c)
            The probability of randomly picking index 1 is b / (a + b + c)
            The probability of randomly picking index 2 is c / (a + b + c)
        We use the prefix sum array to get the index.
        Example: w[] = [2,5,3,4] => prefix_sum_array = [2,7,10,14]
        index:      0   1    2     3
                  [  |     |   |        ]
        prefix    1  2     7   10       14
        [1, 2) region belongs to index 0, [3,7) region belong to 1 ... etc. As we can see, the size of region that
        each index get is proportional to its weight.
        Then we get a random value 'rand' in range [1,14], and use binary search to determine which region it falls
        upon so that we can tell that the "owner" of that region is the index we want to return.
            rand in [1,2] --> return 0, with probability 2 / 14
            rand in [3,7] --> return 1, with probability 5 / 14
            rand in [8,10] --> return 2, with probability 3 / 14
            rand in [11,14] --> return 3, with probability 4 / 14
    Time complexity: O(N) pre-processing, O(log N) for pick_index
    Space complexity: O(N)
    """

    def __init__(self, w):
        """
        :type w: List[int]
        """
        self.w = w
        for i in range(1, len(self.w)):
            self.w[i] += self.w[i - 1]
        self.total = self.w[-1]

    def pick_index(self):
        """
        :rtype: int
        """
        w = self.w
        rand = randint(1, self.total)
        left, right = 0, len(w) - 1
        while left < right:
            mid = (left + right) // 2
            if w[mid] >= rand:
                right = mid
            else:
                left = mid + 1
        return left


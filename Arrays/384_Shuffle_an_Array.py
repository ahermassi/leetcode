""" Shuffle a set of numbers without duplicates. """

from random import randint


class SolutionV1:
    """ Fisher-Yates algorithm, original method.
        If we put each number in a 'hat' and draw them out at random, the order in which we draw them will define a
        random ordering.
        The algorithm essentially puts each number in the aforementioned 'hat', and draws them at random (without
        replacement) until there are none left. Mechanically, this is performed by copying the contents of array into
        a second auxiliary array 'aux' before overwriting each element of array with a randomly selected one from 'aux'.
        After selecting each random element, it is removed from 'aux' to prevent duplicate draws. The implementation
        of reset is simple, as we just store the original state of nums on construction.
        The correctness of the algorithm follows from the fact that an element (without loss of generality) is equally
        likely to be selected during all iterations of the for loop.
        To prove this, observe that the probability of a particular element e being chosen on the kth iteration
        (indexed from 0) is simply:
            P = P(e being chosen during the kth iteration) * P(e not being chosen before the kth iteration)
        At kth iteration, there are (n - k) elements in the array (k is 0-indexed). Therefore:
            P(e being chosen during the kth iteration) = 1 / (n - k)
        Moreover:
            P(e not being chosen before the kth iteration) = product(P(e not being chosen in ith iteration)), i = 0..k-1
        Now to find the formula of P(e not being chosen in ith iteration), we use:
            P(e not being chosen in ith iteration) = 1 - P(e being chosen in ith iteration)
        So for i = 0..k-1:
            P(e being chosen in ith iteration) = 1 - 1/(n - i) = (n - i - 1)/(n - i)
        Therefore:
            P(e not being chosen before the kth iteration) = product(i = 0..k-1) {(n - i + 1)/(n - i)}
        Which can be written:
            P(e not being chosen before the kth iteration) = product(i = 1..k) {(n - i)/(n - i + 1)}
        Finally:
            P = P(e being chosen during the kth iteration) * P(e not being chosen before the kth iteration)
              = (1 / (n - k)) * product(i = 1..k) {(n - i)/(n - i + 1)}
        When expanded (and rearranged), the numerator of each fraction can be cancelled with the denominator of the
        next, leaving the n from the 0th draw as the only uncancelled denominator. Therefore, no matter on which draw
        an element is drawn, it is drawn with a 1/n chance, so each array permutation is equally likely to arise.
    """

    def __init__(self, nums):
        self.nums = nums
        self.original = nums[:]

    def reset(self):
        """ Resets the array to its original configuration and returns it.
        Time complexity: O(N)
        Space complexity: O(N)
        """
        self.nums = self.original[:]
        return self.nums

    def shuffle(self):
        """ Returns a random shuffling of the array.
        Time complexity: O(N)
        Space complexity: O(N), we must use linear additional space to store the original array
        """
        aux = self.nums[:]
        n = len(self.nums)
        for i in range(n):
            random_index = randint(0, len(aux) - 1)
            self.nums[i] = aux[random_index]
            # Delete from aux in constant time
            aux[random_index] = aux[-1]
            aux.pop()
        return self.nums
""" Given two sparse vectors, compute their dot product.

Implement class SparseVector:

SparseVector(nums) Initializes the object with the vector nums
dotProduct(vec) Compute the dot product between the instance of SparseVector and vec
A sparse vector is a vector that has mostly zero values, you should store the sparse vector efficiently and compute
the dot product between two SparseVector.

Follow up: What if only one of the vectors is sparse? """

from collections import defaultdict


class SparseVectorV1:

    def __init__(self, nums):
        """ A sparse vector is a vector that has mostly zero values, while a dense vector is a vector where most of
             the elements are non-zero.

             It is inefficient to store a sparse vector as a one-dimensional array. Instead, we can store the non-zero
             values and their corresponding indices in a dictionary, with the index being the key. Any index that is not
             present corresponds to a value 0 in the input array.

             Dot product requires two vectors of equal length. However, after we store the vector in a hashmap, their
             sizes are different based on the sparsity. Therefore, the performance can be improved by iterating over the
             shorter hashmap and check whether each key is present in the other vector. This effectively answers the
             follow-up question.

        Time complexity: O(N), for creating the hashmap; O(L) for calculating the dot product, where L is the length
        of the shortest hashmap
        Space complexity: O(L), for creating the hashmap, as we only store elements that are non-zero. O(1) for
        calculating the dot product
        """
        self.non_zeros = defaultdict(int)
        for i, num in enumerate(nums):
            if num:
                self.non_zeros[i] = num

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec):
        """
        :type vec: 'SparseVector'
        :rtype: int
        """
        non_zeros = self.non_zeros
        if len(vec.non_zeros) < len(non_zeros):
            return vec.dotProduct(self)
        res = 0
        for i, num in non_zeros.items():
            res += num * vec.non_zeros[i]
        return res


class SparseVectorV2:
    def __init__(self, nums):
        """ We can also represent elements of a sparse vector as a list of <index, value> pairs. We use two pointers to
        iterate through the two vectors to calculate the dot product.
        Time complexity: O(N) for creating the <index, value> pair for non-zero values, O(L1 + L2) for calculating the
        dot product, where L1 is the number of non-zero values in the first vector and L2 is the number of non-zero
        values in the second vector
        Space complexity: O(L) for creating the <index, value> pairs for non-zero values, O(1) for calculating the dot
        product
        """
        self.pairs = []
        for i, num in enumerate(nums):
            if num:
                self.pairs.append((i, num))

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec):
        """
        :type vec: 'SparseVector'
        :rtype: int
        """
        res = 0
        i = j = 0
        n, m = len(self.pairs), len(vec.pairs)
        while i < n and j < m:
            self_index, self_val = self.pairs[i]
            vec_index, vec_val = vec.pairs[j]
            if self_index == vec_index:  # Both elements at this index are non-zero, so they contribute to the product
                res += self_val * vec_val
                i += 1
                j += 1
            elif self_index < vec_index:  # We've got a non-zero value at the current index, but the next non-zero
                # value of the other vector is ahead of us
                i += 1
            else:
                j += 1
        return res
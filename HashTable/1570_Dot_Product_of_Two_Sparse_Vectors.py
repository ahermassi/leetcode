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
        """ Hashing/lookups, while on surface look efficient, for large sparse vectors, hashing function takes up bulk
             of the computation. Technically, a hashmap uses an array of nodes internally, but to get an element we hash
             the key, and then access this array based on the hashcode. Depending on the hashing function, can result in
             collisions. Also, the hashmap resizes when it gets to 75% (by default) capacity, but then it will rehash
             everything. And this is likely to happen a lot as size grows. So between the resizing and the collisions,
             the hashmap approach isn't going to scale well to a very large vector.

             We can represent the elements of a sparse vector as a list of <index, value> pairs. We then use two
             pointers to iterate through the two vectors to calculate the dot product.

        Time complexity: O(N), for creating the <index, value> pair for non-zero values, O(L1 + L2) for calculating the
        dot product, where L1 is the number of non-zero values in the first vector and L2 is the number of non-zero
        values in the second vector
        Space complexity: O(L), for creating the <index, value> pairs for non-zero values, O(1) for calculating the dot
        product
        """
        self.non_zeros = []
        for i, num in enumerate(nums):
            if num:
                self.non_zeros.append((i, num))

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec):
        """
        :type vec: 'SparseVector'
        :rtype: int
        """
        n, m = len(self.non_zeros), len(vec.non_zeros)
        res = 0
        i = j = 0
        while i < n and j < m:
            self_index, self_val = self.non_zeros[i]
            vec_index, vec_val = vec.non_zeros[j]
            if self_index == vec_index:
                # Both elements at this index are non-zero, so they contribute to the product
                res += self_val * vec_val
                i += 1
                j += 1
            elif self_index < vec_index:
                # We've got a non-zero value at the current index, but the next non-zero value of the other vector is
                # ahead
                i += 1
            else:
                j += 1
        return res


class SparseVectorV3:
    def __init__(self, nums):
        """ What if only one vector is sparse and the other is full of non-zero values?

             If the sizes of the two index-pair vectors are n and m, then we iterate the smaller vector (sparse) and
             binary search the larger one. So the effective runtime is O(min(n, m) * Log(max(n, m)))

             Let's say, m is few orders of magnitude bigger than n, like n=5 and m = 1024. nLog(m) = 5*Log(1024) = 50,
             whereas n + m = 5 + 1024 = 1029, so it does make a difference.

        Time complexity: O(N), for creating the <index, value> pair for non-zero values, O(L1 * Log(L2)) for
        calculating the dot product, where L1 is the number of non-zero values in the shortest vector and L2 is the
        number of non-zero values in the other vector
        Space complexity: O(L), for creating the <index, value> pairs for non-zero values, O(1) for calculating the dot
        product
        """
        self.non_zeros = []
        for i, num in enumerate(nums):
            if num:
                self.non_zeros.append((i, num))

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec):
        """
        :type vec: 'SparseVector'
        :rtype: int
        """
        def binary_search(index, pairs):
            left, right = 0, len(pairs) - 1
            while left <= right:
                mid = (left + right) // 2
                if pairs[mid][0] == index:
                    return pairs[mid][1]
                if pairs[mid][0] < index:
                    left = mid + 1
                else:
                    right = mid - 1
            return float('inf')

        self_non_zeros, vec_non_zeros = self.non_zeros, vec.non_zeros
        if len(vec_non_zeros) < len(self_non_zeros):
            return vec.dotProduct(self)
        res = 0
        for i, num1 in enumerate(self_non_zeros):
            num2 = binary_search(i, vec_non_zeros)
            if num2 != float('inf'):
                res += num1 * num2
        return res
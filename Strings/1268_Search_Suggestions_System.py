""" Given an array of strings products and a string search_word. We want to design a system that suggests at most three
product names from products after each character of search_word is typed. Suggested products should have common prefix
with the search_word. If there are more than three products with a common prefix return the three lexicographically
minimums products.
Return list of lists of the suggested products after each character of search_word is typed. """

from _heapq import heappush, heappop
import unittest2 as unittest


def suggested_products_v1(products, search_word):
    """ For any two words w1 and w2 in 'products', if w1 is prefix of w2, w1 and w2 must be neighbours in the sorted
        'products'. The same, we can binary search the position of each prefix of search word in 'products' and check
        if the following 3 words are valid.
    Time complexity: O(P * logP), where N is the length of products array
    Space complexity: O(P)
    """

    def insertion_index(word):
        left, right = 0, len(products) - 1
        while left < right:
            mid = (left + right) // 2
            if products[mid] < word:
                left = mid + 1
            else:
                right = mid
        return left

    products.sort()
    res, prefix = [], ''
    for c in search_word:
        prefix += c
        index = insertion_index(prefix)  # Find where 'prefix' can be inserted in order in the products array. Same as
        # bisect_left()
        suggestions = [products[i] for i in range(index, min(len(products), index + 3)) if prefix in products[i]]
        res.append(suggestions)
    return res


def suggested_products_v2(products, search_word):
    """ Iterate through every substring of search_word asking each word in the products array if it starts with the
        substring. If it does, we add it to a heap which is comparing lexicographically, that way we just need to
        pop from the heap 3 times to find the appropriate suggestions.
    Time complexity: O(N * P * logP), where N is the length of the search word and P is the length of products list
    Space complexity: O(N + P), for the search word slicing and the heap space
    """
    heap, res = [], []
    n = len(search_word)
    for i in range(n):
        prefix = search_word[:i + 1]
        for product in products:
            if product[:i + 1] == prefix:
                heappush(heap, product)
        suggestions = []
        for _ in range(3):
            if heap:
                suggestions.append(heappop(heap))
        heap = []  # Clear the heap at the end of every iteration
        res.append(suggestions)
    return res


class Test(unittest.TestCase):
    data = [(['mobile', 'mouse', 'moneypot', 'monitor', 'mousepad'], 'mouse',
             [['mobile', 'moneypot', 'monitor'], ['mobile', 'moneypot', 'monitor'], ['mouse', 'mousepad'],
              ['mouse', 'mousepad'], ['mouse', 'mousepad']])]

    def test_suggested_products(self):
        for test_products, test_search_word, result in self.data:
            self.assertEqual(result, suggested_products_v1(test_products, test_search_word))
            self.assertEqual(result, suggested_products_v2(test_products, test_search_word))


if __name__ == '__main__':
    unittest.main()

""" A gene string can be represented by an 8-character long string, with choices from 'A', 'C', 'G', and 'T'.

Suppose we need to investigate a mutation from a gene string start_gene to a gene string end_gene where one mutation is
defined as one single character changed in the gene string.

For example, "AACCGGTT" --> "AACCGGTA" is one mutation.
There is also a gene bank bank that records all the valid gene mutations. A gene must be in bank to make it a valid
gene string.

Given the two gene strings start_gene and end_gene and the gene bank bank, return the minimum number of mutations needed
to mutate from start_gene to end_gene. If there is no such a mutation, return -1.

Note that the starting point is assumed to be valid, so it might not be included in the bank. """

from collections import deque
import unittest2 as unittest


def min_mutation_v1(start_gene, end_gene, bank):
    """ Similar to 127- Word Ladder.

         We can model the problem as a graph. Each gene string is a node, and mutations are the edges. Two nodes have an
         edge (are neighbors) if they differ by one character. The added constraints are that the characters must be one
         of "ACGT", and each node must be in the bank.

         Then, the problem is simplified: what is the shortest path between start and end?

         When a graph problem involves finding the shortest path, BFS should be used over DFS. This is because with BFS,
         all nodes at distance x from start will be visited before any node at distance x+1 will be visited. Once we
         find the target (end), we know that we found it in the smallest number of steps possible.

            - Perform a BFS starting from node start. Keep track of the number of steps taken so far and return that
               number of steps when we find end.

            - Only traverse to nodes that are in bank. Neighbors can be found by iterating over each node and replacing
               one of the characters with a character from "ACGT".

            - To check if a node is in bank, we would normally first convert bank to a set to have O(1) checking.
               However, the problem's constraints state that 0 <= bank.length <= 10. With such a small constraint, it
               may actually be slower to use a set due to the overhead associated with hashing.

            - If we finish the BFS and did not find end, then the task is impossible. Return -1.

    Time complexity: technically, the BFS runs in constant time because the problem limits the length of the gene
    strings to 8 and the strings can only have 4 characters.
    Space complexity: O(1)
    """
    bank = set(bank)
    if end_gene not in bank:
        return -1
    choices = 'ACGT'
    queue = deque([(start_gene, 0)])
    while queue and bank:
        gene, mutations = queue.popleft()
        chars = list(gene)
        for i, c in enumerate(chars):
            for choice in choices:
                chars[i] = choice
                mutation = ''.join(chars)
                if mutation == end_gene:
                    return mutations + 1
                if mutation in bank:
                    queue.append((mutation, mutations + 1))
                    bank.remove(mutation)
                chars[i] = c
    return -1


def min_mutation_v2(start_gene, end_gene, bank):
    """ A different style of BFS.

        Instead of actually mutating the genes, we can check the difference between the current gene string and those in
        the bank. The transformation is valid if the difference is only 1 character.

        We also use a visited set to prevent visiting a node more than once and also because it's not possible not
        remove a string from a hash set while iterating over the set.

    Time complexity: O(1)
    Space complexity: O(1)
    """
    bank = set(bank)
    if end_gene not in bank:
        return -1
    queue = deque([(start_gene, 0)])
    visited = set()
    while queue:
        gene, mutations = queue.popleft()
        for mutation in bank:
            if mutation in visited:
                continue
            diff = 0
            for i, c in enumerate(mutation):
                if gene[i] != c:
                    diff += 1
            if diff == 1:
                if mutation == end_gene:
                    return mutations + 1
                queue.append((mutation, mutations + 1))
                visited.add(mutation)
    return -1


class Test(unittest.TestCase):
    data = [('AACCGGTT', 'AACCGGTA', ['AACCGGTA'], 1),
            ('AACCGGTT', 'AAACGGTA', ['AACCGGTA', 'AACCGCTA', 'AAACGGTA'], 2)]

    def test_ladder_length(self):
        for start_gene, end_gene, bank, result in self.data:
            self.assertEqual(result, min_mutation_v1(start_gene, end_gene, bank))
            self.assertEqual(result, min_mutation_v2(start_gene, end_gene, bank))


if __name__ == '__main__':
    unittest.main()

""" Given a string containing only digits, restore it by returning all possible valid IP address combinations. """

import unittest2 as unittest


def restore_ip_addresses_v1(s):
    """ There are three periods in a valid IP address, so we can enumerate all possible placements of these periods,
        and check whether all four corresponding substrings are between 0 and 255. We can reduce the number of
        placements considered by spacing the periods 1 to 3 characters apart.
        Each part separated by the '.' should not start with '0' except only '0'.
        Each part separated by the '.' should not be larger than 255.
    Time complexity: O(1), the total number of IP addresses is a constant (2^32)
    Space complexity: O(1)
    """

    def is_valid(segment):
        return len(segment) == 1 or segment[0] != '0' and int(segment) <= 255

    n, res = len(s), []
    for i in range(1, min(4, n - 2)):
        for j in range(i + 1, min(i + 4, n - 1)):
            for k in range(j + 1, min(j + 4, n)):
                part1, part2, part3, part4 = s[:i], s[i:j], s[j:k], s[k:]
                if is_valid(part1) and is_valid(part2) and is_valid(part3) and is_valid(part4):
                    res.append('.'.join([part1, part2, part3, part4]))
    return res


def restore_ip_addresses_v2(s):
    """ Let's imagine we put one or two dots already and that left no way to place the others to create a valid IP
        address. What to do? To backtrack. That means to come back, to change the position of the previously placed
        dot and try to proceed again. If that would not work either, backtrack again.
    Time complexity: O(1), the total number of IP addresses is a constant (2^32)
    Space complexity: O(1)
    """

    def is_valid(segment):
        return len(segment) == 1 or segment[0] != '0' and int(segment) <= 255

    def dfs(index, path, dots):  # 'index' is where we last placed a dot
        if dots > 4:  # We placed more than 4 dots. Remember that we place 1st dot and recurse with dots=1, place 2nd
            # dot and recurse with dots=2, place 3rd dot and recurse with dots=3, then finally find the last valid
            # segment and recurse with dots=4
            return
        if dots == 4 and index == n:  # Check if all 3 dots are placed and the end of string was reached
            res.append(path[:-1])  # If we don't exclude the last character, the last ip part would end with a dot '.'
            return
        for i in range(1, 4):  # Iterate over three available slots to place a dot
            if index + i > n:
                break
            segment = s[index:index + i]
            if is_valid(segment):  # Check if the segment from the previous dot to the current index is valid
                dfs(index + i, path + segment + '.', dots + 1)  # If yes, place the dot and proceed to place next dots

    n, res = len(s), []
    dfs(0, '', 0)
    return res


class Test(unittest.TestCase):
    data = [('25525511135', ['255.255.11.135', '255.255.111.35'])]

    def test_restore_ip_addresses(self):
        for test_string, result in self.data:
            self.assertEqual(result, restore_ip_addresses_v1(test_string))
            self.assertEqual(result, restore_ip_addresses_v2(test_string))


if __name__ == '__main__':
    unittest.main()
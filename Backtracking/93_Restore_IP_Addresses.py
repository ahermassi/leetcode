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


class Test(unittest.TestCase):
    data = [('25525511135', ['255.255.11.135', '255.255.111.35'])]

    def test_restore_ip_addresses(self):
        for test_string, result in self.data:
            self.assertEqual(result, restore_ip_addresses_v1(test_string))


if __name__ == '__main__':
    unittest.main()
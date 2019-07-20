""" Given a list of emails, we send one email to each address in the list.  How many different addresses actually
receive mails?  """

import unittest2 as unittest


def num_unique_emails(emails):
    """ Time complexity: O(N)
        Space complexity: O(N)
    """
    unique_addresses = set()  # Use set() instead of list() or []
    for email in emails:
        local, domain = email.split('@')  # Note this beautiful unpacking in action
        if '+' in local:
            local = local[:local.find('+')]
        local = local.replace('.', '')
        unique_addresses.add('@'.join([local, domain]))
    return len(unique_addresses)  # If [] was used in the beginning, this would be return len(set(unique_addresses))


class Test(unittest.TestCase):
    data = ['test.email+alex@leetcode.com', 'test.e.mail+bob.cathy@leetcode.com', 'testemail+david@lee.tcode.com']

    def test_num_unique_emails(self):
        self.assertEqual(2, num_unique_emails(self.data))


if __name__ == '__main__':
    unittest.main()

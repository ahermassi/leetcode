""" Given a list of emails, we send one email to each address in the list.  How many different addresses actually
receive mails?  """

import unittest2 as unittest


def num_unique_emails(emails):
    """ Pretty straightforward. Process the emails and apply the necessary modifications. Use a set to store the new,
        modified addresses.
    Time complexity: O(N * k), where k is the number of emails and N is the length of the longest email
    Space complexity: O(N)
    """
    unique_addresses = set()  # Use a set instead of a list to avoid duplicates
    for email in emails:
        local, domain = email.split('@')  # Note this beautiful unpacking in action
        local = local.replace('.', '')
        local = local.split('+')[0]
        unique_addresses.add('@'.join([local, domain]))
    return len(unique_addresses)


class Test(unittest.TestCase):
    data = ['test.email+alex@leetcode.com', 'test.e.mail+bob.cathy@leetcode.com', 'testemail+david@lee.tcode.com']

    def test_num_unique_emails(self):
        self.assertEqual(2, num_unique_emails(self.data))


if __name__ == '__main__':
    unittest.main()

""" Read description on Leetcode """

from collections import defaultdict
import unittest2 as unittest


# All this entire problem is TODO.

def accounts_merge_v1(accounts):
    """ We give each account an ID, based on the index of it within the list of accounts.
        Next, build an emails_accounts_map that maps an email to a list of accounts, which can be used to track which
        email is linked to which account. This is essentially our graph.
        Next we do a DFS on each account in accounts list and look up emails_accounts_map to tell us which accounts are
        linked to that particular account via common emails. This will make sure we visit each account only once. This
        is a recursive process and we should collect all the emails that we encounter along the way.
        Lastly, sort the collected emails and add it to final results, res along with the name.
    Time complexity: O(sum(a_i log(a_i)), where a_i is the length of accounts[i]. Without the log factor, this is the
    complexity to build the graph and search for each component. The log factor is for sorting each component at the
    end.
    Space complexity: O(sum(a_i)), the space used by our graph and our search
    """

    # DFS code for traversing accounts.
    def dfs(i, emails):
        if i in visited:
            return
        visited.add(i)
        for j in range(1, len(accounts[i])):
            email = accounts[i][j]
            emails.add(email)
            for neighbor in emails_accounts_map[email]:
                dfs(neighbor, emails)

    visited, res = set(), []
    emails_accounts_map = defaultdict(list)
    # Build up the graph.
    for i, account in enumerate(accounts):
        for j in range(1, len(account)):
            email = account[j]
            emails_accounts_map[email].append(i)

    # Perform DFS for accounts and add to results.
    for i, account in enumerate(accounts):
        if i not in visited:
            name, emails = account[0], set()
            dfs(i, emails)
            res.append([name] + sorted(emails))
    return res


def accounts_merge_v2(accounts):
    """ The key task here is to connect those emails, and this is a perfect use case for union find.
        To group these emails, each group need to have a representative, or parent.
        At the beginning, set each email as its own representative.
        Emails in each account naturally belong to a same group, and should be joined by assigning to the same parent
        (let's use the parent of first email in that list)
    Time complexity: O(sum(a_i log(a_i))
    Space complexity: O(sum(a_i))
    """

    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        parent[find(i)] = find(j)

    parent = {}
    email_to_name = {}
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in parent:
                parent[email] = email
            email_to_name[email] = name
            union(email, account[1])  # account[1]: the first email

    res = defaultdict(list)
    for email in parent.keys():
        res[find(email)].append(email)

    return [[email_to_name[root]] + sorted(emails) for (root, emails) in res.items()]


class Test(unittest.TestCase):
    data = [([['John', 'johnsmith@mail.com', 'john00@mail.com'], ['John', 'johnnybravo@mail.com'],
              ['John', 'johnsmith@mail.com', 'john_newyork@mail.com'], ['Mary', 'mary@mail.com']],
             [['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com'],  
              ['John', 'johnnybravo@mail.com'], ['Mary', 'mary@mail.com']])]

    def test_accounts_merge(self):
        for test_accounts, result in self.data:
            self.assertEqual(result, accounts_merge_v1(test_accounts))
            self.assertEqual(result, accounts_merge_v2(test_accounts))


if __name__ == '__main__':
    unittest.main()
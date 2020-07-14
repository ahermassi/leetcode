""" Read description on Leetcode """

from collections import defaultdict
import unittest2 as unittest


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


# Similar to https://leetcode.com/problems/accounts-merge/discuss/109161/Python-Simple-DFS-with-explanation!!!
# 4th comment

def accounts_merge_v2(accounts):
    """ A different DFS approach. For every pair of emails in the same account, draw an edge between those emails.
        The problem is about enumerating the connected components of this graph.
    Time complexity: O(sum(a_i log(a_i))
    Space complexity: O(sum(a_i))
    """
    def dfs(vertex, emails):
        if vertex not in visited:
            emails.append(vertex)
            visited.add(vertex)
            for neighbor in graph[vertex]:
                dfs(neighbor, emails)

    res, visited, graph = [], set(), defaultdict(list)
    for account in accounts:
        n = len(account)
        for i in range(1, n - 1):
            graph[account[i]].append(account[i + 1])
            graph[account[i + 1]].append(account[i])
    for account in accounts:
        n = len(account)
        for i in range(1, n):
            if account[i] not in visited:  # This vertex hasn't been explored yet
                user_name, emails = account[0], []
                dfs(account[i], emails)  # Collect the vertices/emails that belong to the same connected component
                res.append([user_name] + sorted(emails))
    return res


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
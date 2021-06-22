""" Given a list of accounts where each element accounts[i] is a list of strings, where the first element
accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account.

Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common
email to both accounts. Note that even if two accounts have the same name, they may belong to different people as
people could have the same name. A person can have any number of accounts initially, but all of their accounts
definitely have the same name.

After merging the accounts, return the accounts in the following format: the first element of each account is the name,
and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order. """

from collections import defaultdict
import unittest2 as unittest


def accounts_merge_v1(accounts):
    """ For every pair of emails in the same account, draw an edge between those emails. The problem is about
        enumerating the connected components of this graph.
        Notice that each accounts[i] tells us some edges. What we have to do is as follows:
        Use these edges to build some components. Common email addresses are like the intersections that connect each
        single component for each account.
        Because each component represents a merged account, do DFS search for each component and add it into a list.
        Before adding the name to this list, sort the emails. Then add name string into it.
        Example: Assume we have three accounts, we connect them like this in order to use DFS.
            {Name, 1, 2, 3} => Name -- 1 -- 2 -- 3
            {Name, 2, 4, 5} => Name -- 2 -- 4 -- 5 (The same graph node 2 appears)
            {Name, 6, 7, 8} => Name -- 6 -- 7 -- 8
            (Where numbers represent email addresses)
    Time complexity: O(sum(a_i log(a_i)), where a_i is the length of accounts[i]. Without the log factor, this is the
    complexity of building the graph and searching for each component. The log factor is for sorting each component at
    the end.
    Space complexity: O(sum(a_i))
    """
    def build_graph():
        for account in accounts:
            n = len(account)
            for i in range(1, n - 1):
                graph[account[i]].append(account[i + 1])
                graph[account[i + 1]].append(account[i])

    def dfs(vertex, emails):
        if vertex not in visited:  # Each vertex/node is an email address
            emails.append(vertex)
            visited.add(vertex)
            for neighbor in graph[vertex]:
                dfs(neighbor, emails)

    graph = defaultdict(list)
    build_graph()
    res, visited, = [], set()
    for account in accounts:
        n = len(account)
        for i in range(1, n):
            if account[i] not in visited:  # This vertex hasn't been explored yet. Each account[i] is an email address
                user_name, emails = account[0], []
                dfs(account[i], emails)  # Collect the vertices/emails that belong to the same connected component
                res.append([user_name] + sorted(emails))
    return res


# Similar to https://leetcode.com/problems/accounts-merge/discuss/109161/Python-Simple-DFS-with-explanation!!!
# 4th comment

def accounts_merge_v2(accounts):
    """ We give each account owner an ID based on its index within the list of accounts.
        Next, build an email_owners_map that maps an email to a list of account owners, which can be used to track which
        email is linked to which account. This is essentially our graph.
        Next we do a DFS on each account in accounts list and look up email_owners_map to tell us which accounts are
        linked to that particular account via common emails. This will make sure we visit each account only once. This
        is a recursive process and we should collect all the emails that we encounter along the way.
        Lastly, sort the collected emails and add it to final results, res along with the name.
        Example:
            [
                ["John", "johnsmith@mail.com", "john00@mail.com"], # Account 0
                ["John", "johnnybravo@mail.com"], # Account 1
                ["John", "johnsmith@mail.com", "john_newyork@mail.com"],  # Account 2
                ["Mary", "mary@mail.com"] # Account 3
            ]
            emails_accounts_map of email to account ID
            {
                "johnsmith@mail.com": [0, 2],
                "john00@mail.com": [0],
                "johnnybravo@mail.com": [1],
                "john_newyork@mail.com": [2],
                "mary@mail.com": [3]
            }
    Time complexity: O(sum(a_i log(a_i))
    Space complexity: O(sum(a_i)), the space used by our graph and our search
    """
    def build_graph():
        for i, account in enumerate(accounts):
            for j in range(1, len(account)):
                email = account[j]
                email_owners_map[email].append(i)  # key:value, email:[list of account ids it's associated with]

    # DFS code for traversing accounts. It collects the emails associated with the current id and recursively
    # collects the other emails that are shared with the rest of ids that exist in email_owners_map[email]
    def dfs(id, emails):
        if id in visited:
            return
        visited.add(id)
        cur_account = accounts[id]  # [owner_name, ...emails]
        for j in range(1, len(cur_account)):
            email = cur_account[j]
            emails.add(email)
            for neighbor in email_owners_map[email]:  # Navigate to the different account ids to which this email is
                # associated and collect the rest of email addresses
                dfs(neighbor, emails)

    visited, res = set(), []
    email_owners_map = defaultdict(list)
    build_graph()

    # Perform DFS for accounts and add to results.
    for id, account in enumerate(accounts):
        if id not in visited:
            owner_name, emails = account[0], set()
            dfs(id, emails)
            res.append([owner_name] + sorted(emails))
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
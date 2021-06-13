""" Given a string s of '(' , ')' and lowercase English characters.
Your task is to remove the minimum number of parentheses ( '(' or ')', in any positions ) so that the resulting
parentheses string is valid and return any valid string. """

import unittest2 as unittest


def min_remove_to_make_valid_v1(s):
    """ The parentheses in a string are balanced if and only if these 2 conditions are met:
            1- There is the same number of '(' and ')' in the string
            2- Scanning through the string from left to right and counting how many '(' and ')' there are so far,
               there should never be a time where there are more ')' than '('
        We call count('(') - count(')') the balance of the string.
        So, remembering that each ')' was paired with the closest '(' that isn't already paired, how could we do this
        in code? We need to know the indexes of the problematic '('.
        We can use a stack. Each time we see a '(', we add its index to the stack. Each time we see a ')', we remove
        an index from the stack because the ')' will match with whatever '(' was at the top of the stack. The length
        of the stack is equivalent to the balance.
        We will need to:
            1- Remove a ')' if it is encountered when stack was already empty (prevent negative balance)
            2- Remove a '(' if it is left on stack at end (prevent non-zero final balance)
        After removing invalid ')', the number of '(' we remove is the minimum needed to ensure that
        count('(') == count(')'), or that the balance is equal to 0.
        If we put the indexes of the '(' on the stack, then we'll know that all the indices on the stack at the end
        are the indices of the unmatched '('. We should also use a set to keep track of the unmatched ')' we come
        across. Then, we can remove the character at each of those indices and then return the edited string.
        In fewer words:
        To make the string valid with minimum removals, we need to get rid of all parentheses that do not have a
        matching pair.
            1- Push char index into the stack when we see '('
            2- Pop from the stack when we see ')'
                - If the stack is empty, then we have ')' without the pair, and it needs to be removed
            3- In the end, the stack will contain indexes of '(' without the pair, if any. We need to remove all of
               them too.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    stack, invalid_indices = [], set()
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        elif c == ')':
            if stack:
                stack.pop()
            else:
                # Meet closing parentheses but no opening parenthesis -> remove closing parenthesis
                invalid_indices.add(i)
    while stack:
        invalid_indices.add(stack.pop())  # Remove remaining open parenthesis
    return ''.join([c for i, c in enumerate(s) if i not in invalid_indices])


class Test(unittest.TestCase):
    data = [('lee(t(c)o)de)', 'lee(t(c)o)de'), ('))((', '')]

    def test_min_remove_to_make_valid(self):
        for test_s, result in self.data:
            self.assertEqual(result, min_remove_to_make_valid(test_s))


if __name__ == '__main__':
    unittest.main()
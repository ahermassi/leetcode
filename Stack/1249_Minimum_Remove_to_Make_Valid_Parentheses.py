""" Given a string s of '(' , ')' and lowercase English characters.
Your task is to remove the minimum number of parentheses ( '(' or ')', in any positions ) so that the resulting
parentheses string is valid and return any valid string. """

import unittest2 as unittest


def min_remove_to_make_valid_v1(s):
    """ The parentheses in a string are balanced if and only if these 2 conditions are met:

            1- There is the same number of '(' and ')' in the string
            2- Scanning through the string from left to right and counting how many '(' and ')' there are so far,
               there should never be a time when there are more ')' than '('

        We call count('(') - count(')') the balance of the string.

        For starters, we know we'll need to remove any ')' that we encountered when balance was already 0. It would be
        impossible to remove less ')', because there are not enough '(' before them.

        So, remembering that each ')' was paired with the closest '(' that isn't already paired, how could we do this
        in code? We need to know the indices of the problematic '('s.

        We can use a stack. Each time we see a '(', we add its index to the stack. Each time we see a ')', we remove
        an index from the stack because the ')' will match with whatever '(' was at the top of the stack. The length
        of the stack is equivalent to the balance.

        We will need to:

            1- Mark a ')' as invalid/unmatched if it is encountered when stack was already empty (prevent negative
                 balance)
            2- Remove a '(' if it is left on stack at end (prevent non-zero final balance)

        After removing invalid ')', the number of '(' we remove is the minimum needed to ensure that
        count('(') == count(')'), or that the balance is equal to 0.

        If we put the indices of the '(' on the stack, then we'll know that all the indices on the stack at the end
        are the indices of the unmatched '('. We should also use a hash set (or a second stack) to keep track of the
        unmatched ')' we've come across. Then, we can remove the character at each of those indices and then return the
        edited string.

        If all the indices we need to remove are in a set, then we can iterate through each index in the string, check
        if the current index is in the set, and if it is not, then add the character at that index to the string builder.

        In fewer words:
        To make the string valid with minimum removals, we need to get rid of all parentheses that do not have a
        matching pair.

            1- Push char index into the stack when we see '('
            2- Pop from the stack when we see ')'
                - If the stack is empty, then we have ')' without the pair, and it needs to be removed
            3- In the end, the stack will contain indices of '(' without the pair, if any. We need to remove all of
               them too.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    unmatched_left, unmatched_right = [], []
    for i, c in enumerate(s):
        if c == '(':
            unmatched_left.append(i)
        elif c == ')':
            if unmatched_left:
                unmatched_left.pop()
            else:
                # Meet closing parentheses but no opening parenthesis -> remove closing parenthesis
                unmatched_right.append(i)
    while unmatched_left:
        # Collect all the unmatched parentheses into a single holder
        unmatched_right.append(unmatched_left.pop())
    unmatched_brackets = set(unmatched_right)
    return ''.join([c for i, c in enumerate(s) if i not in unmatched_brackets])


def min_remove_to_make_valid_v2(s):
    """ Similar idea but operating on the string's characters as we go.

         A key observation we might have made from the previous algorithm is that for all invalid ')', we know
         immediately that they are invalid (they are the ones we were putting in the set). It is the '(' that we don't
         know about until the end (as they are what was left on the stack at the end).

        Keep track of indices of unmatched left parentheses in the stack. In other words, when we come across an open
        parenthesis we add its index to the stack.

        When we come across a right parenthesis, we pop an element from the stack. If the stack is empty, we replace the
        current character with an empty string.

        At the end, we replace all indices we have in the stack with empty strings because they don't have matching
        right parentheses.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    chars = list(s)
    unmatched_left = []
    for i, c in enumerate(s):
        if c == '(':
            unmatched_left.append(i)
        elif c == ')':
            if not unmatched_left:
                chars[i] = ''
            else:
                unmatched_left.pop()
    for index in unmatched_left:
        chars[index] = ''
    return ''.join(chars)


class Test(unittest.TestCase):
    data = [('lee(t(c)o)de)', 'lee(t(c)o)de'), ('))((', '')]

    def test_min_remove_to_make_valid(self):
        for test_s, result in self.data:
            self.assertEqual(result, min_remove_to_make_valid_v1(test_s))
            self.assertEqual(result, min_remove_to_make_valid_v2(test_s))


if __name__ == '__main__':
    unittest.main()
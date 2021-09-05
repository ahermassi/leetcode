""" Given a parentheses string s containing only the characters '(' and ')'. A parentheses string is balanced if:

Any left parenthesis '(' must have a corresponding two consecutive right parenthesis '))'.
Left parenthesis '(' must go before the corresponding two consecutive right parenthesis '))'.
In other words, we treat '(' as opening parenthesis and '))' as closing parenthesis.

For example, "())", "())(())))" and "(())())))" are balanced, ")()", "()))" and "(()))" are not balanced.

You can insert the characters '(' and ')' at any position of the string to balance it if needed.

Return the minimum number of insertions needed to make s balanced. """


def min_insertions_v1(s):
    """ Maintain a stack. Every time we see a '(' we need to have 2 ')' to balance it out, soo we would push 2 to the
        stack. Then when we see ')' we would check the top of the stack. If the top is 2, that means this is the
        first ')' that will match the previous '(', so we would change the top to 1. In case the top of stack had 1,
        means we are seeing the second ')' for some '(' and so we just pop this 1 from the stack.

        Details of transition:

        When we see '(':
            - If the stack is empty or has a 2 at the top: we just push another 2.
            - If the stack has 1 at the top, this means we have just seen '()' and now we are seeing '('. In this case,
              we need to first provide a ')' to the previous '()' and then we can process the current '('. So increment
              right_parenthesis_added, pop the 1 (which was for last '()'), and push a 2 (for current '(')

        When we see ')':
            - If the stack is empty: We have encountered a lone ')'. We would need to add '(' to the sequence to
              balance out, which would match one of its ')' with the current ')'. So we increment
              'left_parenthesis_added'. Moreover, it would also need another ')' to match, soo we push 1 to the top.
              This is like saying we have seen '()' (of which '(' was inserted by us).
            - If the stack had 1 at the top: This the second ')' for some '('. We just pop from the stack.
            - If the stack had 2 at the top: This the first ')' for some '('. We just pop 2 from the stack and push 1.

        Finally, we just add up all the numbers in the stack with the number of left and right parenthesis that we
        added.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    left_unmatched = []
    left_parenthesis_added = right_parenthesis_added = 0
    for c in s:
        if c == '(':
            if not left_unmatched or left_unmatched[-1] == 2:
                left_unmatched.append(2)
            else:
                right_parenthesis_added += 1
                left_unmatched.pop()
                left_unmatched.append(2)
        elif not left_unmatched:
            left_parenthesis_added += 1
            left_unmatched.append(1)
        elif left_unmatched[-1] == 1:
            left_unmatched.pop()
        else:
            left_unmatched[-1] = 1
    return left_parenthesis_added + right_parenthesis_added + sum(left_unmatched)

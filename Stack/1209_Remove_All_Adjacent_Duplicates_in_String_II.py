""" You are given a string s and an integer k, a k duplicate removal consists of choosing k adjacent and equal letters
from s and removing them, causing the left and the right side of the deleted substring to concatenate together.

We repeatedly make k duplicate removals on s until we no longer can.

Return the final string after all such duplicate removals have been made. It is guaranteed that the answer is
unique. """


def remove_duplicates_v1(s, k):
    """ Notice that we consider groups of elements with the same value which are adjacent. If we delete them, other
        symbols will become adjacent. Stack is just ideal for this purposes.
        So, we maintain a stack with pairs of elements: the character and its frequency. For each element:
            - Check if the current character matches to the previous one in stack. If it does, increment the count on
              the top of the stack. Otherwise, create a new instance with a count of 1.
            - Check if we can delete groups of k equal elements: If last frequency in stack is equal to k, pop from
              the stack.
        Finally, we build the result string using characters and counts in the stack.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    stack = []
    for c in s:
        if not stack or stack[-1][0] != c:
            stack.append([c, 1])
        else:
            stack[-1][1] += 1
        if stack[-1][1] == k:
            stack.pop()
    return ''.join([c * freq for c, freq in stack])


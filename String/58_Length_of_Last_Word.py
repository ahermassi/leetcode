""" Given a string s consisting of words and spaces, return the length of the last word in the string.
A word is a maximal
substring
 consisting of non-space characters only. """


def lengthOfLastWordV1(s):
    """ We should pay attention to some edge cases:

            1- The input string could be empty.
            2- There could be some trailing spaces in the input string, e.g. hello <space>.
            3- There might only be one word in the given string.

        The challenge is to build a concise yet comprehensive solution that could handle all above cases.

        We can break down the solution into two steps:

            - Try to locate the last word, starting from the end of the string. We iterate the string in reverse order,
               consuming the empty spaces. When we first come across a non-space character, we know that we are at the
               last character of the last word.

            - Once we locate the last word, we count its length starting from its last character.

        Time complexity: O(N), where N is the length of the input string. In the worst case, the input string might
        contain only a single word, which implies that we would need to iterate through the entire string to obtain the
        result.
        Space complexity: O(1)
        """
    last_space = len(s) - 1
    while s[last_space] == '  ':
        last_space -= 1
    length = 0
    while last_space >= 0 and s[last_space] != '  ':
        length += 1
        last_space -= 1
    return length


def lengthOfLastWordV2(s):
    """ In the above approach, we applied two loops. One is used to locate the last word, and the other one to calculate
         its length. We could actually complete the same tasks within a single loop.

         The trick is that we could define a condition, i.e. the precise moment that we should start to count the length
         of the word. If we encounter a white space while a word count is underway, we know this space marks the start
         of the second-to-last word.

        Time complexity: O(N), where N is the length of the input string
        Space complexity: O(1)
        """
    length = 0
    i = len(s) - 1
    while i >= 0:
        if s[i] != '  ':
            length += 1
        elif length > 0:
            # Did we already start to count the length of a word ? If yes, we've found the last word
            return length
        i -= 1
    return length

""" Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and
is decoded back to the original list of strings. """


class CodecV1:
    """ Naive solution here is to join strings using delimiters.
        What to use as a delimiter? Each string may contain any possible characters out of 256 valid ascii characters.
        It's convenient to use two different non-ASCII characters to distinguish between situations of 'empty array'
        and of 'array of empty strings'.
    """

    def encode(self, strs: [str]) -> str:
        """ Encodes a list of strings to a single string.
        Time complexity: O(N)
        Space complexity: O(1)
        """
        if not strs:
            return chr(258)
        return chr(259).join(strs)

    def decode(self, s: str) -> [str]:
        """ Decodes a single string to a list of strings.
        Time complexity: O(N)
        Space complexity: O(1)
        """
        if s == chr(258):
            return None
        return s.split(chr(259))


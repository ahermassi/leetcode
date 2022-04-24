""" Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and
is decoded back to the original list of strings. """


class CodecV1:
    """ Naive solution here is to join strings using delimiters.
        What to use as a delimiter? Each string may contain any possible characters out of 256 valid ascii characters.
    """

    def encode(self, strs):
        """ Encodes a list of strings to a single string.
        Time complexity: O(N), where N is a number of strings in the input array
        Space complexity: O(1)
        """
        return chr(258).join(strs)

    def decode(self, s):
        """ Decodes a single string to a list of strings.
        Time complexity: O(N), O(N), where N is a number of strings in the input array
        Space complexity: O(1)
        """
        return s.split(chr(258))

# Video explanation: https://www.youtube.com/watch?v=B1k_sxOSgv8


class CodecV2:
    """ This approach doesn't depend on the set of input characters, and hence is more versatile and effective than
        Approach 1.
        Data stream is divided into chunks. Each chunk is preceded by its size and '#' delimiter between the length and
        the actual string. It acts as a boundary to show where the length string ends when the length has multiple
        digits and/or the string itself starts with a digit. If we know all substring are shorter than 10 characters,
        then we wouldn't have to use any separator like '#'.
    """

    def encode(self, strs: [str]) -> str:
        """ Encode a list of strings to a single string.
            Iterate over the array of strings. For each string, compute its length and append it to the encoded string:
            Information about chunk size and chunk itself.
        Time complexity: O(N)
        Space complexity: O(1)
        """
        res = []
        for s in strs:
            res.extend([str(len(s)), '#', s])
        return ''.join(res)

    def decode_v1(self, s: str) -> [str]:
        """ Decode a single string to a list of strings.
        Time complexity: O(N)
        Space complexity: O(1)
        """
        n, res = len(s), []
        i = 0
        while i < n:
            j = i
            while s[j] != '#':
                j += 1
            length = int(s[i:j])
            res.append(s[j + 1:j + 1 + length])
            i = j + 1 + length
        return res


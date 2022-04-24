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


class CodecV2:
    """ This approach doesn't depend on the set of input characters, and hence is more versatile and effective than
        Approach 1.
        Data stream is divided into chunks. Each chunk is preceded by its size.
    """

    def encode(self, strs: [str]) -> str:
        """ Encodes a list of strings to a single string.
            Iterate over the array of strings
            For each string, compute its length
            Append to encoded string: information about chunk size and chunk itself.
        Time complexity: O(N)
        Space complexity: O(1)
        """
        res = []
        for s in strs:
            res.extend([str(len(s)), ':', s])
        return ''.join(res)

    def decode_v1(self, s: str) -> [str]:
        """ Decodes a single string to a list of strings.
        Time complexity: O(N)
        Space complexity: O(1)
        """
        i, n, res = 0, len(s), []
        while i < n:
            j = i
            while s[j] != ':':
                j += 1
            size = int(s[i:j])
            res.append(s[j + 1:j + 1 + size])
            i = j + size + 1
        return res

    def decode_v2(self, s: str) -> [str]:
        """ Decodes a single string to a list of strings.
        Time complexity: O(N)
        Space complexity: O(1)
        """
        i, n, res = 0, len(s), []
        while i < n:
            index = s.find(':', i)
            size = int(s[i:index])
            res.append(s[index + 1:index + 1 + size])
            i = index + 1 + size
        return res


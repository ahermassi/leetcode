""" Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and
is decoded back to the original list of strings. """


class CodecV1:
    """ We often use a delimiter, which is a special character or sequence of characters that we insert between each
         string when we combine them into one. The key thing about a delimiter is that it must be a character or
         sequence of characters that doesn't occur in the strings we're encoding. This allows us to correctly separate
         the strings when we decode them.

         If the strings we're encoding could contain any ASCII character, then we can't use an ASCII character as the
         delimiter, because we wouldn't know whether that character is part of a string or a delimiter.

         That's where the idea of a non-ASCII delimiter comes in. There are many more characters available than just
         the ones in the ASCII set. Unicode is a character encoding standard that includes virtually every character
         from every writing system in the world, plus many symbols, control characters, and more. There are many
         Unicode characters that are not commonly used in text, and we can use one of these as our delimiter.

         This non-ASCII delimiter approach is simple and effective as long as we can be sure that the delimiter
         character won't appear in the strings we're encoding.
    """

    def encode(self, strs):
        """ Encodes a list of strings to a single string.

        Time complexity: O(N), where N is the total number of characters across all strings in the input list
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


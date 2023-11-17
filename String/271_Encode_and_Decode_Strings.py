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
    """ Chunked transfer encoding is a method used in data communication protocols to send data in self-contained
         chunks, each of which is accompanied by its length or size. In the context of our problem, this technique can
         be very useful.

         In the encoding process, instead of just joining all the strings together with a delimiter, we would precede
         each string with its length, followed by a delimiter, and then the string itself. This way, even if the string
         contains the delimiter, we can correctly identify the string boundaries.

         When we decode the encoded string, we know that the first item before the delimiter is the length of the string.

         The advantage of this method is that it doesn't matter what characters our string consists of. It could include
         the delimiter, or any other special or non-ASCII characters, and we would still correctly encode and decode
         the list of strings. This is because we always know where each string starts and ends, thanks to the length
         prefix. Numbers being in the string can't confuse the algorithm either since the number characters would be
         after the delimiter

         Suppose we have the following list of strings: ["Hello", "World", "/:Example/:"].

         For the encoding, we take each string's length, followed by a delimiter (we'll use $), and then the string
         itself. After processing all strings, the encoded string becomes 5$Hello5$World11$/:Example/:

        For the decoding process, we start reading the encoded string
        First, we read until we encounter $, which gives us 5. This tells us that the length of the first string is 5.
        So, we read the next 5 characters to get "Hello".
        Next, we again read until $ to get 5, indicating that our next string is of length 5. Reading the next
        5 characters gives us "World".
        Finally, reading until the next $ gives us 11. Reading the next 11 characters gives us "/:Example/:".
        After processing the whole encoded string, we are left with the original list of strings:
        ["Hello", "World", "/:Example/:"]
    """

    def encode(self, strs: [str]) -> str:
        """ Encode a list of strings to a single string.

            Iterate over the array of strings. For each string, compute its length and append it to the encoded string:
            Information about chunk size and chunk itself.

        Time complexity: O(N), where N is the total number of characters across all strings in the input list
        Space complexity: O(k), where k is the number of strings. For each word, we are using some space for the length
        and delimiter.
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
        i, n, res = 0, len(s), []
        while i < n:
            j = i
            while s[j] != '#':
                j += 1
            length = int(s[i:j])
            res.append(s[j + 1:j + 1 + length])
            i = j + 1 + length
        return res
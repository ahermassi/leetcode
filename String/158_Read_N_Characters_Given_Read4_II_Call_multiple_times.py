""" Given a file and assume that you can only read the file using a given method read4, implement a method read to
read n characters. Your method read may be called multiple times.

Method read4:

The API read4 reads four consecutive characters from file, then writes those characters into the buffer array buf4.

The return value is the number of actual characters read.

Note that read4() has its own file pointer, much like FILE *fp in C. """


def read4(buf):
    return 0  # Dummy return value


class SolutionV1(object):
    """ The idea is to create an internal buffer 'internal_buf' and every time we we call read(n), we read from
        'internal_buf' first until all characters are consumed. To do this, we need 2 more variables 'int_buf_counter'
        and 'int_buf_pointer', which track the actual size of 'internal_buf' and the index of next character to read
        from 'internal_buf'. Afterwards, we call read4 to read characters into 'internal_buf'. So when we call read(n),
        we read from 'internal_buf' starting from 'int_buf_pointer'. Once int_buf_pointer == int_buf_counter, we finish
        reading from the internal buffer and we have to call read4 to refill 'internal_buf' and read from it again.

        What is the difference between call once (question 157) and call multiple times?
        Suppose we have 4 chars "a, b, c, d" in the file, and we want to call the function twice like this:
        read(buf, 1); // should return 1 and buffer's content is 'a'
        read(buf, 3); // should return 3 and buffer's content is 'b, c, d'
        However, notice that all the 4 chars will be consumed in the first call. So the tricky part of this question is
        how to preserve the remaining 'b, c, d' to the second call.
        When we call read4, which reads 4 bytes into the buffer passed to it as argument, we might read more than we
        need. So we want to store those bytes in the structure, and next time we call read it will start from those
        stored bytes and then read more from the file.
        Call once: Assume we are always going to read from the start of the file/buffer.
        Call multiple times: Start reading from where we left off. This means that we have to store the last index
        (pointer) where we stopped and store the read but not copied bytes to the buffer.

    Time complexity: O(N)
    Space complexity: O(1)
    """

    def __init__(self):
        self.internal_buf = [''] * 4  # Stores bytes read when we call read4
        self.int_buf_pointer = 0  # Points to the next reading position in internal_buf. It is always < 4.
        self.int_buf_counter = 0  # Counts number of characters copied from internal_buf to the buffer in read(buf, n)

    def read(self, buf, n):
        write_index = 0
        while write_index < n:
            # Only if int_buf_pointer did not reach the end of internal_buf we can copy bytes from internal_buf to
            # final buffer buf. Using read4 we could have read more than n bytes in the previous call, in which case
            # we need to first continue reading from internal_buf.
            if self.int_buf_pointer < self.int_buf_counter:
                buf[write_index] = self.internal_buf[self.int_buf_pointer]
                self.int_buf_pointer += 1
                write_index += 1
            else:  # Refill the internal buffer if all its chars have been read and 'transferred' to buf
                self.int_buf_counter = read4(self.internal_buf)
                # Reset int_buf_pointer. This means all chars that were read into internal_buf are at standby and
                # waiting to be copied/transferred to buf
                self.int_buf_pointer = 0
                if self.int_buf_counter == 0:  # If no more characters we can read, break.
                    break
        return write_index


class SolutionV2(object):
    """ Same algorithm re-written differently. We don't need to reset 'int_buf_pointer' to 0 in the end. Instead, we
    check whether int_buf_pointer == int_buf_counter in the beginning, which can be more intuitive.

    Time complexity: O(N)
    Space complexity: O(1)
    """

    def __init__(self):
        self.internal_buf = [''] * 4  # Stores bytes read when we call read4
        self.int_buf_pointer = 0  # Points to the next reading position in internal_buf. It is always < 4.
        self.int_buf_counter = 0  # Counts number of characters copied from internal_buf to the buffer in read(buf, n)

    def read(self, buf, n):
        write_index = 0
        while write_index < n:
            # Refill the internal buffer if all its chars have been read and 'transferred' to buf
            if self.int_buf_pointer == self.int_buf_counter:
                self.int_buf_counter = read4(self.internal_buf)
                # Reset int_buf_pointer. This means all chars that were read into internal_buf are at standby and
                # waiting to be copied/transferred to buf
                self.int_buf_pointer = 0
                if self.int_buf_counter == 0:  # If no more characters we can read, break.
                    break
            # Only if int_buf_pointer did not reach the end of internal_buf we can copy bytes from internal_buf to
            # final buffer buf. Using read4 we could have read more than n bytes in the previous call, in which case
            # we need to first continue reading from internal_buf.
            buf[write_index] = self.internal_buf[self.int_buf_pointer]
            self.int_buf_pointer += 1
            write_index += 1
        return write_index

""" Given a file and assume that you can only read the file using a given method read4, implement a method to read n
characters. """


def read4(buf):
    pass


def read(buf, n):
    """ This function is to read n characters into buf only 4 characters at a time using read4() function.
    """
    write_index = 0
    while write_index < n:
        temp = [''] * 4  # Temporary buffer to read characters into
        chars_read = read4(temp)
        if not chars_read:  # This check is used for cases when we attempt to read more characters than the actual
            # length of the file, in which case read4 returns chars_read = 0
            break
        chars_read = min(chars_read, n - write_index)  # This is for cases when the remaining number of characters in
        # the file is greater than the remaining number of characters we want to read. Example: 'leetcode', n = 5.
        # First pass we read 4 characters 'leet', second pass read4 reads 'code' and returns chars_read = 4, but we
        # want to read only one character more: 5 - 4 = 1
        # Even if we read 4 chars from read4, we don't want to exceed n and only want to read chars till n
        buf[write_index:] = temp[:chars_read]  # Read that exact number of characters from temp and append it to buf
        write_index += chars_read
    return write_index


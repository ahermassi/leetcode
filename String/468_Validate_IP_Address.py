""" Given a string IP, return "IPv4" if IP is a valid IPv4 address, "IPv6" if IP is a valid IPv6 address or "Neither"
if IP is not a correct IP of any type.

A valid IPv4 address is an IP in the form "x1.x2.x3.x4" where 0 <= xi <= 255 and xi cannot contain leading zeros.
For example, "192.168.1.1" and "192.168.1.0" are valid IPv4 addresses but "192.168.01.1", while "192.168.1.00" and
"192.168@1.1" are invalid IPv4 addresses.

A valid IPv6 address is an IP in the form "x1:x2:x3:x4:x5:x6:x7:x8" where:

1 <= xi.length <= 4
xi is a hexadecimal string which may contain digits, lower-case English letter ('a' to 'f') and upper-case English
letters ('A' to 'F').
Leading zeros are allowed in xi.
For example, "2001:0db8:85a3:0000:0000:8a2e:0370:7334" and "2001:db8:85a3:0:0:8A2E:0370:7334" are valid IPv6 addresses,
while "2001:0db8:85a3::8A2E:037j:7334" and "02001:0db8:85a3:0000:0000:8a2e:0370:7334" are invalid IPv6 addresses. """


def validIPAddress(IP):
    """ Both IPv4 and IPv6 addresses are composed of several substrings separated by certain delimiter, and each of the
        substrings is of the same format. Therefore, intuitively, we could break down the address into chunks, and then
        verify them one by one. The address is valid if and only if each of the chunks is valid.
        For the IPv4 address, we split IP into 4 chunks by the delimiter '.', while for IPv6 address we split IP into
        8 chunks by the delimiter ':'
        For each substring of IPv4 address, we check if it is an integer between 0 - 255 and there is no leading zeros.
        For each substring of IPv6 address, we check if it's a hexadecimal number of length 1 - 4.
    Time complexity: O(N)
    Space complexity: O(1)
    """

    def validate_ipv4(parts):
        for part in parts:
            if not part.isdigit():
                return 'Neither'
            if not 0 <= int(part) <= 255:
                return 'Neither'
            if part[0] == '0' and len(part) != 1:
                return 'Neither'
        return 'IPv4'

    def validate_ipv6(parts):
        hexdigits = '0123456789abcdefABCDEF'
        for part in parts:
            if not 1 <= len(part) <= 4:
                return 'Neither'
            for c in part:
                if c not in hexdigits:
                    return 'Neither'
        return 'IPv6'

    if IP.count('.') == 3:
        return validate_ipv4(IP.split('.'))
    if IP.count(':') == 7:
        return validate_ipv6(IP.split(':'))
    return 'Neither'

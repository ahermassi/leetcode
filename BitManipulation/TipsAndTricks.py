#  Shifting by n bits to the right is equivalent to dividing by 2^n
#  x = 100101 = 37; x >> 3 = 000100 = 4 ~= 37 / (2^3)

#  Shifting by n bits to the left is equivalent to multiplying b 2^n
#  x = 100101 = 37; x << 3 = 100101000 = 296 = 37 * (2^3)

# Shifting by k bits to the right brings the kth bit to the rightmost index (k is 0-based)
# Therefore, to find the value of kth bit: x >> k & 1
# x = 100101, k = 2; x >> 2 = 001001; x >> 2 & 1 = 1 which is the bit at index 2

# x & (x -1 1) equals x with its lowest set bit erased
#  x = 00101100; x - 1= 00101011; x & (x - 1) = 00101000

# Most bit manipulations involve the use of a bit mask, which is a string of bits applied to the binary representation
# of the integer we want to manipulate.


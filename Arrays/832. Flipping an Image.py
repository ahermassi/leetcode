def flip_and_invert_image(A):
    """
    :type A: List[List[int]]
    :rtype: List[List[int]]
    Time complexity: O(N) where N is the number of elements in A (number of lists)
    """
    flipped = [lst[::-1] for lst in A]
    invert = lambda x: 0 if x == 1 else 1
    inverted = [list(map(invert, row)) for row in flipped]
    return inverted


if __name__ == '__main__':
    A = [[1,1,0],[1,0,1],[0,0,0]]
    inverted = flip_and_invert_image(A)
    print('Array before inversion: ', A)
    print('Array After inversion: ', inverted)

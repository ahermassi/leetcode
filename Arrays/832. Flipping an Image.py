def flip_and_invert_image(A):
    """
    :type A: List[List[int]]
    :rtype: List[List[int]]
    Time complexity: O(N) where N is the number of elements in A (number of lists)
    Space complexity: O(N) where N is the number of A elements, since a new array is introduced to hold the result
    """
    flipped = [lst[::-1] for lst in A]
    invert = lambda x: 0 if x == 1 else 1
    inverted = [list(map(invert, row)) for row in flipped]
    return inverted


def flip_and_invert_image_v2(A):  # Constant space
    """
    :type A: List[List[int]]
    :rtype: List[List[int]]
    Time complexity: O(N) where N is the number of elements in A (number of lists)
    Space complexity: O(1) since the transformation is in-place
    """
    invert = lambda x: 0 if x == 1 else 1
    A = [list(map(invert, row[::-1])) for row in A]
    return A


if __name__ == '__main__':
    A = [[1,1,0],[1,0,1],[0,0,0]]
    inverted = flip_and_invert_image_v2(A)
    print('Array before inversion: ', A)
    print('Array After inversion: ', inverted)

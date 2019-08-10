""" You are climbing a stair case. It takes n steps to reach to the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top? """


def climb_stairs_v1(n):
    """ This is the classic/intuitive recursive solution. However, it returns TLE.
    Time complexity: O(2 ** n), size of recursion tree will be 2 ** n
    Space complexity: O(n)
    """
    if n == 1:
        return 1
    if n == 2:
        return 2
    return climb_stairs_v1(n - 1) + climb_stairs_v1(n - 2)







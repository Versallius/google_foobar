# foobar.withgoogle.com
# Level 5 extra problem


'''
Disorderly Escape
=================

Oh no! You've managed to free the bunny workers and escape Commander Lambdas exploding space station, but Lambda's team of elite starfighters has flanked your ship. If you dont jump to hyperspace, and fast, youll be shot out of the sky!

Problem is, to avoid detection by galactic law enforcement, Commander Lambda planted the space station in the middle of a quasar quantum flux field. In order to make the jump to hyperspace, you need to know the configuration of celestial bodies in the quadrant you plan to jump through. In order to do *that*, you need to figure out how many configurations each quadrant could possibly have, so that you can pick the optimal quadrant through which youll make your jump. 

There's something important to note about quasar quantum flux fields' configurations: when drawn on a star grid, configurations are considered equivalent by grouping rather than by order. That is, for a given set of configurations, if you exchange the position of any two columns or any two rows some number of times, youll find that all of those configurations are equivalent in that way -- in grouping, rather than order.

Write a function solution(w, h, s) that takes 3 integers and returns the number of unique, non-equivalent configurations that can be found on a star grid w blocks wide and h blocks tall where each celestial body has s possible states. Equivalency is defined as above: any two star grids with each celestial body in the same state where the actual order of the rows and columns do not matter (and can thus be freely swapped around). Star grid standardization means that the width and height of the grid will always be between 1 and 12, inclusive. And while there are a variety of celestial bodies in each grid, the number of states of those bodies is between 2 and 20, inclusive. The solution can be over 20 digits long, so return it as a decimal string.  The intermediate values can also be large, so you will likely need to use at least 64-bit integers.

For example, consider w=2, h=2, s=2. We have a 2x2 grid where each celestial body is either in state 0 (for instance, silent) or state 1 (for instance, noisy).  We can examine which grids are equivalent by swapping rows and columns.

00
00

In the above configuration, all celestial bodies are "silent" - that is, they have a state of 0 - so any swap of row or column would keep it in the same state.

00 00 01 10
01 10 00 00

1 celestial body is emitting noise - that is, has a state of 1 - so swapping rows and columns can put it in any of the 4 positions.  All four of the above configurations are equivalent.

00 11
11 00

2 celestial bodies are emitting noise side-by-side.  Swapping columns leaves them unchanged, and swapping rows simply moves them between the top and bottom.  In both, the *groupings* are the same: one row with two bodies in state 0, one row with two bodies in state 1, and two columns with one of each state.

01 10
01 10

2 noisy celestial bodies adjacent vertically. This is symmetric to the side-by-side case, but it is different because there's no way to transpose the grid.

01 10
10 01

2 noisy celestial bodies diagonally.  Both have 2 rows and 2 columns that have one of each state, so they are equivalent to each other.

01 10 11 11
11 11 01 10

3 noisy celestial bodies, similar to the case where only one of four is noisy.

11
11

4 noisy celestial bodies.

There are 7 distinct, non-equivalent grids in total, so solution(2, 2, 2) would return 7.
'''

'''
Math problem: 
Find the number of distinct orbits of a w x h grid with s colors in every cell over permutations over rows and columns. 

The Polya enumeration theorem can help. 
For a symmetry group Sn (a set of n elements symmetric about any permutation of them) acting on a set X, the number of distinct orbits is: 
n_orbits = 1/|Sn| * sum over elements of Sn: s^ck(g)
where: |Sn| is the number of symmetry operations in Sn, and ck(g) is the number of cycles of size k in the cycle decomposition of symmetry operation g which is an of Sn. 

However the 2D situation is slightly more complicated because we need the Cartesian product of two cycle index polynomials. 
Luckily a neat outline of the mathematics is available here: https://franklinvp.github.io/2020-06-05-PolyaFooBar/

To implement the algorithm to compute the final result, we note the following: 

1. factorials and gcds are quite annoying to compute, and the final computation requires a lot of them. Therefore we pre-compute them in a lookup table to save on the recursive calls. 
2. The solution require generating all unique partitions of w and h. This is a non-trivial problem but we borrow the algorithm from https://arxiv.org/abs/0909.2331

Therefore this is mostly a dynamic programming problem. 

Step 1: pre-compute all factorials and pairwise gcds up to max(w, h). 
Step 2: generate all unique partitions of w and h. 
Step 3: iterate through partitions of w and h, computing the term for every case. 

'''

from collections import Counter

# Step 1: pre-compute factorials and pairwise gcds
def gen_factorials(n): 
    '''
    n: integer > 0
    generates factorials by storing values and multiplying the previous value by current multiple

    return factorials: list of factorials such that factorials[n] = n!
    '''
    factorials = [1] # 0! = 1 and for padding coordinates
    for i in range(1, n+1): 
        factorials.append(factorials[i-1]*i)
    
    return factorials

def gen_gcds(n): 
    '''
    n: integer > 0
    generates gcds using Euclidean algorithm

    return gcds: array of pairwise gcds such that gcds[x][y] = gcd(x, y) for x, y in integers > 0
    '''
    gcds = [[0 for _ in range(n+1)] for _ in range(n+1)]

    for i in range(n+1): 
        for j in range(i, n+1): 
            if i == 0 or j == 0: # extra row and column for padding coordinates
                gcds[i][j] = 0
                gcds[j][i] = 0
            elif i == 1 or j == 1: 
                gcds[i][j] = 1
                gcds[j][i] = 1
            elif i == j: 
                gcds[i][j] = i
            else: 
                gcds[i][j] = gcds[i][j-i]
                gcds[j][i] = gcds[i][j-i]

    return gcds

# Step 2: generate all unique partitions of w and h. also some functions to calculate intermediate results while we're here. 

def get_partitions(n):
    '''
    n: integer > 0
    iteratively generates all unique integer partitions of n

    return partitions: non-decreasing sorted list of unique partitions of n (each partition is itself a non-decreasing sorted list)

    Algorithm 4.1 AccelAsc from https://arxiv.org/abs/0909.2331
    '''
 
    k = 1 # in original algorithm k starts at 2, but they defined the partition as a1, a2, ... ak and here we have first index is 0
    a = [0 for i in range(n)]
    y = n - 1
    partitions = [] # to store results
    
    while k is not 0:
        k -= 1
        x = a[k]+1

        while 2*x <= y:
            a[k] = x
            y -= x
            k += 1

        l = k+1

        while x <= y:
            a[k] = x
            a[l] = y
            partition = a[:l+1]
            partitions.append(partition)
            x += 1
            y -= 1

        y = x+y-1
        a[k] = y+1
        
        partition = a[:k+1]
        partitions.append(partition)
    
    return partitions


    
def get_coefficient(part, n, factorials): 
    '''
    part: list of positive integers (may be obtained from get_partitions)
    n: sum(part). don't compute this because part is obtained from get_partitions(n) so n is already known. 
    factorials: list of factorials such that factorials[n] = n! (may be obtained from gen_factorials)

    return coeff: coefficient of each term in the summation, given by n! / product(k**i * i!) for k in part, i is the frequency of i and part is a partition of n. 
    '''
    
    coeff = factorials[n]
    for k, i in Counter(part).items(): 
        coeff = coeff // (k**i * factorials[i])

    return coeff

def get_power(w_part, h_part, gcds): 
    '''
    w_part: list of integers > 0, a partition of w
    h_part: list of integers > 0, a partition of h
    gcds: array of pairwise gcds such that gcds[x][y] = gcd(x, y) (may be obtained from gen_gcds)

    return power: the power that s is raised to in each term of the summation, given by sum over i in w_part and j in h_part: gcd(i, j)
    '''

    power = 0
    for i in w_part: 
        for j in h_part: 
            power += gcds[i][j]

    return power

# Step 3: compute the final result by iterating through partitions of w and h

def solution(w, h, s): 
    '''
    w: integer satisfying 1 <= w <= 12, number of columns of the celestial grid
    h: integer satisfying 1 <= h <= 12, number of rows of the celestial grid
    s: integer satisfying 2 <= s <= 20, number of states for each star in the celestial grid

    return n_orbits: string, decimal string representation of the number of unique configurations of the celestial grid
    '''

    n = max(w, h) # find how big to construct factorials and gcds
    factorials = gen_factorials(n)
    gcds = gen_gcds(n)

    w_parts, h_parts = get_partitions(w), get_partitions(h)
    
    n_orbits = 0
    for w_part in w_parts: 
        for h_part in h_parts: 
            n_orbits += get_coefficient(w_part, w, factorials) * get_coefficient(h_part, h, factorials) * (s ** get_power(w_part, h_part, gcds))
            

    n_orbits = n_orbits // (factorials[w]*factorials[h])

    return str(n_orbits)

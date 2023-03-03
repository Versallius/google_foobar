# foobar.withgoogle.com
# Level 3

'''
Fuel Injection Perfection
=========================

Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for the LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP -- and maybe sneak in a bit of sabotage while you're at it -- so you took the job gladly. 
Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. 
The fuel control mechanisms have three operations: 

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.

For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1
'''

''' 
Math problem: 

The 3 operations allowed are +1, -1 and /2. 
Clearly, /2 is the most efficient operation at getting closer toward 1. Therefore we should use it as often as possible. 
A naive algorithm simply chooses +1 or -1 to get toward the nearest number with the greatest power of 2 in its prime factorization, thereby allowing us to use /2 often. 

Example: 
15 is 2^4 - 1, so we choose +1 to get to 16 and /2 down to 1. 15 -> 16 -> 8 -> 4 -> 2 -> 1
13 is 2^2*3 + 1 or 2*7 - 1, so we choose to -1 because 12 has a higher power of 2. 13 -> 12 -> 6 -> 3 -> 2 -> 1

The exception to this rule is 3, where we choose -1 instead because although 4 has the larger power of 2, 3 -> 2 -> 1 is faster than 3 -> 4 -> 2 -> 1. 

Consider 3 cases: 

Case 1: n is even
Here we always /2, there is no situation in which moving away from a multiple of 2 is efficient. 

Case 2: n is 4k+1. 
Here we always choose -1, this way we can /2 twice. If we chose +1 here, we can only /2 once before we must use -1 again before /2. 

Case 3: n is 4k-1. 
Here unless n = 3 (in which case we chose -1 as described above), we always choose +1. This way we can /2 twice. 

'''

def solution_bin(n): 
    n = int(n)
    count = 0
    while n > 1: 
        # Case 1
        if n % 2 == 0: 
            n = n//2
        # Case 2 or Case 3 and n is 3
        elif n == 3 or n % 4 == 1: 
            n = n - 1
        # Case 3 and n is not 3
        else: 
            n = n + 1
        count += 1 
    return count

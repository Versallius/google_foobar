# foobar.withgoogle.com
# Level 5

'''
Dodge the Lasers!
=================

Oh no! You've managed to escape Commander Lambda's collapsing space station in an escape pod with the rescued bunny workers - but Commander Lambda isnt about to let you get away that easily. Lambda sent an elite fighter pilot squadron after you -- and they've opened fire!

Fortunately, you know something important about the ships trying to shoot you down. Back when you were still Lambda's assistant, the Commander asked you to help program the aiming mechanisms for the starfighters. They undergo rigorous testing procedures, but you were still able to slip in a subtle bug. The software works as a time step simulation: if it is tracking a target that is accelerating away at 45 degrees, the software will consider the targets acceleration to be equal to the square root of 2, adding the calculated result to the targets end velocity at each timestep. However, thanks to your bug, instead of storing the result with proper precision, it will be truncated to an integer before adding the new velocity to your current position.  This means that instead of having your correct position, the targeting software will erringly report your position as sum(i=1..n, floor(i*sqrt(2))) - not far enough off to fail Commander Lambdas testing, but enough that it might just save your life.

If you can quickly calculate the target of the starfighters' laser beams to know how far off they'll be, you can trick them into shooting an asteroid, releasing dust, and concealing the rest of your escape.  
Write a function solution(str_n) which, given the string representation of an integer n, returns the sum of (floor(1*sqrt(2)) + floor(2*sqrt(2)) + ... + floor(n*sqrt(2))) as a string. That is, for every number i in the range 1 to n, it adds up all of the integer portions of i*sqrt(2).

For example, if str_n was "5", the solution would be calculated as
floor(1*sqrt(2)) +
floor(2*sqrt(2)) +
floor(3*sqrt(2)) +
floor(4*sqrt(2)) +
floor(5*sqrt(2))
= 1+2+4+5+7 = 19
so the function would return "19".

str_n will be a positive integer between 1 and 10^100, inclusive. Since n can be very large (up to 101 digits!), using just sqrt(2) and a loop won't work. Sometimes, it's easier to take a step back and concentrate not on what you have in front of you, but on what you don't.
'''


'''
Math problem: 
Find the sum of a Beatty sequence S(alpha, n) = sum(floor(alpha*k)) for k in range(1, n+1) for some positive real number alpha


If alpha > 2: 
let beta = alpha - j where j in integers such that 2 > beta > 1
then S(alpha, n)    = S(beta, n) + j*sum(k) for k in range(1, n+1)
                    = S(beta, n) + j*n*(n+1) / 2

If 2 > alpha > 1: 
use Rayleigh's Theorem: there exists beta satisfying 1/alpha + 1/beta = 1 such that the sequences floor(alpha * n) and floor(beta * n) for n >= 1 partition the set of positive integers
then S(alpha, n) + S(beta, floor(floor(n*alpha)/beta))  = sum(k) for k in range(1, floor(n*alpha)+1)
                                                        = floor(n*alpha) * (floor(n*alpha) +1) / 2

Note that because beta = alpha / (alpha - 1), we get:
floor(floor(n*alpha)/beta) = floor(n*alpha) - n = floor((alpha-1)*n)

Therefore if we let m = floor((alpha-1)*n), we have :
S(alpha, n) + S(beta, m) = (m + n)(m + n + 1) / 2

When alpha = sqrt(2), beta = sqrt(2) / (sqrt(2) - 1) = 2 + sqrt(2)
We can combine the above 2 equations: 

S(sqrt(2), n)   = (m+n)(m+n+1)/2 - S(2+sqrt(2), m) # remember that m = floor((sqrt(2)-1)*n)
                = (m+n)(m+n+1)/2 - S(sqrt(2), m) - m(m+1) 

This recurrence relation in n allows us to reduce the argument n of S(sqrt(2), n) by a multiple of sqrt(2)-1 each time, so this algorithm will have a complexity of O(log n), suitable for this problem. 

'''

import math

# store first 100 digits of sqrt(2)-1 because we need extra precision and python floats don't store that many digits
# data source: https://apod.nasa.gov/htmltest/gifcity/sqrt2.1mil
decay_factor = 4142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727

def recursion(n): # same function as solution except it takes int as input and output
    if n == 0: # boundary conditions for recusion. need n = 0 for the recurrence because sometimes m = 0 (even though 0 is not a valid input to the original problem)
        return 0
    if n == 1: 
        return 1

    m = (decay_factor*n)//(10**100) # correct for the extra powers of 10 we introduced in decay_factor. can make this slightly more efficient by only using the digits we need, but this is simpler to implement
    return ((m+n)*(m+n+1))//2 - m*(m+1) - recursion(m)

def solution(str_n): 
    n = int(str_n)    
    return str(recursion(n))

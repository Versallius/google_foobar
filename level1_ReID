# foobar.withgoogle.com
# Level 1

'''
Re-ID
=====
There's some unrest in the minion ranks: minions with ID numbers like "1", "42", and other "good" numbers have been lording it over the poor minions who are stuck with more boring IDs. To quell the unrest, Commander Lambda has tasked you with reassigning everyone new random IDs based on a Completely Foolproof Scheme. 
Commander Lambda has concatenated the prime numbers in a single long string: "2357111317192329...". Now every minion must draw a number from a hat. That number is the starting index in that string of primes, and the minion's new ID number will be the next five digits in the string. So if a minion draws "3", their ID number will be "71113". 
Help the Commander assign these IDs by writing a function solution(n) which takes in the starting index n of Lambda's string of all primes, and returns the next five digits in the string. Commander Lambda has a lot of minions, so the value of n will always be between 0 and 10000.
'''

# the only challenge here is constructing the concatenated primes string. 

import numpy as np

def is_prime(x): 
    for factor in range(2, int(np.floor(np.sqrt(x)))+1): 
        if x % factor is 0: 
            return False
    return True

def gen_string(length): 
    p_string = ''
    for n in range(2,50000): 
        if is_prime(n): 
            p_string += str(n)
        if len(p_string) > length+10: 
            break
    return p_string


def solution(i):
    p_string = gen_string(i)
    return p_string[i:i+5]

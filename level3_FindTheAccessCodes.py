# foobar.withgoogle.com
# Level 3

'''
Find the Access Codes
=====================

In order to destroy Commander Lambda's LAMBCHOP doomsday device, you'll need access to it. But the only door leading to the LAMBCHOP chamber is secured with a unique lock system whose number of passcodes changes daily. Commander Lambda gets a report every day that includes the locks' access codes, but only the Commander knows how to figure out which of several lists contains the access codes. You need to find a way to determine which list contains the access codes once you're ready to go in. 
Fortunately, now that you're Commander Lambda's personal assistant, Lambda has confided to you that all the access codes are "lucky triples" in order to make it easier to find them in the lists. A "lucky triple" is a tuple (x, y, z) where x divides y and y divides z, such as (1, 2, 4). With that information, you can figure out which list contains the number of access codes that matches the number of locks on the door when you're ready to go in (for example, if there's 5 passcodes, you'd need to find a list with 5 "lucky triple" access codes).
Write a function solution(l) that takes a list of positive integers l and counts the number of "lucky triples" of (li, lj, lk) where the list indices meet the requirement i < j < k.  The length of l is between 2 and 2000 inclusive.  The elements of l are between 1 and 999999 inclusive.  The solution fits within a signed 32-bit integer. Some of the lists are purposely generated without any access codes to throw off spies, so if no triples are found, return 0. 
For example, [1, 2, 3, 4, 5, 6] has the triples: [1, 2, 4], [1, 2, 6], [1, 3, 6], making the solution 3 total.

'''

'''
# A naive solution would be to brute force the problem as follows: 

def count_lucky(l): 
    #l.sort()
    lucky_list = []
    for i_left, left in enumerate(l[0:-2]): 
        for i_middle, middle in enumerate(l[i_left+1:-1]): 
            if middle % left == 0: 
                for i_right, right in enumerate(l[i_left+i_middle+2::]):
                    if right % middle == 0: 
                        #print((left, middle, right))
                        lucky_list.append((left, middle, right))
    
    #lucky_list = list(dict.fromkeys(lucky_list))
    return len(lucky_list)

# But this is not optimal, as it runs in O(n^3) time. 
# We can do better by first searching left and middle first in O(n^2) time, followed by searching the middle and right in O(n^2) time. This way we are overall O(n^2). 
# We use a lookup table to store the information from the first search. 
'''
def count_lucky(l):

    mid_lookup = [0]*(len(l)-2)
    for i_middle, middle in enumerate(l[1:-1]): 
        right_count = 0
        for i_right, right in enumerate(l[i_middle + 2::]): 
            if right % middle == 0: 
                right_count += 1
        mid_lookup[i_middle] = right_count
    
    lucky_count = 0
    for i_left, left in enumerate(l[0:-2]): 
        for i_middle, middle in enumerate(l[i_left + 1: -1]): 
            if middle % left == 0: 
                lucky_count += mid_lookup[i_left + i_middle]
    
    return lucky_count

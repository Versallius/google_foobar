# foobar.withgoogle.com
# some ARG
# Level 2

'''
Ion Flux Relabeling
===================

Oh no! Commander Lambda's latest experiment to improve the efficiency of the LAMBCHOP doomsday device has backfired spectacularly. The Commander had been improving the structure of the ion flux converter tree, but something went terribly wrong and the flux chains exploded. Some of the ion flux converters survived the explosion intact, but others had their position labels blasted off. Commander Lambda is having her henchmen rebuild the ion flux converter tree by hand, but you think you can do it much more quickly -- quickly enough, perhaps, to earn a promotion!
Flux chains require perfect binary trees, so Lambda's design arranged the ion flux converters to form one. To label them, Lambda performed a post-order traversal of the tree of converters and labeled each converter with the order of that converter in the traversal, starting at 1. For example, a tree of 7 converters would look like the following:

   7
 3   6
1 2  4 5

Write a function solution(h, q) - where h is the height of the perfect tree of converters and q is a list of positive integers representing different flux converters - which returns a list of integers p where each element in p is the label of the converter that sits on top of the respective converter in q, or -1 if there is no such converter.  For example, solution(3, [1, 4, 7]) would return the converters above the converters at indexes 1, 4, and 7 in a perfect binary tree of height 3, which is [3, 6, -1].
The domain of the integer h is 1 <= h <= 30, where h = 1 represents a perfect binary tree containing only the root, h = 2 represents a perfect binary tree with the root and two leaf nodes, h = 3 represents a perfect binary tree with the root, two internal nodes and four leaf nodes (like the example above), and so forth.  The lists q and p contain at least one but no more than 10000 distinct integers, all of which will be between 1 and 2^h-1, inclusive.
'''

def find_parent(overall_h, i): 
    # first find minimum x such that 2^x > i. x must be less than 30. 
    # this is to find the top of the subtree this number is in
    for x in range(31): 
        if 2**x > i: 
            subtree_root = 2**x - 1
            subtree_h = x
            break
    
    to_search = subtree_root - i
    search_history = [to_search]
    
    # now search path from root of the subtree to this number: 
    # going left requires -2**x, going right requires -1. 
    
    if i == 2**overall_h - 1: 
        return -1 # if the query node is also the main tree's root, then return -1
    
    for x in range(subtree_h-1, -1, -1): 
        if to_search >= 2**x: 
            to_search -= 2**x
            search_history.append(to_search)
        elif to_search > 0: 
            to_search -= 1
            search_history.append(to_search)
    if search_history[0] is not 0: 
        return search_history[-2]+i # parent node is the second last node in the path. 
    else: 
        return i + 2**subtree_h

def solution(h, q):
    output = []
    for query in list(q): 
        output.append(find_parent(h, query))
    return output

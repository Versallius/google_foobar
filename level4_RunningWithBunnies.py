# foobar.withgoogle.com
# Level 4


'''
Running with Bunnies
====================

You and the bunny workers need to get out of this collapsing death trap of a space station -- and fast! Unfortunately, some of the bunnies have been weakened by their long work shifts and can't run very fast. Their friends are trying to help them, but this escape would go a lot faster if you also pitched in. The defensive bulkhead doors have begun to close, and if you don't make it through in time, you'll be trapped! You need to grab as many bunnies as you can and get through the bulkheads before they close. 
The time it takes to move from your starting point to all of the bunnies and to the bulkhead will be given to you in a square matrix of integers. Each row will tell you the time it takes to get to the start, first bunny, second bunny, ..., last bunny, and the bulkhead in that order. The order of the rows follows the same pattern (start, each bunny, bulkhead). The bunnies can jump into your arms, so picking them up is instantaneous, and arriving at the bulkhead at the same time as it seals still allows for a successful, if dramatic, escape. (Don't worry, any bunnies you don't pick up will be able to escape with you since they no longer have to carry the ones you did pick up.) You can revisit different spots if you wish, and moving to the bulkhead doesn't mean you have to immediately leave -- you can move to and from the bulkhead to pick up additional bunnies if time permits.
In addition to spending time traveling between bunnies, some paths interact with the space station's security checkpoints and add time back to the clock. Adding time to the clock will delay the closing of the bulkhead doors, and if the time goes back up to 0 or a positive number after the doors have already closed, it triggers the bulkhead to reopen. Therefore, it might be possible to walk in a circle and keep gaining time: that is, each time a path is traversed, the same amount of time is used or added.
Write a function of the form solution(times, time_limit) to calculate the most bunnies you can pick up and which bunnies they are, while still escaping through the bulkhead before the doors close for good. If there are multiple sets of bunnies of the same size, return the set of bunnies with the lowest worker IDs (as indexes) in sorted order. The bunnies are represented as a sorted list by worker ID, with the first bunny being 0. There are at most 5 bunnies, and time_limit is a non-negative integer that is at most 999.

For instance, in the case of
[
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]
and a time limit of 1, the five inner array rows designate the starting point, bunny 0, bunny 1, bunny 2, and the bulkhead door exit respectively. You could take the path:

Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit

With this solution, you would pick up bunnies 1 and 2. This is the best combination for this space station hallway, so the solution is [1, 2].

'''



import copy
import itertools

def shortest_path(times): 
  # Bellman-Ford algorithm for finding shortest paths
  # Normally Bellman-Ford requires stipulating a starting location
  # Here we loop the algorithm to find pairwise shortest distances between all nodes in graph

  mintimes = copy.deepcopy(times) 
  has_neg_cyc = False

  nodes = list(range(len(times)))
  edges = list(itertools.permutations(range(len(times)), 2)) # fully connected graph
  
  for _ in range(len(times)-1): 
    for edge in edges: 
      initial, final = edge[0], edge[1]
      other_nodes = [i for i in nodes if i not in edge]
      for node in other_nodes: 
          mintimes[initial][final] = min(mintimes[initial][final], mintimes[initial][node] + mintimes[node][final])

  for edge in edges:
    initial, final = edge[0], edge[1]
    dists = mintimes[0]  
    if dists[initial] + times[initial][final] < dists[final]: 
      has_neg_cyc = True

  return mintimes, has_neg_cyc


def get_path_time(bunnies, mintimes): 
  # Minimum path to save this set of bunnies
  path_time = 0
  for i, bunny in enumerate(bunnies): 
    if i == 0: 
      previous = 0
    else: 
      previous = bunnies[i-1]+1
    path_time += mintimes[previous][bunny+1]
  path_time += mintimes[bunny+1][-1]
  return path_time

def solution(times, time_limit): 
  n_bunnies = len(times)-2
  mintimes, has_neg_cyc = shortest_path(times)
  
  # if the graph has the negative valued cycle, then we can endlessly loop this for infinite time and save all bunnies
  if has_neg_cyc: 
    return list(range(n_bunnies))

  # otherwise, we check all combinations of bunnies that can be saved to see which are possible
  for n_saved in range(n_bunnies, 0, -1): 
    to_save_list = list(itertools.permutations(range(n_bunnies), n_saved))
    for to_save in to_save_list: 
    
      path_time = get_path_time(to_save, mintimes)
      if path_time <= time_limit: 
        return list(sorted(to_save))


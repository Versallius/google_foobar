# foobar.withgoogle.com
# Level 4

'''
Bringing a Gun to a Trainer Fight
=================================

Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers! Fortunately, you grabbed a beam weapon from an abandoned storeroom while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the bunny trainers: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!
Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either you or the bunny trainer, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.
The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite trainer were positioned in a room with dimensions [3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite trainer (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite trainer with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite trainer with a total shot distance of sqrt(5).
'''

'''
The intuition here is that when shooting at an object by reflecting at a mirror, you are shooting at their reflection in the mirror. 
For example, if you are at (0, 0) and there is a mirror at x = 1. If you shoot in direction (1, 1) to hit a target at (0, 2), you are aiming at (2, 2), the reflection of the target in the mirror. 
Therefore rather than trying to find all possible ways to reflect the beam around the room, it's easier to tile the room and aim at all the reflections. 

Finally, storing target locations using polar coordinates is a nice optimization. 
'''

import math

def solution(room_dim, your_pos, train_pos, max_dist): 

    locations = (([], []), ([], [])) # (you_X, you_Y), (train_X, train_Y)
    yous_dict = {}
    allowed_list = []

    # calculates positions of you and trainer after reflecting on mirrors (tiling). coordinates have 0 < x/y < x/y_dim, so people cannot be exactly on the wall. this means theres exactly 1 reflection of you and train in each tile. 

    for is_train, location in enumerate(locations): # iterate through you (0), train (1)

        for coord_id, axis_coord in enumerate(location): # iterate through X (0), Y (1)
            
            to_tile = (max_dist//room_dim[coord_id]) + 1 # how many times to tile: estimate based on max distance
            for tile in range(-to_tile, to_tile+1): # infer cartesian coordinates of you and trainer by looking at each tile
                
                if not is_train: 
                    axis_coord.append(room_dim[coord_id]*(tile+tile%2) - 2*(tile%2)*your_pos[coord_id]) # if reflecting even number of tiles, position is just based on translation, else if odd number of tiles correct with a reflection
                else: 
                    axis_coord.append(room_dim[coord_id]*(tile+tile%2) + train_pos[coord_id] - your_pos[coord_id] - 2*(tile%2)*train_pos[coord_id])

        # store positions of you and trainer using polar coordinates (gradient stored in radians)
        for x in location[0]: 
            for y in location[1]: 
                grad = math.atan2(y, x)
                dist = math.sqrt(y**2 + x**2)
                    
                # if is you, store positions. don't store origin position (this has grad = 0 and dist = 0, which is not meaningful for checking beam collisions), check that dist is less than max_dist before storing. 
                if not is_train: 
                    if ((grad in yous_dict and yous_dict[grad] > dist) or grad not in yous_dict) and max_dist >= dist > 0: # if grad already exists, only store if current dist is smaller than recorded
                        yous_dict[grad] = dist
                
                # if is train, check position with stored. reject if for the same grad, a you exists with smaller dist, or if the dist to train exceeds max dist
                else: 
                    if (grad in yous_dict and yous_dict[grad] < dist) or dist > max_dist: 
                        continue
                    if grad not in allowed_list: 
                        allowed_list.append(grad)

    return len(allowed_list)

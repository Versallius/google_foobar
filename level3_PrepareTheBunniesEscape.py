# foobar.withgoogle.com
# Level 3

'''
Prepare the Bunnies' Escape
===========================
You're awfully close to destroying the LAMBCHOP doomsday device and freeing Commander Lambda's bunny workers, but once they're free of the work duties the bunnies are going to need to escape Lambda's space station via the escape pods as quickly as possible. Unfortunately, the halls of the space station are a maze of corridors and dead ends that will be a deathtrap for the escaping bunnies. Fortunately, Commander Lambda has put you in charge of a remodeling project that will give you the opportunity to make things a little easier for the bunnies. Unfortunately (again), you can't just remove all obstacles between the bunnies and the escape pods - at most you can remove one wall per escape pod path, both to maintain structural integrity of the station and to avoid arousing Commander Lambda's suspicions. 
You have maps of parts of the space station, each starting at a work area exit and ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, where 0s are passable space and 1s are impassable walls. The door out of the station is at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1). 
Write a function solution(map) that generates the length of the shortest path from the station door to the escape pod, where you are allowed to remove one wall as part of your remodeling plans. The path length is the total number of nodes you pass through, counting both the entrance and exit nodes. The starting and ending positions are always passable (0). The map will always be solvable, though you may or may not need to remove a wall. The height and width of the map can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal moves are allowed.
'''

# Use dynamic programming to update the maze from both front and back. 
# This way we can figure out where to best remove a wall. 

def backward(maze):
    nrows = len(maze)
    ncols = len(maze[0])
    output = []
    for i in range(nrows):
       output.append([float('inf')]*ncols) 
    output[-1][-1] = 1

    bfs_queue = [(nrows-1, ncols-1)]
    val = 1
    
    while len(bfs_queue) != 0:
        cell = bfs_queue[0]
        bfs_queue = bfs_queue[1:]

        my = output[cell[0]][cell[1]]
        if cell[0]-1 >= 0 and maze[cell[0]-1][cell[1]] == 0 and output[cell[0]-1][cell[1]] == float('inf'):
            output[cell[0]-1][cell[1]] = my + 1
            bfs_queue.append((cell[0]-1, cell[1]))
        if cell[1]-1 >= 0 and maze[cell[0]][cell[1]-1] == 0 and output[cell[0]][cell[1]-1] == float('inf'):
            output[cell[0]][cell[1]-1] = my + 1
            bfs_queue.append((cell[0], cell[1]-1))
        if cell[0]+1 < nrows and maze[cell[0]+1][cell[1]] == 0 and output[cell[0]+1][cell[1]] == float('inf'):
            output[cell[0]+1][cell[1]] = my + 1
            bfs_queue.append((cell[0]+1, cell[1]))
        if cell[1]+1 < ncols and maze[cell[0]][cell[1]+1] == 0 and output[cell[0]][cell[1]+1] == float('inf'):
            output[cell[0]][cell[1]+1] = my + 1
            bfs_queue.append((cell[0], cell[1]+1))


    return output

def forward(maze):
    nrows = len(maze)
    ncols = len(maze[0])
    output = []
    for i in range(nrows):
       output.append([float('inf')]*ncols) 
    output[0][0] = 0

    bfs_queue = [(0, 0)]
    val = 0
    
    while len(bfs_queue) != 0:
        cell = bfs_queue[0]
        bfs_queue = bfs_queue[1:]

        my = output[cell[0]][cell[1]]
        if cell[0]-1 >= 0 and maze[cell[0]-1][cell[1]] == 0 and output[cell[0]-1][cell[1]] == float('inf'):
            output[cell[0]-1][cell[1]] = my + 1
            bfs_queue.append((cell[0]-1, cell[1]))
        if cell[1]-1 >= 0 and maze[cell[0]][cell[1]-1] == 0 and output[cell[0]][cell[1]-1] == float('inf'):
            output[cell[0]][cell[1]-1] = my + 1
            bfs_queue.append((cell[0], cell[1]-1))
        if cell[0]+1 < nrows and maze[cell[0]+1][cell[1]] == 0 and output[cell[0]+1][cell[1]] == float('inf'):
            output[cell[0]+1][cell[1]] = my + 1
            bfs_queue.append((cell[0]+1, cell[1]))
        if cell[1]+1 < ncols and maze[cell[0]][cell[1]+1] == 0 and output[cell[0]][cell[1]+1] == float('inf'):
            output[cell[0]][cell[1]+1] = my + 1
            bfs_queue.append((cell[0], cell[1]+1))


    return output


def combine(fwd, bwd, maze):
    nrows = len(maze)
    ncols = len(maze[0])
    output = []
    for i in range(nrows):
       output.append([float('inf')]*ncols) 

    for i in range(nrows):
        for j in range(ncols):
            output[i][j] = fwd[i][j] + bwd[i][j]

    for i in range(nrows):
        for j in range(ncols):
            if maze[i][j] == 1:
                fs = []
                bs = []
                if i-1 >= 0:
                    fs.append(fwd[i-1][j])
                    bs.append(bwd[i-1][j])
                if j-1 >= 0:
                    fs.append(fwd[i][j-1])
                    bs.append(bwd[i][j-1])
                if i+1 < nrows:
                    fs.append(fwd[i+1][j])
                    bs.append(bwd[i+1][j])
                if j+1 < ncols:
                    fs.append(fwd[i][j+1])
                    bs.append(bwd[i][j+1])
                min_val = min(fs) + min(bs) + 2
                output[i][j] = min_val

    return output

def solution(map):
    bwd = backward(map)
    fwd = forward(map)
    output = combine(fwd, bwd, map)
    return min([min(i) for i in output])

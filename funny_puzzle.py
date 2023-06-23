import heapq

def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    for idx, e in enumerate(from_state):
        if e != 0:
            curr_x = idx // 3
            curr_y = idx % 3

            des_x = (e - 1) // 3
            des_y = (e - 1) % 3

            distance += abs(curr_x - des_x) + abs(curr_y - des_y)

    return distance


def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    succ_states = []
    moves = [[-1,0], [1,0], [0,-1], [0,1]]
    
    for move in moves:
        for idx, e in enumerate(state):
            if e == 0: continue
            curr_x = idx // 3
            curr_y = idx % 3

            new_x = curr_x + move[0]
            new_y = curr_y + move[1]

            x_in_range = new_x >= 0 and new_x < 3
            y_in_range = new_y >= 0 and new_y < 3            

            if x_in_range and y_in_range:
                is_zero = state[3 * new_x + new_y] == 0

                if is_zero:
                    #swap 0 with current element and add to succ_states list
                    list_to_add = state.copy()
                    list_to_add[idx] = 0
                    list_to_add[3 * new_x + new_y] = e

                    succ_states.append(list_to_add)


    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    #Initialize variables
    pq = []
    visited = {}
    max_queue_length = 0

    #Add state
    g = 0
    h = get_manhattan_distance(state)   
    heapq.heappush(pq,(g + h, state, (g, h, -1)))

    while(len(pq) > 0):
        max_queue_length = max(max_queue_length, len(pq))

        #Pop from top of PQ
        current_p, current_state, current_rest = heapq.heappop(pq) 
        current_key = int(''.join([str(n) for n in current_state]))
        
        #Add to visited with all necessary info
        if visited.get(current_key) == None:
            visited[current_key] = (current_p, current_state, current_rest) 
        elif visited.get(current_key)[2][0] > current_rest[0]:
            visited[current_key] = (current_p, current_state, current_rest)

        #Goal state reached, we simply print the path now
        if get_manhattan_distance(current_state) == 0:
            print_path(visited, max_queue_length, current_state, current_rest)
            break
        
        #Expand from current state
        succ_states = get_succ(current_state) #Get children of current_state
        for succ_state in succ_states:
            g = current_rest[0] + 1
            h = get_manhattan_distance(succ_state)
            parent_index = current_key #parent_index is simply the key of our current node/state

            succ_key = int(''.join([str(m) for m in succ_state]))            
            if visited.get(succ_key) == None:
                heapq.heappush(pq, (g + h, succ_state, (g, h, parent_index)))
            elif visited.get(succ_key)[2][0] > g:
                heapq.heappush(pq, (g + h, succ_state, (g, h, parent_index)))
        

def print_path(visited, max_queue_length, current_state, current_rest):
    path = [current_state]
    parent_index = current_rest[2]

    while parent_index != -1:
        p, add_state, rest = visited.get(parent_index)
        path.append(add_state)
        parent_index = rest[2]

    i = 0
    for p in path[::-1]:
        print(p, "h={}".format(get_manhattan_distance(p)), "moves: {}".format(i))
        i += 1
    
    print("Max queue length:", max_queue_length)

if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([2,5,1,4,0,6,7,0,3])
    print()

    solve([4,3,0,5,1,6,7,2,0])
    print()
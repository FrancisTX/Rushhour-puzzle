import copy
## ["--B---",
#   "--B---", 
#   "XXB---", 
#   "--AA--", 
#   "------", 
#   "------"]
class Car:
    def __init__(self, name, starting_position, length, end_position, direction):
        self.name = name
        self.starting_position = starting_position
        self.length = length 
        self.end_position = end_position
        self.direction = direction


def rushhour(search_mode, start_state):
    if search_mode == 0:
        total_moves, total_states = state_search(start_state)

    print('Total moves: ', total_moves)
    print('Total states explored: ', total_states)
   

##go through all vehicles in the grid
def cars(start_state):
    car_list = []
    for i in range(len(start_state)):
        for j in range(len(start_state[i])):
            if start_state[i][j] != "-":
                if j + 2 < 6 and start_state[i][j + 2] == start_state[i][j]:
                    if check_repeat_car(car_list, start_state[i][j]) == False:
                        car_list.append(Car(start_state[i][j], [i,j], 3, [i,j+2], "HORIZONTAL"))
                elif j + 1 < 6 and start_state[i][j + 1] == start_state[i][j]:
                    if check_repeat_car(car_list, start_state[i][j]) == False:
                        car_list.append(Car(start_state[i][j], [i,j], 2, [i,j+1], "HORIZONTAL"))
                elif i + 2 < 6 and start_state[i + 2][j] == start_state[i][j]:
                    if check_repeat_car(car_list, start_state[i][j]) == False:
                        car_list.append(Car(start_state[i][j], [i,j], 3, [i+2,j], "VERTICAL"))
                elif i + 1 < 6 and start_state[i + 1][j] == start_state[i][j]:
                    if check_repeat_car(car_list, start_state[i][j]) == False:
                        car_list.append(Car(start_state[i][j], [i,j], 2, [i+1,j], "VERTICAL"))
            else:
                continue
    return car_list

def check_repeat_car(car_list,car_name):
    for car in car_list:
        if car_name == car.name:
            return True
    return False

##Implementing the blocking heuristic
def state_search(start_state):
    total_moves = 0
    total_states_explored = 0
    cur_state = start_state
    path = []
    moving_set = set()
    explored_cur_state = set()
    while len(cur_state) > 0:
        explored_cur_state.add(tuple(cur_state))
        cur_state = list(cur_state)

        for element in cur_state:
            print(element)
        print("\n")

        if cur_state[2][4] == "X" and cur_state[2][5] == "X":
            path.append (cur_state)
            break

        path.append(cur_state)
        car_list = cars(cur_state)

        new_states = try_move_right(cur_state, car_list)
        #new_states.difference_update(explored_cur_state)
        moving_set = moving_set.union(new_states)

        new_states = try_move_left(cur_state, car_list)
        #new_states.difference_update(explored_cur_state)
        moving_set = moving_set.union(new_states)

        new_states = try_move_up(cur_state, car_list)
        #new_states.difference_update(explored_cur_state)
        moving_set = moving_set.union(new_states)

        new_states = try_move_down(cur_state, car_list)
        #new_states.difference_update(explored_cur_state)
        moving_set = moving_set.union(new_states)

        total_states_explored += len(moving_set)
        
        next_state = []
        if len(moving_set) == 0:
            print("FALL")
            break
        h_n = 7
        for state in moving_set:
            blocking = blocking_heuristic(state)
            if blocking < h_n and state not in explored_cur_state:
                h_n = blocking
                cur_state = state
        
        moving_set.clear()
        total_moves += 1

    return total_moves, total_states_explored
    
def try_move_right(cur_state, car_list):
    new_state_list = set()
    for car in car_list:
        if car.direction == "HORIZONTAL":
            #move right 
            if car.end_position[1] + 1 < 6 and cur_state[car.end_position[0]][car.end_position[1]+1] == "-":
                new_state = copy.deepcopy(cur_state)
                tem_list = list(new_state[car.starting_position[0]])
                tem_list[car.starting_position[1]] = "-"
                tem_list[car.end_position[1] + 1] = car.name
                new_state[car.starting_position[0]] = ''.join(tem_list)
                #car.starting_position[1] = car.starting_position[1] + 1
                #car.end_position[1] = car.end_position[1] + 1
                new_state_list.add(tuple(new_state))
    return new_state_list

def try_move_left(cur_state, car_list):
    new_state_list = set()
    for car in car_list:
        if car.direction == "HORIZONTAL":
            #move right 
            if car.starting_position[1] - 1 >= 0 and cur_state[car.starting_position[0]][car.starting_position[1] - 1] == "-":
                new_state = copy.deepcopy(cur_state)
                tem_list = list(new_state[car.starting_position[0]])
                tem_list[car.starting_position[1] - 1] = car.name
                tem_list[car.end_position[1]] = "-"
                new_state[car.starting_position[0]] = ''.join(tem_list)
                #car.starting_position[1] = car.starting_position[1] - 1
                #car.end_position[1] = car.end_position[1] - 1
                new_state_list.add(tuple(new_state))
    return new_state_list

def try_move_down(cur_state, car_list):
    new_state_list = set()
    for car in car_list:
        if car.direction == "VERTICAL":
            #move right 
            if car.end_position[0] + 1 < 6 and cur_state[car.end_position[0] + 1][car.end_position[1]] == "-":
                new_state = copy.deepcopy(cur_state)
                tem_list = list(new_state[car.starting_position[0]])
                tem_list[car.starting_position[1]] = "-"
                new_state[car.starting_position[0]] = ''.join(tem_list)
                tem_list = list(new_state[car.end_position[0] + 1])
                tem_list[car.end_position[1]] = car.name
                new_state[car.end_position[0] + 1] = ''.join(tem_list)
                #car.starting_position[0] = car.starting_position[0] + 1
                #car.end_position[0] = car.end_position[0] + 1
                new_state_list.add(tuple(new_state))
    return new_state_list

def try_move_up(cur_state, car_list):
    new_state_list = set()
    for car in car_list:
        if car.direction == "VERTICAL":
            #move right 
            if car.starting_position[0] - 1 >= 0 and cur_state[car.starting_position[0] - 1][car.starting_position[1]] == "-":
                new_state = copy.deepcopy(cur_state)
                tem_list = list(new_state[car.starting_position[0] - 1])
                tem_list[car.starting_position[1]] = car.name
                new_state[car.starting_position[0] - 1] = ''.join(tem_list)
                tem_list = list(new_state[car.end_position[0]])
                tem_list[car.end_position[1]] = "-"
                new_state[car.end_position[0]] = ''.join(tem_list)
                #car.starting_position[0] = car.starting_position[0] - 1
                #car.end_position[0] = car.end_position[0] - 1
                new_state_list.add(tuple(new_state))
    return new_state_list

def blocking_heuristic(cur_state):
    blocking_car = 1
    for i in range(len(cur_state[2])):
        if cur_state[2][i] != "-" and cur_state[2][i] !=  "X":
            blocking_car += 1
    return blocking_car




def reverse(lst):
    return lst[::-1]

rushhour(0,["--B---","--B---","XXB---","--AA--", "------","------"])
#rushhour(0, ["--OPPP","--O--A","XXO--A","-CC--Q","-----Q","--RRRQ"])
#rushhour(0, ["--OPPP","--O--A","XXO--A","---CCQ","-----Q","--RRRQ"])

#rushhour(0, ["------", "------", "XX----", "AAB---","--B---","--B---"])


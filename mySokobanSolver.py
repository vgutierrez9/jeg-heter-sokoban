
'''

The partially defined functions and classes of this module
will be called by a marker script.

You should complete the functions and classes according to their specified interfaces.


'''

import search
import itertools
from itertools import product
import sokoban
import math
import copy

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#DONE
def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [ (9890394, 'Vanessa', 'Gutierrez'), (9884050, 'Glenn', 'Christensen'), (9884076, 'Marius', 'Imingen') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#DONE
def taboo_cells(warehouse):
    '''
    Identify the taboo cells of a warehouse. A cell is called 'taboo'
    if whenever a box get pushed on such a cell then the puzzle becomes unsolvable.
    When determining the taboo cells, you must ignore all the existing boxes,
    simply consider the walls and the target  cells.
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of
             these cells is a target.

    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with
       an '#' and the taboo cells marked with an 'X'.
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.
    '''

    coordinate_list = taboo_coordinates(warehouse)

    X,Y = zip(*warehouse.walls)
    x_size, y_size = 1+max(X), 1+max(Y)

    vis = [[" "] * x_size for y in range(y_size)]
    for (x,y) in warehouse.walls:
        vis[y][x] = "#"
    for (x,y) in coordinate_list:
        vis[y][x] = "X"

    return "\n".join(["".join(line) for line in vis])

#DONE
def taboo_coordinates(warehouse):
    '''
    Identify the coordinates of the taboo cells of a warehouse. A cell is called 'taboo'
    if whenever a box get pushed on such a cell then the puzzle becomes unsolvable.
    When determining the taboo cells, you must ignore all the existing boxes,
    simply consider the walls and the target  cells.
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of
             these cells is a target.

    @param warehouse: a Warehouse object

    @return
       A list containing the coordinates for all the taboo cell
    '''
    # Get map dimensions
    X,Y = zip(*warehouse.walls)
    x_size, y_size = 1 + max(X), 1 + max(Y)

    # Get all map coordinates
    all_possible_coordinates = list(itertools.product(range(x_size), range(y_size)))

    # Get all floor (non-wall) tiles

    floor = [coordinate for coordinate in all_possible_coordinates if coordinate not in warehouse.walls]
    floor_next_to_wall = [coordinate for coordinate in all_possible_coordinates if is_next_to_wall(warehouse, coordinate)]

    # Get all corner tiles
    corners = [(x,y) for x,y in floor if is_corner(warehouse, (x,y))]

    # Add non-target corners to taboo cells
    taboo = [(x,y) for x,y in corners if (x,y) not in warehouse.targets]

    #Pair all corners with all other corners and put in list
    all_corner_pairs = itertools.permutations(corners, 2)
    
    #list of gaps in walls
    gap = []
        
    #Check for floor tiles between corners, without targets, and add to taboo list
    #Pull each set of corner pairs
    for corner_pair in all_corner_pairs:
        #Check if those corners are in same column
        if vertically_aligned(corner_pair[0], corner_pair[1]):
            #Find which are the min and max y values
            if corner_pair[0][1] < corner_pair[1][1]:
                taboo_y_min = corner_pair[0][1]
                taboo_y_max = corner_pair[1][1]
            else:
                taboo_y_min = corner_pair[1][1]
                taboo_y_max = corner_pair[0][1]

            target_between_corners = False
            #Check if any targets are between the corners
            for target in warehouse.targets:
                if vertically_aligned(corner_pair[0], target) and ((target[1] > taboo_y_min) or (target[1] < taboo_y_max)):
                    target_between_corners = True
                    break
                    
            #if no target between corners, check for gaps in walls 
            if not target_between_corners:
            
                corner_x = corner_pair[0][0]
                corner1 = corner_pair[0]
                corner2 = corner_pair[1]
                
                #Will be marked true if corner (1/2) has wall on that side (R/L)
                corner1L = False
                corner1R = False
                corner2L = False
                corner2R = False
                
                #check for walls on sides of corners
                if cell_in_direction(corner1, "Left") in warehouse.walls:
                    corner1L = True
                if cell_in_direction(corner1, "Right") in warehouse.walls:
                    corner1R = True
                if cell_in_direction(corner2, "Left") in warehouse.walls:
                    corner2L = True
                if cell_in_direction(corner2, "Right") in warehouse.walls:
                    corner2R = True    
                    
                if (corner1L and corner2L) or (corner1R and corner2R):
                    #if wall on L, check wall on L for a gap
                    if corner1L and corner2L:
                        gap = [(x,y) for x,y in floor if x == corner1[0]-1 and ((y > taboo_y_min) and (y < taboo_y_max))]
                    #if wall on R, check wall on R for a gap
                    if corner1R and corner2R:
                        gap = [(x,y) for x,y in floor if x == corner1[0]+1 and ((y > taboo_y_min) and (y < taboo_y_max))]
                    
                    #if no gap in wall(s)   
                    if gap == []:
                        #add each floor cell between corners to taboo
                        taboo += [(x,y) for x,y in floor if x == corner_x and ((y > taboo_y_min) and (y < taboo_y_max))]


        elif horizontally_aligned(corner_pair[0], corner_pair[1]):
            #Find which are the min and max x values
            if corner_pair[0][0] < corner_pair[1][0]:
                taboo_x_min = corner_pair[0][0]
                taboo_x_max = corner_pair[1][0]
            else:
                taboo_x_min = corner_pair[1][0]
                taboo_x_max = corner_pair[0][0]

                target_between_corners = False
                #Check if any targets are between the corners
                for target in warehouse.targets:
                    if horizontally_aligned(corner_pair[0], target) and ((target[0] > taboo_x_min) or (target[0] < taboo_x_max)):
                        target_between_corners = True
                        break
                if not target_between_corners:
                    corner_y = corner_pair[0][1]
                    
                    corner1 = corner_pair[0]
                    corner2 = corner_pair[1]
                    
                    #Will be marked true if corner (1/2) has wall on that side (Up/Down)
                    corner1U = False
                    corner1D = False
                    corner2U = False
                    corner2D = False
                    
                    #check for walls on sides of corners
                    if cell_in_direction(corner1, "Up") in warehouse.walls:
                        corner1U = True
                    if cell_in_direction(corner1, "Down") in warehouse.walls:
                        corner1D = True
                    if cell_in_direction(corner2, "Up") in warehouse.walls:
                        corner2U = True
                    if cell_in_direction(corner2, "Down") in warehouse.walls:
                        corner2D = True  
                        
                    if (corner1U and corner2U) or (corner1D and corner2D):
                        #if wall above, check wall above for a gap
                        if corner1U and corner2U:
                            gap = [(x,y) for x,y in floor if y == corner1[1]-1 and ((x > taboo_x_min) and (x < taboo_x_max))]
                        #if wall below, check wall below for a gap
                        if corner1D and corner2D:
                            gap = [(x,y) for x,y in floor if y == corner1[1]+1 and ((x > taboo_x_min) and (x < taboo_x_max))]
                        
                        #if no gap in wall(s)   
                        if gap == []:
                            #add each floor cell between corners to taboo
                            taboo += [(x,y) for x,y in floor if y == corner_y and ((x > taboo_x_min) and (x < taboo_x_max))]
    
    return taboo

#DONE
def is_corner(warehouse, floor_cell):
    x,y = floor_cell[0], floor_cell[1]
    #if in a lower right hand corner
    if (x + 1,y) in warehouse.walls and (x, y + 1) in warehouse.walls:
        return True
    if (x - 1,y) in warehouse.walls and (x, y + 1) in warehouse.walls:
        return True
    if (x - 1,y) in warehouse.walls and (x, y - 1) in warehouse.walls:
        return True
    if (x + 1,y) in warehouse.walls and (x, y - 1) in warehouse.walls:
        return True

    return False

#def get_dist_to_closest_cell(origin, cells):
    #min_distance = 0
    #if len(cells) > 0:
   #     min_distance = manhattan_distance(origin, cells[0])

        #for cell in cells:
# end of observable code on this method.

#def get_hungarian_assignment(boxes, targets):
    # # There must be an equal number of targets and boxes
    # assert(len(boxes) == len(targets))
    # value = 0
    # first = True
    # dist = 0
    # for box in boxes:
        # box_x, box_y = zip(*box)
        # for target in targets:
            # target_x, target_y = zip(*target)
            # dist = math.sqrt((box_x - target_x)**2 + (box_y - target_y)**2 )
            # if first:
                # min_dist = dist
                # first = False
            # elif dist < min_dist:
                # min_dist = dist
        # value += min_dist

    # return value

def manhattan_distance(cell_a, cell_b):
    return abs(cell_a[0] - cell_b[0]) + abs(cell_a[1] - cell_b[1])


#DONE
def is_next_to_wall(warehouse, cell):
    x,y = cell[0], cell[1]
    if ((x + 1, y) in warehouse.walls or (x - 1, y) in warehouse.walls or (x, y + 1) in warehouse.walls or (x, y - 1) in warehouse.walls):
        return True
    else:
        return False

#did we use?
# def next_to(cell_a, cell_b):
    # if(abs(cell_a[0] - cell_b[0])) == 1 or abs(cell_a[1] - cell_b[1]) == 1:
        # return True
    # return False


#DONE
def cell_in_direction(cell, direction):
    if direction == "Left":
        return(cell[0] - 1, cell[1])
    elif direction == "Right":
        return(cell[0] + 1, cell[1])
    elif direction == "Up":
        return(cell[0], cell[1] - 1)
    elif direction == "Down":
        return(cell[0], cell[1] + 1)

#DONE - don't need because search returns list of directions
def get_direction(origin, destination):
   if horizontally_aligned(destination, origin):
      if origin[0] - destination[0] == 1:
         return "Left"
      elif origin[0] - destination[0] == -1:
         return "Right"
      else:
         return "Destination cell is too far away to be reached in one left or right movement."
   elif vertically_aligned(destination, origin):
      if origin[1] - destination[1] == 1:
         return "Up"
      elif origin[1] - destination[1] == -1:
         return "Down"
      else:
         return "Destination cell is too far away to be reached in one up or down movement."
   else:
      return "Destination cell cannot be reached in one up, down, left or right movement from origin."


#DONE
def horizontally_aligned(cell_a, cell_b):
    if cell_a[1] == cell_b[1]:
        return True

#DONE
def vertically_aligned(cell_a, cell_b):
    if cell_a[0] == cell_b[0]:
        return True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the provided module 'search.py'.

        Use the sliding puzzle and the pancake puzzle for inspiration!

    '''
    #DONE
    def __init__(self, warehouse):

        self.wh = warehouse
        self.initial = ((warehouse.worker),) + tuple(warehouse.boxes) 
        self.targets = warehouse.targets
        self.taboo_list = taboo_coordinates(warehouse)
        
    #DONE
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state
        if these actions put the builder into an empty space and
        do not push a box in a taboo cell, a wall, or into another box.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']
        NO TABOO!!!!!!!!!!!!!!
        """
        #print("in actions")
        #print(self.wh.walls)
        OK_actions = []

        #get cells in each direction
        cell_to_right = cell_in_direction(state[0], "Right")
        cell_to_left = cell_in_direction(state[0], "Left")
        cell_up = cell_in_direction(state[0], "Up")
        cell_down = cell_in_direction(state[0], "Down")

        #if no wall or box on the right, add it to action list
        if cell_to_right not in self.wh.walls and cell_to_right not in state[1:]:
            OK_actions += ("Right",)
        #if box on right, check it out
        elif cell_to_right in state[1:]:
            #what's on box's right?
            box_right = cell_in_direction(cell_to_right, "Right")
            #if box's right is good, add right to action list
            if box_right not in self.taboo_list and box_right not in self.wh.walls and box_right not in state[1:]:
                OK_actions += ("Right",)

        #if no wall or box on the left, add it to action list
        if cell_to_left not in self.wh.walls and cell_to_left not in state[1:]:
            OK_actions += ("Left",)
        #if box on left, check it out
        elif cell_to_left in state[1:]:
            #what's on box's left?
            box_left = cell_in_direction(cell_to_left, "Left")
            #if box's left is good, add left to action list
            if box_left not in self.taboo_list and box_left not in self.wh.walls and box_left not in state[1:]:
                OK_actions += ("Left",)

        #exact same thing as above, but for up and down directions
        if cell_up not in self.wh.walls and cell_up not in state[1:]:
            OK_actions += ("Up",)
        elif cell_up in state[1:]:
            box_up = cell_in_direction(cell_up, "Up")
            if box_up not in self.taboo_list and box_up not in self.wh.walls and box_up not in state[1:]:
                OK_actions += ("Up",)

        if cell_down not in self.wh.walls and cell_down not in state[1:]:
            OK_actions += ("Down",)
        elif cell_down in state[1:]:
            box_down = cell_in_direction(cell_down, "Down")
            if box_down not in self.taboo_list and box_down not in self.wh.walls and box_down not in state[1:]:
                OK_actions += ("Down",)

        return OK_actions

    #DONE
    def taboo_allowed_actions(self, state):
        """
        Return the list of actions that can be executed in the given state
        if these actions put the builder in an empty space or
        do not push a box in a wall, or into another box.
        Does not care if box is pushed to taboo space!!!!!!!!!!
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']
        """

        OK_actions = ()

        #get cells in each direction
        cell_to_right = cell_in_direction(state[0], "Right")
        cell_to_left = cell_in_direction(state[0], "Left")
        cell_up = cell_in_direction(state[0], "Up")
        cell_down = cell_in_direction(state[0], "Down")

        #if no wall or box on the right, add it to action list
        if cell_to_right not in self.wh.walls and cell_to_right not in state:
            OK_actions += ("Right",)
        #if box on right, check it out
        elif cell_to_right in state:
            #what's on box's right?
            box_right = cell_in_direction(cell_to_right, "Right")
            #if box's right is good, add right to action list
            if box_right not in self.wh.walls and box_right not in state:
                OK_actions += ("Right",)

        #if no wall or box on the left, add it to action list
        if cell_to_left not in self.wh.walls and cell_to_left not in state:
            OK_actions += ("Left",)
        #if box on left, check it out
        elif cell_to_left in state:
            #what's on box's left?
            box_left = cell_in_direction(cell_to_left, "Left")
            #if box's left is good, add left to action list
            if box_left not in self.wh.walls and box_left not in state:
                OK_actions += ("Left",)

        #exact same thing as above, but for up and down directions
        if cell_up not in self.wh.walls and cell_up not in state:
            OK_actions += ("Up",)
        elif cell_up in state:
            box_up = cell_in_direction(cell_up, "Up")
            if box_up not in self.wh.walls and box_up not in state:
                OK_actions += ("Up",)

        if cell_down not in self.wh.walls and cell_down not in state:
            OK_actions += ("Down",)
        elif cell_down in state:
            box_down = cell_in_direction(cell_down, "Down")
            if box_down not in self.wh.walls and box_down not in state:
                OK_actions += ("Down",)

        return OK_actions

    #DONE ?
    def result(self, state, action):
        """Return the state that results from executing the given action in the given state. The action must be one of self.actions(state)."""
        assert action in self.actions(state)
        
        new_state = ()
        new_state = copy.deepcopy(state)
        
        #is the cell builder moving to a box?
        if cell_in_direction(state[0], action) in state[1:]:
            i = 1
            #find which box
            for box in state[1:]:
                #if we find the box that builder is moving to
                if cell_in_direction(state[0], action) == box:
                    new_state_list = list(new_state)
                    #move the box one space in the direction
                    new_state_list[i] = cell_in_direction(box, action)
                    
                    new_state = tuple(new_state_list)
                    break
                i+=1

            new_state_list = list(new_state)
            #move the builder to the cell in that direction (where the box was)
            new_state_list[0] = cell_in_direction(state[0], action)
            new_state = tuple(new_state_list)

        else:
            new_state_list = list(new_state)
            #move the builder to the cell in that direction
            new_state_list[0] = cell_in_direction(state[0], action)
            new_state = tuple(new_state_list)

        new_state = (new_state[0],) + tuple(sorted(new_state[1:]))

        # print(new_state)
        
        
        return new_state

   #DONE
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""

        num_box_on_target = 0
        for box in state[1:]:
            if box in self.targets:
                num_box_on_target += 1
        
        # print("Num box on target")
        # print(num_box_on_target)
        
        if num_box_on_target == len(state)-1:
            print("GOAL")
            return True
        else:
           return False

    def h(self, node):
    
        return self.value(node.state)
        
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        #Boxes as path cost
        for i in range(1, len(state1)-1):
            if state1[i][0] != state2[i][0] or state1[i][1] != state2[i][1]:
                return c + 1
        return c

        #Worker as path cost
        # return c + manhattan_distance(state1[0], state2[0])

    #DONE ?
    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value. Returns
        the value of the state passed to it as a sum of all the
        diagonal distances of each box to its closest target."""

        # There must be an equal number of targets and boxes
        assert(len(state)-1 == len(self.targets))

        value = 0
        first = True
        dist = 0
        boxes = []
        boxes = copy.deepcopy(state[1:])
        target_list = []
        target_list = copy.deepcopy(self.wh.targets)
        min_dist = 0
        
        box_targets_dist = []
        temp_list = []
        
        for box in boxes:
            #separate the box's x, y coordinates
            box_x = box[0]
            box_y = box[1]
            for target in target_list:
                #separate the target's x,y coordinates
                target_x = target[0]
                target_y = target[1]
                
                #find the diagonal distance (via hypotenus)
                dist = math.sqrt((box_x - target_x)**2 + (box_y - target_y)**2)
                #dist = manhattan_distance(box, target)
                
                temp_list += box
                temp_list += target
                temp_list += [dist,]
                #print("Temp list:")
                #print(temp_list)
                box_targets_dist += [temp_list,]
                temp_list = []
                #print("box_targets_dist")
                #print(box_targets_dist)
                
        while box_targets_dist:
            temp_trio = box_targets_dist[0]
            
            for i in range(0, len(box_targets_dist)):
                if i == 0:
                    min_dist = box_targets_dist[0][4]
                if box_targets_dist[i][4] < min_dist:
                    min_dist = box_targets_dist[i][4]
                    temp_trio = box_targets_dist[i] 
                    
            value += min_dist
            #print("min trio")
            #print(temp_trio)
            
            i = 0
            while i < len(box_targets_dist):
                trio = box_targets_dist[i]
                if (trio[0] == temp_trio[0] and trio[1] == temp_trio[1]) or (trio[2] == temp_trio[2] and trio[3] == temp_trio[3]):
                    box_targets_dist.remove(trio)
                    i -= 1
                i += 1
            
            #print("box tag dist minus")
            #print(box_targets_dist)
            
            min_buildr_dist = math.sqrt((boxes[0][0] - state[0][0])**2 + (boxes[0][1] - state[0][1])**2)
            for box in boxes:
                #separate the box's x, y coordinates
                box_x = box[0]
                box_y = box[1]
                
                temp_dist = math.sqrt((box_x - state[0][0])**2 + (box_y - state[0][1])**2)
                if temp_dist < min_buildr_dist:
                    min_buildr_dist = temp_dist
            
            value += min_buildr_dist
            
        return value
        
        # #get each box, one at a time
        # for box in boxes:
            # #separate the box's x, y coordinates
            # box_x = box[0]
            # box_y = box[1]
            # #get each target one at a time and find the distance to the target that is closest to the box
            # for target in target_list:
                # #separate the target's x,y coordinates
                # target_x = target[0]
                # target_y = target[1]
                # #find the diagonal distance (via hypotenus)
                # dist = math.sqrt((box_x - target_x)**2 + (box_y - target_y)**2)
                # #if first target, save that distance as minimum distance
                # if first:
                    # min_dist = dist
                    # first = False
                # #Save distance as minimum distance if it is less than the existing minimum distance
                # elif dist < min_dist:
                    # min_dist = dist
                    # target_list.remove(target)
            # #add the minimum distance for each box to value
            # value += min_dist

        # return value

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#DONE
def check_taboo_allowed_action_seq(warehouse, action_seq):
    '''
    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
      
        ***AN ACTION IS LEGAL EVEN IF IT PUSHES A BOX INTO A TABOO CELL***
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''

    skp = SokobanPuzzle(warehouse)
    temp_state = skp.initial
    for direction in action_seq:
        if direction in skp.legal_actions(temp_state):
            temp_state = skp.result(temp_state, direction)
        else:
            return "Failure"

    skp.wh.worker = temp_state[0]
    skp.wh.boxes = temp_state[1:]

    return skp.wh.__str__()

#DONE
def check_action_seq(warehouse, action_seq):
    '''
    Check if action sequence is norwegian legal if calling action accounting for taboo cells
    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    ***AN ACTION IS NOT LEGAL IF IT PUSHES A BOX INTO A TABOO CELL***
    
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall, OR PUSH A BOX INTO A TABOO SPOT.
        Otherwise, if all actions were successful, return
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    skp = SokobanPuzzle(warehouse)
    temp_state = skp.initial
    for direction in action_seq:
        if direction in skp.actions(temp_state):
            temp_state = skp.result(temp_state, direction)
        else:
            return "Failure"

    skp.wh.worker = temp_state[0]
    skp.wh.boxes = temp_state[1:]

    return skp.wh.__str__()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''
    This function should solve using elementary actions
    the puzzle defined in a file.

    @param warehouse: a valid Warehouse object

    @return
        A list of strings.
        If puzzle cannot be solved return ['Impossible']
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
           
    '''
    skp = SokobanPuzzle(warehouse)
    #SEARCH
    path = search.astar_graph_search(skp)
    
    if not path:
        return []
    #turn list of coordinates into list of strings
    else:
        print("Solution")
        # print(path.solution())
        print(len(path.solution()))
        return path.solution()
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#DONE!!!!!
def can_go_there(warehouse, dst):
    '''
    Determine whether the worker can walk to the cell dst=(row,col)
    without pushing any box.

    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,col) without pushing any box
      False otherwise
    '''

    X,Y = zip(*warehouse.walls)
    #get the maximum values of the x,y coordinates that are in the warehouse
    x_size, y_size = 1 + max(X), 1 + max(Y)
    
    #is worker already in goal coordinate - return true
    if warehouse.worker == dst:
        return True
    else:
        explored = []
        #add starting position expanded directions to frontier
        frontier = [warehouse.worker,]
        
        for cell in frontier:
            #check if cell being explored is valid (not a wall, box, explored or out of bounds)
            if cell not in warehouse.walls and cell not in warehouse.boxes and cell not in explored and cell[0] > 0 and cell[0] < x_size and cell[1] > 0 and cell[1] < y_size:
                
                #check if the cell is the goal coordinate, if so stop searching and return true
                if tuple(cell) == dst:                 
                    return True
                
                #expand cell in each direction and add the valid results cells to frontier
                cell_temp = cell_in_direction(cell, "Up")
                if cell_temp not in warehouse.walls and cell_temp not in warehouse.boxes and cell_temp not in explored and cell_temp[0] > 0 and cell_temp[0] < x_size and cell_temp[1] > 0 and cell_temp[1] < y_size:
                    frontier +=  [list(cell_in_direction(cell, "Up")),] 

                cell_temp = cell_in_direction(cell, "Down")
                if cell_temp not in warehouse.walls and cell_temp not in warehouse.boxes and cell_temp not in explored and cell_temp[0] > 0 and cell_temp[0] < x_size and cell_temp[1] > 0 and cell_temp[1] < y_size:
                    frontier += [list(cell_in_direction(cell, "Down")),] 
 
                cell_temp = cell_in_direction(cell, "Left")
                if cell_temp not in warehouse.walls and cell_temp not in warehouse.boxes and cell_temp not in explored and cell_temp[0] > 0 and cell_temp[0] < x_size and cell_temp[1] > 0 and cell_temp[1] < y_size:
                    frontier += [list(cell_in_direction(cell, "Left")),]                      
                    
                cell_temp = cell_in_direction(cell, "Right")
                if cell_temp not in warehouse.walls and cell_temp not in warehouse.boxes and cell_temp not in explored and cell_temp[0] > 0 and cell_temp[0] < x_size and cell_temp[1] > 0 and cell_temp[1] < y_size:
                    frontier += [list(cell_in_direction(cell, "Right")),] 
            
            
            #add cell to explored
            explored += [cell,]
            
        #all possible paths from the worker cell have been explored without reaching the destination, so return false
        return False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ]
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.

    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return ['Impossible']
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    skp = SokobanPuzzle(warehouse)
    
    if skp.goal_test(skp.initial):
        return []
        
    string_directions = solve_sokoban_elem(warehouse)
    print(string_directions)
    if not string_directions:
        return ['Impossible']
    
    macro_directions = []
    temp_state = skp.initial
    
    #go through each elementary action and look for actions that move boxes, add those actions to macro list
    for direction in string_directions:
        print(direction)
        #check if the move from the elem string is going to move a builder to a box
        if cell_in_direction(temp_state[0], direction) in temp_state[1:]:
            macro_move = tuple(list((cell_in_direction(temp_state[0], direction),) + (direction,)))
            macro_directions += [macro_move,]
        temp_state = skp.result(temp_state, direction)
    print("Macro")
    print(macro_directions)
    return macro_directions

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
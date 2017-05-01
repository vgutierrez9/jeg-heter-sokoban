
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

def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [ (9890394, 'Vanessa', 'Gutierrez'), (9884050, 'Glenn', 'Christensen'), (9884076, 'Marius', 'Imingen') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def taboo_cells(warehouse):
    '''
    Uses the taboo_coordinates method to make a string representation
    of the list of taboo cells taboo_coordinates return. 

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

    # Pair all corners with all other corners and put in list
    all_corner_pairs = itertools.permutations(corners, 2)

    # List of gaps in walls
    gap = []

    # Check for floor tiles between corners, without targets, and add to taboo list
    # Pull each set of corner pairs
    for corner_pair in all_corner_pairs:
        # Check if those corners are in same column
        if vertically_aligned(corner_pair[0], corner_pair[1]):
            # Find which are the min and max y values
            if corner_pair[0][1] < corner_pair[1][1]:
                taboo_y_min = corner_pair[0][1]
                taboo_y_max = corner_pair[1][1]
            else:
                taboo_y_min = corner_pair[1][1]
                taboo_y_max = corner_pair[0][1]

            target_between_corners = False
            # Check if any targets are between the corners
            for target in warehouse.targets:
                if vertically_aligned(corner_pair[0], target) and ((target[1] > taboo_y_min) or (target[1] < taboo_y_max)):
                    target_between_corners = True
                    break

            # If no target between corners, check for gaps in walls
            if not target_between_corners:

                corner_x = corner_pair[0][0]
                corner1 = corner_pair[0]
                corner2 = corner_pair[1]

                # Will be marked true if corner (1/2) has wall on that side (Right/Left)
                corner1L = False
                corner1R = False
                corner2L = False
                corner2R = False

                # Check for walls on sides of corners
                if cell_in_direction(corner1, "Left") in warehouse.walls:
                    corner1L = True
                if cell_in_direction(corner1, "Right") in warehouse.walls:
                    corner1R = True
                if cell_in_direction(corner2, "Left") in warehouse.walls:
                    corner2L = True
                if cell_in_direction(corner2, "Right") in warehouse.walls:
                    corner2R = True

                if (corner1L and corner2L) or (corner1R and corner2R):
                    # If wall on L, check wall on L for a gap
                    if corner1L and corner2L:
                        gap = [(x,y) for x,y in floor if x == corner1[0]-1 and ((y > taboo_y_min) and (y < taboo_y_max))]
                    # If wall on R, check wall on R for a gap
                    if corner1R and corner2R:
                        gap = [(x,y) for x,y in floor if x == corner1[0]+1 and ((y > taboo_y_min) and (y < taboo_y_max))]

                    # If no gap in wall(s)
                    if gap == []:
                        # Add each floor cell between corners to taboo
                        taboo += [(x,y) for x,y in floor if x == corner_x and ((y > taboo_y_min) and (y < taboo_y_max))]


        elif horizontally_aligned(corner_pair[0], corner_pair[1]):
            # Find which are the min and max x values
            if corner_pair[0][0] < corner_pair[1][0]:
                taboo_x_min = corner_pair[0][0]
                taboo_x_max = corner_pair[1][0]
            else:
                taboo_x_min = corner_pair[1][0]
                taboo_x_max = corner_pair[0][0]

                target_between_corners = False
                # Check if any targets are between the corners
                for target in warehouse.targets:
                    if horizontally_aligned(corner_pair[0], target) and ((target[0] > taboo_x_min) or (target[0] < taboo_x_max)):
                        target_between_corners = True
                        break
                if not target_between_corners:
                    corner_y = corner_pair[0][1]

                    corner1 = corner_pair[0]
                    corner2 = corner_pair[1]

                    # Will be marked true if corner (1/2) has wall on that side (Up/Down)
                    corner1U = False
                    corner1D = False
                    corner2U = False
                    corner2D = False

                    # Check for walls on sides of corners
                    if cell_in_direction(corner1, "Up") in warehouse.walls:
                        corner1U = True
                    if cell_in_direction(corner1, "Down") in warehouse.walls:
                        corner1D = True
                    if cell_in_direction(corner2, "Up") in warehouse.walls:
                        corner2U = True
                    if cell_in_direction(corner2, "Down") in warehouse.walls:
                        corner2D = True

                    if (corner1U and corner2U) or (corner1D and corner2D):
                        # If wall above, check wall above for a gap
                        if corner1U and corner2U:
                            gap = [(x,y) for x,y in floor if y == corner1[1]-1 and ((x > taboo_x_min) and (x < taboo_x_max))]
                        # If wall below, check wall below for a gap
                        if corner1D and corner2D:
                            gap = [(x,y) for x,y in floor if y == corner1[1]+1 and ((x > taboo_x_min) and (x < taboo_x_max))]

                        # If no gap in wall(s)
                        if gap == []:
                            # Add each floor cell between corners to taboo
                            taboo += [(x,y) for x,y in floor if y == corner_y and ((x > taboo_x_min) and (x < taboo_x_max))]

    return taboo

def is_corner(warehouse, floor_cell):
    '''
    Checks the floor cell in the given warehouse if its a corner or not

    @param warehouse: a Warehouse object
    @param floor_cell: a floor cell

    @return
        True, if the floor cell has a wall diagonaly under and over the floor cell's position
        Otherwise, If the floor cell has no walls diagonaly under and over
            return False
    '''

    x,y = floor_cell[0], floor_cell[1]

    # If floor cell is in a lower right hand corner
    if (x + 1,y) in warehouse.walls and (x, y + 1) in warehouse.walls:
        return True
    # If floor cell is in a lower left hand corner
    if (x - 1,y) in warehouse.walls and (x, y + 1) in warehouse.walls:
        return True
    # If floor cell is in a upper left hand corner
    if (x - 1,y) in warehouse.walls and (x, y - 1) in warehouse.walls:
        return True
    # If floor cell is in a upper right hand corner
    if (x + 1,y) in warehouse.walls and (x, y - 1) in warehouse.walls:
        return True

    return False

def manhattan_distance(cell_a, cell_b):
    '''
    Finds the manhattan distance between two given cells

    @param cell_a: a cell
    @param cell_b: a cell

    @return
        The manhattan distance between the two given cells
    '''
    return abs(cell_a[0] - cell_b[0]) + abs(cell_a[1] - cell_b[1])

def is_next_to_wall(warehouse, cell):
    '''
    Checks if the cell is next to a wall

    @param warehouse: a Warehouse object
    @param cell: a cell

    @return
        True, if the given cell is next to a wall.
        Otherwise, if no wall is found next to the cell
            return False


    '''
    x,y = cell[0], cell[1]
    # Checks if the cell has a wall above, under, or a wall on one of it sides
    if ((x + 1, y) in warehouse.walls or (x - 1, y) in warehouse.walls or (x, y + 1) in warehouse.walls or (x, y - 1) in warehouse.walls):
        return True
    else:
        return False

def cell_in_direction(cell, direction):
    '''
    Determine which cell is in the given direction

    @param cell: a cell

    @param direction: a string of containing a direction
        For example: "Right"

    @return
        The coordinate for the given direction.

    '''
    if direction == "Left":
        return(cell[0] - 1, cell[1])
    elif direction == "Right":
        return(cell[0] + 1, cell[1])
    elif direction == "Up":
        return(cell[0], cell[1] - 1)
    elif direction == "Down":
        return(cell[0], cell[1] + 1)


def horizontally_aligned(cell_a, cell_b):
    '''
    Checks if the two given cells are horizontally aligned

    @param cell_a: a cell

    @param cell_b: a cell

    @return
        True, if the cells are horizontally aligned
        Otherwise, if the cells are not horizontally aligned,
            return False
    '''

    # If the y axis of cell_a and y axis of cell_b are the same
    if cell_a[1] == cell_b[1]:
        return True

def vertically_aligned(cell_a, cell_b):
    '''
    Checks if the two given cells are vertically aligned

    @param cell_a: a cell

    @param cell_b: a cell

    @return
        True, if the cells are vertically aligned
        Otherwise, if the cells are not vertically aligned,
            return False
    '''
    # If the x axis of cell_a and x axis of cell_b are the same
    if cell_a[0] == cell_b[0]:
        return True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the provided module 'search.py'.

        Use the sliding puzzle and the pancake puzzle for inspiration!

    @param search.Problem: Problem class object

    '''
    def __init__(self, warehouse):
        '''
        Constructor specifying the puzzle's initial state, targets, warehouse
        and list over taboo coordinates.

        @param self: instance of a attribute

        @param warehouse: a warehouse
        '''

        self.wh = warehouse
        self.initial = ((warehouse.worker),) + tuple(warehouse.boxes)
        self.targets = warehouse.targets
        self.taboo_list = taboo_coordinates(warehouse)

    def actions(self, state):
        '''
        Return the list of actions that can be executed in the given state
        if these actions put the worker into an empty space and
        do not push a box in a taboo cell, a wall, or into another box.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']

        @param self: instance of a attribute

        @param state: the puzzle's current state

        @return
            List of actions
        '''
        OK_actions = []

        # Get cells in each direction
        cell_to_right = cell_in_direction(state[0], "Right")
        cell_to_left = cell_in_direction(state[0], "Left")
        cell_up = cell_in_direction(state[0], "Up")
        cell_down = cell_in_direction(state[0], "Down")

        # If there is no wall or box on the right, add it to action list
        if cell_to_right not in self.wh.walls and cell_to_right not in state[1:]:
            OK_actions += ("Right",)
        # If there is a box on the right, explore it, and check whats next to its right
        elif cell_to_right in state[1:]:
            box_right = cell_in_direction(cell_to_right, "Right")

            # If the cell right for the box is not a taboo cell, a wall, or another box. Add it to action list
            if box_right not in self.taboo_list and box_right not in self.wh.walls and box_right not in state[1:]:
                OK_actions += ("Right",)

        # If there is no wall or box on the left, add it to action list
        if cell_to_left not in self.wh.walls and cell_to_left not in state[1:]:
            OK_actions += ("Left",)
        # If there is a box on the left, explore it, and check whats next to its left
        elif cell_to_left in state[1:]:
            box_left = cell_in_direction(cell_to_left, "Left")
            # If the cell left for the box is not a taboo cell, a wall, or another box. Add it to action list
            if box_left not in self.taboo_list and box_left not in self.wh.walls and box_left not in state[1:]:
                OK_actions += ("Left",)

        # Exact same thing as above, but for up and down directions
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

    def taboo_allowed_actions(self, state):
        '''
        Return the list of actions that can be executed in the given state
        if these actions put the worker in an empty space or
        do not push a box in a wall, or into another box.
        Does not care if box is pushed to a taboo space.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']

        @param self: instance of a attribute

        @param state: the puzzle's current state

        @return
            List of actions

        '''


        OK_actions = ()

        # Get cells in each direction
        cell_to_right = cell_in_direction(state[0], "Right")
        cell_to_left = cell_in_direction(state[0], "Left")
        cell_up = cell_in_direction(state[0], "Up")
        cell_down = cell_in_direction(state[0], "Down")

        # If there is no wall or box on the right, add it to action list
        if cell_to_right not in self.wh.walls and cell_to_right not in state:
            OK_actions += ("Right",)
        # If there is a box on the right, explore it, and check whats next to its right
        elif cell_to_right in state:
            box_right = cell_in_direction(cell_to_right, "Right")
            # If the cell right for the box is not a taboo cell, a wall, or another box. Add it to action list
            if box_right not in self.wh.walls and box_right not in state:
                OK_actions += ("Right",)

        # If there is no wall or box on the left, add it to action list
        if cell_to_left not in self.wh.walls and cell_to_left not in state:
            OK_actions += ("Left",)
        # If there is a box on the left, explore it, and check whats next to its left
        elif cell_to_left in state:
            box_left = cell_in_direction(cell_to_left, "Left")
            # If the cell left for the box is not a taboo cell, a wall, or another box. Add it to action list
            if box_left not in self.wh.walls and box_left not in state:
                OK_actions += ("Left",)

        # Exact same thing as above, but for up and down directions
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

    def result(self, state, action):
        '''
        Return the state that results from executing the given action in the given state.
        The action must be one of self.actions(state).

        @param self: instance of a attribute

        @param state:

        @param action: a action

        @return
            Returns a new state of the puzzle.

        '''

        #Assert that the action is legal
        assert action in self.actions(state)

        new_state = ()
        new_state = copy.deepcopy(state)

        # Checks if the worker is pushing a box
        if cell_in_direction(state[0], action) in state[1:]:
            i = 1
            # Finds which box the worker pushes
            for box in state[1:]:
                # If current box is getting pushed, get the direction and update its new position
                if cell_in_direction(state[0], action) == box:
                    new_state_list = list(new_state)
                    new_state_list[i] = cell_in_direction(box, action)
                    new_state = tuple(new_state_list)
                    break
                i+=1

            new_state_list = list(new_state)
            # When the box's position is updated, move the worker where the box was.
            new_state_list[0] = cell_in_direction(state[0], action)
            new_state = tuple(new_state_list)

        # If the worker does not push a box, update the worker's position
        else:
            new_state_list = list(new_state)
            # Move the worker to the cell in that direction
            new_state_list[0] = cell_in_direction(state[0], action)
            new_state = tuple(new_state_list)

        # Place the worker at the first position of the tuple, and add the boxes
        new_state = (new_state[0],) + tuple(sorted(new_state[1:]))

        return new_state

    def goal_test(self, state):
        '''
        Determine if the state is a goal state.
        The requirement for a state to be a goal state,
        is if all targets has a box in them.

        @param self: instance of a attribute

        @param state: the puzzle's current state

        @return
            True, if the state is a goal.
            Otherwise, if the state is not a goal,
                return False
        '''
        # Counts amount of boxes on target
        num_box_on_target = 0
        for box in state[1:]:
            if box in self.targets:
                num_box_on_target += 1


        # Goal is reached if amount of boxes on target is the same as amount of boxes
        if num_box_on_target == len(state)-1:
            return True
        else:
           return False

    def h(self, node):
        '''
        The heuristic estimate to the goal

        @param self: instance of a attribute

        @param node: node in a search tree

        @return
            The value of the current node
        '''
        return self.value(node.state)


    def path_cost(self, c, state1, action, state2):
        '''
        Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path.

        @param self: instance of a attribute

        @param c: the cost for the path

        @param state1: the puzzle's current state

        @param action: action(s) performed

        @param state2: the puzzle's current state

        @return
            The path cost for the worker getting from state1 too state2
        '''

        '''
        This is the path cost we initally used. It makes the path cost
        the movement of the boxes
        '''
        # Counting the path of each time the box is pushed. Used for gathering data displayed on the graphs in the report
        #Boxes as path cost
        # for i in range(1, len(state1)-1):
        #     if state1[i][0] != state2[i][0] or state1[i][1] != state2[i][1]:
        #         return c + 1
        # return c

        # The path cost for the the movements of the worker getting from state1 too state 2
        return c + manhattan_distance(state1[0], state2[0])

    def value(self, state):
        '''
        Calculates the given state's value by finding the distances between
        the boxes and targets that are closest to each other.

        @param self: instance of a attribute

        @param state: the puzzle's current state

        @return
            The sum of distances between boxes and targets.
            Can return False if there is not equal number of targets and boxes
                in the given state.

        '''

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

        # Gets all the boxes coordinates, and targets coordinates,
        # and finds the boxes distance from all of the targets for the current puzzle
        for box in boxes:
            # Separate the box's x, y coordinates
            box_x = box[0]
            box_y = box[1]

            for target in target_list:
                # Separate the target's x,y coordinates
                target_x = target[0]
                target_y = target[1]

                # Find the diagonal distance (via hypotenus)
                dist = math.sqrt((box_x - target_x)**2 + (box_y - target_y)**2)

                temp_list += box
                temp_list += target
                temp_list += [dist,]
                box_targets_dist += [temp_list,]
                temp_list = []

        # Goes through the different distances and finds the shortest distance for each box
        while box_targets_dist:
            temp_trio = box_targets_dist[0]

            for i in range(0, len(box_targets_dist)):
                if i == 0:
                    min_dist = box_targets_dist[0][4]
                if box_targets_dist[i][4] < min_dist:
                    min_dist = box_targets_dist[i][4]
                    temp_trio = box_targets_dist[i]

            # Add the minimal distance to value
            value += min_dist

            # Loops until the shortest distance for each box is found.
            # If boxA has shortest distance to targetB. Remove targetB from the list and BoxA
            i = 0
            while i < len(box_targets_dist):
                trio = box_targets_dist[i]
                if (trio[0] == temp_trio[0] and trio[1] == temp_trio[1]) or (trio[2] == temp_trio[2] and trio[3] == temp_trio[3]):
                    box_targets_dist.remove(trio)
                    i -= 1
                i += 1

            
            '''
            This part was implemented to make a better value for our heuristic
            but after testing it, it was determined that the search is faster 
            without it
            '''
            # Finds the box closest to the worker, when found add that distance to value
            # min_worker_dist = math.sqrt((boxes[0][0] - state[0][0])**2 + (boxes[0][1] - state[0][1])**2)
            # for box in boxes:
            #     # Separate the box's x, y coordinates
            #     box_x = box[0]
            #     box_y = box[1]

            #     temp_dist = math.sqrt((box_x - state[0][0])**2 + (box_y - state[0][1])**2)
            #     if temp_dist < min_worker_dist:
            #         min_worker_dist = temp_dist

            # value += min_worker_dist

        return value

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_taboo_allowed_action_seq(warehouse, action_seq):
    '''
    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    An action is legal even if it pushes a box into a taboo cell

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
    # Checks each direction in the action sequence. If the direction is legal
    # update the worker and boxes in the puzzle object.
    for direction in action_seq:
        if direction in skp.legal_actions(temp_state):
            temp_state = skp.result(temp_state, direction)
        else:
            return "Failure"
    
    #Updates the worker and boxes position 
    skp.wh.worker = temp_state[0]
    skp.wh.boxes = temp_state[1:]

    return skp.wh.__str__()

def check_action_seq(warehouse, action_seq):
    '''
    Check if action sequence is norwegian legal if calling action accounting for taboo cells
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    An action is not legal if it pushes a box into a taboo cell.

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
    # Checks each direction in the action sequence. If the direction is legal
    # update the worker and boxes in the puzzle object.
    for direction in action_seq:
        if direction in skp.actions(temp_state):
            temp_state = skp.result(temp_state, direction)
        else:
            return "Failure"

    #Updates the worker and box position 
    skp.wh.worker = temp_state[0]
    skp.wh.boxes = temp_state[1:]

    return skp.wh.__str__()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''
    Solves the puzzle using elementary actions, by using the A* graph search.

    #This function should solve using elementary actions
    #the puzzle defined in a file.

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
    path = search.astar_graph_search(skp)

    if not path:
        return ['Impossible']
    # Turn list of coordinates into list of strings
    else:
        return path.solution()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
    # Get the maximum values of the x,y coordinates that are in the warehouse
    x_size, y_size = 1 + max(X), 1 + max(Y)

    # If the worker is already in a goal coordinate - return True, else start exploring floors.
    if warehouse.worker == dst:
        return True
    else:
        explored = []
        # Add starting position to expanded directions to frontier
        frontier = [warehouse.worker,]

        for cell in frontier:
            # Check if cell being explored is valid (not a wall, box, explored or out of bounds)
            if cell not in warehouse.walls and cell not in warehouse.boxes and cell not in explored and cell[0] > 0 and cell[0] < x_size and cell[1] > 0 and cell[1] < y_size:

                # Check if the cell is the goal coordinate, if so stop searching and return True
                if tuple(cell) == dst:
                    return True

                # Expand cell in each direction(Up, Down, Left and Right) and add the valid results cells to frontier
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


            # Add cell to explored
            explored += [cell,]

        # All possible paths from the worker cell have been explored without reaching the destination, so return False
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

    # Check if puzzle already is in a goal state
    if skp.goal_test(skp.initial):
        return []
    
    #Saves the list of strings of elementary actions solve_sokoban_elem returns
    string_directions = solve_sokoban_elem(warehouse)

    # Check if puzzle connot be solved
    if not string_directions:
        return ['Impossible']

    macro_directions = []
    temp_state = skp.initial

    # Go through each elementary action and look for actions that move boxes, add those actions to macro list
    for direction in string_directions:
        # Check if the move from the elementary string is going to move a worker to a box
        if cell_in_direction(temp_state[0], direction) in temp_state[1:]:
            macro_move = tuple(list((cell_in_direction(temp_state[0], direction),) + (direction,)))
            macro_directions += [macro_move,]
        temp_state = skp.result(temp_state, direction)

    return macro_directions

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

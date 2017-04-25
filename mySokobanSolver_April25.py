
'''

The partially defined functions and classes of this module 
will be called by a marker script. 

You should complete the functions and classes according to their specified interfaces.
 

'''

import search

import sokoban



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#DONE
def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (9890394, 'Vanessa', 'Gutierrez'), (9884050, 'Glenn', 'Christensen'), (9884076, 'Marius', 'Imingen') ]
    raise NotImplementedError()

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
    # Get map dimensions
    X,Y = zip(*warehouse.walls)
    x_size, y_size = 1 + max(X), 1 + max(Y)
    
    # Get all map coordinates
    all_possible_coordinates = list(itertools.product(range(x_size), range(y_size)))
    
    # Get all floor (non-wall) tiles
    floor = [floor_coordinate for coordinate in all_possible_coordinates if coordinate is not in warehouse.walls]
    floor_next_to_wall = [floor_coordinate for coordinate in all_possible_coordinates if is_next_to_wall(warehouse, coordinate)]
    
    # Get all corner tiles
    corners = [(x,y) for x,y in floor if is_corner(warehouse, (x,y))]
    
    # Add non-target corners to taboo cells
    taboo = [(x,y) for x,y in corners if (x,y) not in warehouse.targets]
    
    #Pair all corners with all other corners and put in list
    all_corner_pairs = itertools.permutations(corners{,2})
    
    #Check for floor tiles between corners, without targets, and add to taboo list
    
    #Pull each set of corner pairs
    for corner_pair in all_corner_pairs:
        #Check if those corners are in same column
        if vertically_aligned(corner_pair[0], corner_pair[1]):
            #Find which are the min and max y values
            if y in x,y in corner_pair[0] < y in x,y in corner_pair[1]:
                        taboo_y_min = y in x,y in corner_pair[0]
                        taboo_y_max = y in x,y in corner_pair[1]
                    else:
                        taboo_y_min = y in x,y in corner_pair[1]
                        taboo_y_max = y in x,y in corner_pair[0]

            target_between_corners = False
            #Check if any targets are between the corners
            for target in warehouse.target: 
                if vertically_aligned(corner_pair[0], target) and (y in target > taboo_y_min) or (y in target < taboo_y_max)):
                    target_between_corners = True
                    break
            if target_between_corners == False
                    taboo_x = x in x,y in corner_pair[0]
                    #Check if each floor cell is in same column and between corners
                    taboo += [(x,y) for x,y in floor_next_to_wall (if x == taboo_x and ((y > taboo_y_min) and (y < taboo_y_max)))]  

                    
        else if horizontally_aligned(corner_pair[0], corner_pair[1])
                    #Check if those corners are in same row
                    if horizontally_aligned(corner_pair[0], corner_pair[1]):
                    #Find which are the min and max x values
                    if x in x,y in corner_pair[0] < x in x,y in corner_pair[1]:
                        taboo_x_min = x in x,y in corner_pair[0]
                        taboo_x_max = x in x,y in corner_pair[1]
                    else:
                        taboo_x_min = x in x,y in corner_pair[1]
                        taboo_x_max = x in x,y in corner_pair[0]

                    target_between_corners = False
                    #Check if any targets are between the corners
                    for target in warehouse.target: 
                        if horizontally_aligned(corner_pair[0], target) and (x in target > taboo_x_min) or (x in target < taboo_x_max)):
                            target_between_corners = True
                            break
                    if target_between_corners == False
                        taboo_y = y in x,y in corner_pair[0]
                        #Check if each floor cell is in same column and between corners and add to taboo list 
                        taboo += [(x,y) for x,y in floor_next_to_wall (if y == taboo_y and ((x > taboo_x_min) and (x < taboo_x_max)))]  

#DONE
def is_corner(warehouse, floor_cell):
    x,y = floor_cell[0], floor_cell[1]
    #if in a lower right hand corner
    if ((x + 1,y) in warehouse.walls) and ((x, y + 1) in warehouse.walls)):
        return true
    if ((x - 1,y) in warehouse.walls) and ((x, y + 1) in warehouse.walls)):
        return true
    if ((x - 1,y) in warehouse.walls) and ((x, y - 1) in warehouse.walls)):
        return true
    if ((x + 1,y) in warehouse.walls) and ((x, y - 1) in warehouse.walls)):
        return true
    
    return false
    
def get_dist_to_closest_cell(origin, cells):
    min_distance = 0
    if len(cells) > 0:
        min_distance = manhattan_distance(origin, cells[0])
        
        for cell in cells:
# end of observable code on this method.

def get_hungarian_assignment(boxes, targets):
    # There must be an even number of coordinates
    assert(len(boxes) == len(targets))
# end of observable code on this method.
    
def manhattan_distance(cell_a, cell_b):
    return abs(cell_a[0] - cell_b[0]) + abs(cell_a[1] - cell_b[1])
# end of observable code on this method.

#DONE
def is_next_to_wall(warehouse, cell):
    x,y = cell[0], cell[1]
    if ((x + 1, y) in warehouse.walls or (x - 1, y) in warehouse.walls or (x, y + 1) in warehouse.walls or (x, y - 1) in warehouse.walls):
        return True
    else:
        return False


def next_to(cell_a, cell_b):
    if(abs(cell_a[0] - cell_b[0])) == 1 or abs(cell_a[1] - cell_b[1]) == 1:
        return true
    return flase
# end of observable code on this method.

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

def direction(origin, destination):
    if horizontally_aligned(destination, origin):
# end of observable code on this method.

def adjacent_cells(cell):
    x,y = cell[0], cell[1]
# end of observable code on this method.

#DONE
def horizontally_aligned(cell_a, cell_b):
    if cell_a[1] == cell_b[1]:
        return true

#DONE
def vertically_aligned(cell_a, cell_b):
    if cell_a[0] == cell_b[0]:
        return true

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
    """Set the initial state of the problem to the warehouse passed."""
        self.initial = warehouse

	#DONE
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state 
        if these actions do not push a box in a taboo cell.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']        
        """
        
        OK_actions = []
        
        #what is to the (direction), is it a wall or a box?
        cell_to_right = cell_in_direction(state.worker, "Right")
        cell_to_left = cell_in_direction(state.worker, "Left")
		cell_up = cell_in_direction(state.worker, "Up")
		cell_down = cell_in_direction(state.worker, "Down")
		
        #if no wall or box on the right, add it to action list
        if cell_to_right not in state.walls and cell_to_right not in state.boxes:
            OK_actions += "Right"
		#if box on right, check it out
        elif cell_to_right in state.boxes:
			#what's on box's right?
            box_right = cell_in_direction(cell_to_right, "Right")
			#if box's right is good, add right to action list
            if box_right not in taboo_cells(state) and box_right not in state.walls:
                OK_actions += "Right"
		
		#if no wall or box on the left, add it to action list
        if cell_to_left not in state.walls and cell_to_left not in state.boxes:
            OK_actions += "Left"
		#if box on left, check it out
        elif cell_to_left in state.boxes:
			#what's on box's left?
            box_left = cell_in_direction(cell_to_right, "Left")
			#if box's left is good, add left to action list
            if box_left not in taboo_cells(state) and box_left not in state.walls:
                OK_actions += "Left"
        
		#exact same thing as above, but for up and down directions
        if cell_up not in state.walls and cell_up not in state.boxes:
            OK_actions += "Up"
        elif cell_up in state.boxes:
            box_up = cell_in_direction(cell_up, "Up")
            if box_up not in taboo_cells(state) and box_up not in state.walls:
                OK_actions += "Up"

		if cell_down not in state.walls and cell_down not in state.boxes:
            OK_actions += "Down"
        elif cell_down in state.boxes:
            box_down = cell_in_direction(cell_down, "Down")
            if box_down not in taboo_cells(state) and box_down not in state.walls:
                OK_actions += "Down"     

    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError
	
	#DONE
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        if (set(state.boxes) & set(state.targets)) == len(state.boxes)
			return True
		else
			return False
		
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
  

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
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
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


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
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

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
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

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
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


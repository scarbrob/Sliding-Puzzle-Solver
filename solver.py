"""
The solver file for Adam Smith's sliding puzzle.
This file uses A* to solve the 15 sliding puzzle and those with less elements.
@author Benjamin Scarbrough
@version 9/29/19
"""

"""
Imports.
"""
import sys
import heapq
import xxhash
import numpy as np
from itertools import chain


# def main():
    # """
    # A main method used for testing.
    # Uncomment to use.
    # """
    # solve([[6,5,2,3],[0,7,11,4],[9,1,10,8],[15,14,13,12]]) # Square Puzzle
    # solve([[1,2,3,4],[0,5,6,7],[9,10,11,8]]) # Easy Puzzle
    # solve([[5,4],[3,0],[1,2]])
    # solve([[0,3],[2,1]])
    # solve([[2,1,3,4],[5,6,7,8],[9,10,11,0]]) #Impossible
    # solve([[10,5,3,7],[2,9,8,4],[11,1,6,0]])
    # solve([[1,8,2],[0,4,3],[7,6,5]])
    # solve([[7,5,10],[11,2,3],[6,4,1],[9,8,0]])
    # solve([[2,6,5,4],[7,0,9,11],[1,10,3,15],[13,14,12,8]])


def solve(puzzle):
    """
    This is a function to solve the given puzzle. This takes a list as input.
    """
    print("Solving...")
    array_puzzle = np.asarray(puzzle)
    array_puzzle.flags.writeable = False # Turn off writable flags to prevent data being ovewritten accidentally.
    goal_state = __generate_goal(len(array_puzzle[0]), len(array_puzzle))

    flat_puzzle = list(chain.from_iterable(puzzle)) # Flatten the list

    # If the puzzle doesn't contain 0, exit.
    try:
        flat_puzzle.remove(0) # Remove 0 from the list
    except:
        print("All puzzles must include an open tile (0).")
        return None

    inversions = __count_inversions(flat_puzzle) # Count the inversions

    # width = len(array_puzzle[0]) # Get the width of the puzzle (columns)
    # length = len(array_puzzle) # Get the length of the puzzle (rows)

    oddEven = __odd_or_even(len(array_puzzle[0])) # Determine if the width is odd or even.
    start_position = __find_start(array_puzzle) # Find the start position's row
    solvable = __is_solvable(oddEven, inversions, len(array_puzzle), start_position) # Cleck if the puzzle is solvable.

    # If the puzzle is not solvable, return None.
    if(solvable == "None"):
        return None

    # If we cannot calculate a* (for example the given values are not all in sequential order (1-5) 4 is replaced by 6 (1,2,3,5,6))
    try:
        return __a_star(array_puzzle, goal_state)
    except:
        print("Please make sure there are no duplicate or skipped inputs.")
        return None

        # This code was used in testing to print out the string.
    # solved = __a_star(array_puzzle, goal_state)
    # Return the moves needed to complete the puzzle.
    # return print(str(__build_string(solved)) + " (" + str(len(solved)) + ")")


def __a_star(puzzle, goal):
    """
    This function takes a puzzle and its solved state as input, then finds the a best way to solve it.
    """
    # Make the goal state.
    goal_state = State(goal, 0, '', goal)
    # Make the first state.
    init_state = State(puzzle, 0, '', goal)

    # Make all the lists.
    open_list = list()
    temp_open_list = set()
    closed_list = set()

    # Push initial state to open list.
    heapq.heappush(open_list, init_state)
    temp_open_list.add(init_state)

    # While elements exist in the open list, loop.
    while open_list:
        # Pop the node and add it to the closed list.
        popped_node = heapq.heappop(open_list)
        list_states = popped_node._State__get_neighbors(goal) # Must add _State in front to call private method.
        temp_open_list.remove(popped_node)
        closed_list.add(popped_node)

        # If state is goal, return the path.
        if(popped_node == goal_state):
            return popped_node._State__get_path() # Must add _State in front to call private method.

        # Check all the child states (neighbors).
        for state in list_states:
            if state in temp_open_list:
                continue
            elif state in closed_list:
                continue
            else:
                # Combine the paths.
                state._State__combine_path(popped_node) # Must add _State in front to call private method.
                # Push the new state to the open list.
                heapq.heappush(open_list, state)
                temp_open_list.add(state)

    # Check for errors.
    if state != goal_state:
        sys.exit("The OPEN list is empty.")


def __count_inversions(puzzle):
    """
    This function counts the number of inversions.
    """
    puzzleLength = len(puzzle)
    count = 0
    for i in range(puzzleLength):
        for j in range(i + 1, puzzleLength):
            if(puzzle[i] > puzzle[j]):
                count += 1
    return count


def __odd_or_even(number):
    """
    This function returns 0 for even, and 1 for odd.
    """
    if(number % 2) == 0:
        return 0
    else:
        return 1


def __find_start(puzzle):
    """
    Find the row with the start point. The start point is defined as 0.
    [[1,2,3,4], [5,6,0,7]] would return 1.
    """
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == 0:
                return i
    return 0


def __is_solvable(evenOrOdd, inversions, rows, start):
    """
    Check if the puzzle is solvable.
    """
    if(evenOrOdd == 0):
        distance = (rows - 1) - start # calculate the distance of the start point from the bottom.
        solvable = inversions + distance
        if(__odd_or_even(solvable) != 0):
            return "None"
    if(evenOrOdd == 1 and __odd_or_even(inversions)!= 0):
        return "None"
    return "Ok"


def __generate_goal(width, length):
    """
    Generates the goal state.
    """
    goal = np.arange(1, ((width * length)+1)).reshape(length, width)
    goal[length - 1][width - 1] = 0
    return goal


    # This was the string builder method for the returned string.
# def __build_string(a_string):
#     """
#     A function to build the returned string.
#     """
#     string = ("[")
#     for i in range(len(a_string) -1):
#         string += ('\'')
#         string += (a_string[i])
#         string += ('\'')
#         string += (',')
#     string += ('\'')
#     string += (a_string[len(a_string) -1])
#     string += ('\'')
#     string += ("]")
#     return string


# The state class.
class State():
    """
    This is a class that determines the state of a board.
    """

    def __init__(self, puzzle, g, path, goal):
        """
        The constructor of the state class. Set everything up.
        """
        self.puzzle = puzzle
        self.puzzle.flags.writeable = False # Turn off writable flags to prevent data being ovewritten accidentally.
        self.g = g
        self.h = self.__cost_to_goal(goal)
        self.path = path


    def __cost_to_goal(self, goal_state):
        """
        A method that calculates the cost to go from the state to goal.
        The distance of every start node to its goal position, w/o the gap (0).
        """
        cost = 0
        for i in range(len(goal_state) * len(goal_state[0])):
            if(i != 0):
                pos_goal = self.__get_position(i, goal_state)
                pos_current = self.__get_position(i, self.puzzle)
                cost += self.__manhattan(pos_current[0], pos_current[1], pos_goal[0], pos_goal[1])
        return cost


    def __combine_path(self, other):
        """
        A method used to combine the paths of two states.
        """
        self.path = other.path + self.path


    def __get_path(self):
        """
        A method to get the path of a state.
        """
        return self.path


    def __manhattan(self, x_state, y_state, x_goal, y_goal):
        """
        Calculate the manhattan distance.
        """
        distance = (abs(x_state - x_goal) + abs(y_state - y_goal))
        return distance


    def __get_position(self, value, state):
        """
        Get the coordinates of value in the state.
        """
        coords = np.argwhere(state == value).flatten()
        return coords


    def __swap(self, x1, y1, x2, y2):
        """
        This is a method used to swap elements of the puzzle.
        """
        temp = self.puzzle.copy()
        temp[x1, y1] = temp[x2, y2]
        temp[x2, y2] = self.puzzle[x1, y1]
        return temp


    def __get_neighbors(self, goal):
        """
        This is a method to get the neighbors of the state.
        """
        neighbors = set()
        start = self.__get_position(0, self.puzzle)
            # start_x = start[0]
            # start_y = start[1]
        # Get the below neighbor.
        if(start[0] - 1 >= 0):
            temp = self.__swap(start[0], start[1], start[0] - 1, start[1])
            neighbors.add(State(temp, self.g + 1, 'D', goal))
        # Get the above neighbor
        if(start[0] + 1 <= len(self.puzzle) -1):
            temp = self.__swap(start[0], start[1], start[0] + 1, start[1])
            neighbors.add(State(temp, self.g + 1, 'U', goal))
        # Get the right neighbor
        if(start[1] - 1 >= 0):
            temp = self.__swap(start[0], start[1], start[0], start[1] - 1)
            neighbors.add(State(temp, self.g + 1, 'R', goal))
        # Get the left neighbor
        if(start[1] + 1 <= len(self.puzzle[0]) -1):
            temp = self.__swap(start[0], start[1], start[0], start[1] + 1)
            neighbors.add(State(temp, self.g + 1, 'L', goal))

        return neighbors


    def __lt__(self, other):
        """
        A magic less than method. Compare f(x) = g(x) + h(x) values.
        """
        f_self = self.g + self.h
        f_other = other.g + other.h
        if(f_self < f_other):
            return True
        return False


    def __hash__(self):
        """
        A magic hash method that uses xxhash to speed things up.
        """
        x = xxhash.xxh64()
        x.update(self.puzzle)
        return x.intdigest()


    def __eq__(self, other):
        """
        A magic equals method used for comparing states.
        """
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[0])):
                if(self.puzzle[i][j] != other.puzzle[i][j]):
                    return False
        return True


    def __str__(self):
        """
        A magic string function.
        """
        value = str(self.puzzle) + str(" ") + str(self.g) + str(" ") + str(self.h)
        return value

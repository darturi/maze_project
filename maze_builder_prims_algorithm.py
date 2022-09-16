import math
import random
from random import randrange


def create_blank_maze(row_num, col_num):
    return_array = []
    for row in range(row_num):
        row_list = []
        for col in range(col_num):
            row_list.append(['u'])
        return_array.append(row_list)
    return return_array


def select_random_start_cell(height, width):
    # Pick random index for start cell
    x_coordinate = 1 + randrange(height - 2)
    y_coordinate = 1 + randrange(width - 2)

    return [x_coordinate, y_coordinate]


# Checks if the cell passed in as the third parameter is a border
def check_if_border(height, width, cell):
    x, y = cell[0], cell[1]
    if x == 0 or x == height - 1 or y == 0 or y == width - 1:
        # Returns true if the cell is in fact a border cell
        return True
    # Returns false if the cell is not a border cell
    return False


def get_adj_cells(height, width, cell):
    x, y = cell[0], cell[1]

    # Creates a list of all cells adjacent to the one passed in as input
    adj_cell_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]

    # Remove all the cells that are adjacent to the original cell but are walls
    non_border_cells = []
    for i in adj_cell_list:
        if not check_if_border(height, width, i):
            non_border_cells.append(i)

    # return the results of the calculations of the function
    return non_border_cells


#def check_wall_division(wall_cell, visited_cell):
#    w_x, w_y, v_x, v_y = wall_cell[0], wall_cell[1], visited_cell[0], visited_cell[1]
#    # Determine if horizontally or vertically adjacent
#    if math.abs(w_x - v_x) == 1:
#        pass


# Using this function using the coordinates from a wall cell the program can determine the nearest visited cell
def get_adj_visited_cell(height, width, wall_cell, visited_cells):
    adj_cells = get_adj_cells(height, width, wall_cell)
    for cell in adj_cells:
        if cell in visited_cells:
            return cell


def maze_creator():
    # define height and width
    height = 5
    width = 10

    # create blank maze
    maze = create_blank_maze(height, width)

    # initialize relevant lists
    visited_cells = []

    # start off the program with a single random cell
    start_cell = select_random_start_cell(height, width)
    # Add cell to visited cells list
    visited_cells.append(start_cell)
    # Edit graphical representation to reflect visitation of random start cell
    maze[start_cell[0]][start_cell[1]] = ["v"]

    for i in maze:
        print(i)

    # Initialize list of wall cells
    wall_list = get_adj_cells(height, width, start_cell)

    print("start cell:", start_cell)
    print("wall_list:", wall_list)

    # Next bit should be contained in a while loop that loops while length of wall_list > 0
    # However for testing purposes at the moment it will be a standalone

    wall_cell = random.choice(wall_list)
    print("wall_cell:", wall_cell)

    print("Nearest Visited Cell:", get_adj_visited_cell(height, width, wall_cell, visited_cells))


def main():
    maze_creator()
    # print(get_adj_cells(5, 10, [1, 1]))
    # print(check_if_border(5, 10, [2, 2]))


main()

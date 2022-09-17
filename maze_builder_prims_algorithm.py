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


def get_adj_cells(height, width, cell, previously_checked_walls=[]):
    x, y = cell[0], cell[1]

    # Creates a list of all cells adjacent to the one passed in as input
    adj_cell_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]

    # Remove all the cells that are adjacent to the original cell but are walls
    non_border_cells = []
    for i in adj_cell_list:
        if not check_if_border(height, width, i) and i not in previously_checked_walls:
            non_border_cells.append(i)

    # return the results of the calculations of the function
    return non_border_cells


# Returns True if wall divides two visited cells or False if not
# (if it's False delete the wall)
def check_wall_division(height, width, wall_cell, visited_cells_list):
    x, y = wall_cell[0], wall_cell[1]
    visited_cell = get_adj_visited_cell(height, width, wall_cell, visited_cells_list)

    # Creates a list of all cells adjacent to the one passed in as input
    adj_cells = [[[x, y - 1], [x, y + 1]], [[x - 1, y], [x + 1, y]]]
    if visited_cell in adj_cells[0]:
        adj_cells = adj_cells[0]
    else:
        adj_cells = adj_cells[1]

    adj_cells.remove(visited_cell)
    print("opposite cell:", adj_cells[0])
    if adj_cells[0] in visited_cells_list:
        return True
    else:
        return False


def get_unvisited_cell(height, width, wall_cell, visited_cells_list):
    x, y = wall_cell[0], wall_cell[1]
    visited_cell = get_adj_visited_cell(height, width, wall_cell, visited_cells_list)

    # Creates a list of all cells adjacent to the one passed in as input
    adj_cells = [[[x, y - 1], [x, y + 1]], [[x - 1, y], [x + 1, y]]]
    if visited_cell in adj_cells[0]:
        adj_cells = adj_cells[0]
    else:
        adj_cells = adj_cells[1]

    adj_cells.remove(visited_cell)
    return adj_cells[0]



# Using this function using the coordinates from a wall cell the program can determine the nearest visited cell
def get_adj_visited_cell(height, width, wall_cell, visited_cells):
    adj_cells = get_adj_cells(height, width, wall_cell)
    for cell in adj_cells:
        if cell in visited_cells:
            return cell


def maze_creator():
    # define height and width
    height = 10
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
    previously_checked_walls = []

    #print("start cell:", start_cell)
    #print("wall_list:", wall_list)

    # Next bit should be contained in a while loop that loops while length of wall_list > 0
    # However for testing purposes at the moment it will be a standalone

    #wall_cell = random.choice(wall_list)
    #print("wall_cell:", wall_cell)

    #print("Nearest Visited Cell:", get_adj_visited_cell(height, width, wall_cell, visited_cells))
    #wall_div = check_wall_division(wall_cell,
                                   #get_adj_visited_cell(height, width, wall_cell, visited_cells),
                                   #visited_cells)
    #print("wall_div", wall_div)

    print("\n\n\n")

    while len(wall_list) > 0:
        wall_cell = random.choice(wall_list)
        previously_checked_walls.append(wall_cell)
        wall_div = check_wall_division(height, width, wall_cell, visited_cells)
        # visited_cell = get_adj_visited_cell(height, width, wall_cell, visited_cells)
        unvisited_cell = get_unvisited_cell(height, width, wall_cell, visited_cells)

        #for cell in wall_list:
        #    if cell in wall_list and cell in visited_cells:
        #        wall_list.remove(cell)

        # Just Printing for debugging
        for i in maze:
            print(i)
        print("wall cell:", wall_cell,
              "\nwall list:", wall_list,
              "\nwall div:", wall_div,
              "\nvisited cells:", visited_cells, "\n")

        if not wall_div:
            # make wall a passage
            visited_cells.append(wall_cell)
            maze[wall_cell[0]][wall_cell[1]] = ['v']

            # Correction to the below few lines of code: That is adding the nearest already visited cell, we need the
            # nearest, as of yet, UNvisited cell. That is to say the cell across from the one currently being added

            # make nearest adj cell a passage
            if not check_if_border(height, width, unvisited_cell):
                visited_cells.append(unvisited_cell)
                maze[unvisited_cell[0]][unvisited_cell[1]] = ['v']

            for cell in get_adj_cells(height, width, wall_cell, previously_checked_walls):
                if cell not in visited_cells:
                    wall_list.append(cell)

        wall_list.remove(wall_cell)

        # Could definitely come up with a more efficient way to do this
        wall_holder_list = []
        for cell in wall_list:
            if cell not in wall_holder_list:
                wall_holder_list.append(cell)

        wall_list = wall_holder_list


#    while len(wall_list) > 0:
#        wall_cell = random.choice(wall_list)
        # print("wall_cell", wall_cell)
        # wall_list.remove(wall_cell)
        # previously_checked_walls.append(wall_cell)
        # print(wall_list)

        # previously_checked_walls.append(wall_cell)
        # wall_list.remove(wall_cell)

#        wall_div = check_wall_division(wall_cell,
#                                       get_adj_visited_cell(height, width, wall_cell, visited_cells),
#                                       visited_cells)
#        if not wall_div:
            # Mark cell as visited
#            visited_cells.append(wall_cell)
            # Visually reflect that marking
#            maze[wall_cell[0]][wall_cell[1]] = ['v']

#        for cell in get_adj_cells(height, width, start_cell, previously_checked_walls):
#            if cell not in wall_list:
#                wall_list.append(cell)

        # previously_checked_walls.append(wall_cell)
        # wall_list.remove(wall_cell)

    for i in maze:
        print(i)


def main():
    maze_creator()
    # print(get_adj_cells(5, 10, [1, 1]))
    # print(check_if_border(5, 10, [2, 2]))


main()

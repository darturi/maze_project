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
#def check_wall_division(height, width, wall_cell, checked_cells, maze):
#    x, y = wall_cell[0], wall_cell[1]
#    visited_cell = get_adj_visited_cell(height, width, wall_cell, checked_cells)
#
#    # Creates a list of all cells adjacent to the one passed in as input
#    adj_cells = [[[x, y - 1], [x, y + 1]], [[x - 1, y], [x + 1, y]]]
#    if visited_cell in adj_cells[0]:
#        adj_cells = adj_cells[0]
#    else:
#        adj_cells = adj_cells[1]
#
#    adj_cells.remove(visited_cell)
#    print("opposite cell:", adj_cells[0])
#    adj_x, adj_y = adj_cells[0][0], adj_cells[0][1]
#    if maze[adj_x][adj_y] != ['u']:
#        return True
#    else:
#        return False


def check_wall_division(height, width, wall_cell, checked_cells, maze):
    x, y = wall_cell[0], wall_cell[1]

    # Creates a list of all cells adjacent to the one passed in as input
    adj_cells = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]

    checked_count = 0
    for cell in adj_cells:
        if maze[cell[0]][cell[1]] == ['c']:
            checked_count += 1

    if checked_count < 2:
        return False
    return True


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

    unchecked_cells = [[i, j] for i in range(width) for j in range(height)]
    checked_cells = []
    wall_cell_list = []

    # create blank maze
    maze = create_blank_maze(height, width)

    # Setting up the starting checked cell
    start_cell = select_random_start_cell(height, width)
    maze[start_cell[0]][start_cell[1]] = ['c']
    checked_cells.append(start_cell)

    # Setting up the starting wall cells
    for wall_cell in get_adj_cells(height, width, start_cell):
        maze[wall_cell[0]][wall_cell[1]] = ['w']
        wall_cell_list.append(wall_cell)

    # update unchecked cell list
    unchecked_cells.remove(start_cell)
    for cell in wall_cell_list:
        unchecked_cells.remove(cell)

    for i in maze:
        print(i)

    while len(wall_cell_list) > 0:
        wall_cell = random.choice(wall_cell_list)
        print("wall cell:", wall_cell)
        check_div = check_wall_division(height, width, wall_cell, checked_cells, maze)
        print("check_div", check_div)

        if not check_div:
            checked_cells.append(wall_cell)
            maze[wall_cell[0]][wall_cell[1]] = ['c']
            adj_cells = get_adj_cells(height, width, wall_cell)
            print('adj_cells', adj_cells)
            for cell in adj_cells:
                if cell not in checked_cells and cell not in wall_cell_list:
                    wall_cell_list.append(cell)
                    maze[cell[0]][cell[1]] = ['w']

                    # update unchecked cell list
                    if cell in unchecked_cells:
                        unchecked_cells.remove(cell)

        wall_cell_list.remove(wall_cell)

    # Convert unvisited cells to walls
    for cell in unchecked_cells:
        x, y = cell[0], cell[1]
        wall_cell_list.append(cell)
        maze[x][y] = ['w']

    for i in maze:
        print(i)


def main():
    maze_creator()


main()

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
    y_coordinate = 1 + randrange(height - 2)
    x_coordinate = 1 + randrange(width - 2)

    return [x_coordinate, y_coordinate]


def maze_creator():
    # define height and width
    height = 5
    width = 10

    # create blank maze
    maze = create_blank_maze(height, width)

    # initialize relevant lists
    wall_list = []
    visited_cells = []

    # start off the program with a single random cell
    start_cell = select_random_start_cell(height, width)
    visited_cells.append(start_cell)


def main():
    for i in create_blank_maze(5, 10):
        print(i)


main()

from parser import detect_grid
from solver import initialize_grid, get_path_nodes, solve, is_valid_solution
import copy
from renderer import render_solution
import cv2

grid_img, rows, cols, cell_width, cell_height, dots, reverse_color_map = detect_grid("9_2.jpeg")

grid = initialize_grid(rows, cols, dots)
starts, targets = get_path_nodes(dots)

path_ends = copy.deepcopy(starts)
if solve(grid, rows, cols, path_ends, targets):
    if is_valid_solution(grid, rows, cols, starts, targets):
        print("Solved!")
        output = render_solution(grid_img, grid, rows, cols, cell_width, cell_height, reverse_color_map)
        cv2.imshow("Solution", output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Invalid solution")
else:
    print("No solution found")
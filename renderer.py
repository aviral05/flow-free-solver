import cv2

def render_solution(grid_img, grid, rows, cols, cell_width, cell_height, reverse_color_map):
    output = grid_img.copy()
    overlay = grid_img.copy()
    
    for r in range(rows):
        for c in range(cols):
            color_id = grid[r][c]
            if color_id == -1:
                continue
            color = reverse_color_map[color_id]
            x1 = int(c * cell_width)
            x2 = int(c * cell_width + cell_width)
            y1 = int(r * cell_height)
            y2 = int(r * cell_height + cell_height)
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
    
    cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)
    return output
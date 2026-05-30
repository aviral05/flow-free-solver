import cv2
import numpy as np


def detect_grid(path):
    img = cv2.imread(path)
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grayimg, 50, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    grid_img = img[y:y+h, x:x+w]

    grid_gray = cv2.cvtColor(grid_img, cv2.COLOR_BGR2GRAY)
    grid_gray_dark = cv2.convertScaleAbs(grid_gray, alpha=0.5, beta=0)
    _, dot_thresh = cv2.threshold(grid_gray_dark, 20, 255, cv2.THRESH_BINARY_INV)

    edges = cv2.Canny(grid_gray, 50, 255)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=w*0.8, maxLineGap=10)

    horizontal = []
    vertical = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y2 - y1) < 10:
            horizontal.append(y1)
        elif abs(x2 - x1) < 10:
            vertical.append(x1)

    horizontal = deduplicate(horizontal)
    vertical = deduplicate(vertical)

    rows = len(horizontal) - 1
    cols = len(vertical) - 1
    cell_height = h / rows
    cell_width = w / cols

    dot_positions = []
    for r in range(rows):
        for c in range(cols):
            cx = int(c * cell_width + cell_width / 2)
            cy = int(r * cell_height + cell_height / 2)
            if dot_thresh[cy, cx] <= 200:
                dot_positions.append((r, c, cy, cx))

    color_map = {}
    color_id = 0
    dots = {}

    for r, c, cy, cx in dot_positions:
        pixel = tuple(grid_img[cy, cx].tolist())
        matched = None
        for existing in color_map:
            if color_distance(pixel, existing) < 30:
                matched = existing
                break
        if matched:
            dots[(r, c)] = color_map[matched]
        else:
            color_map[pixel] = color_id
            dots[(r, c)] = color_id
            color_id += 1

    reverse_color_map = {v: k for k, v in color_map.items()}
    return grid_img, rows, cols, cell_width, cell_height, dots, reverse_color_map


def deduplicate(values, threshold=10):
    values = sorted(values)
    result = [values[0]]
    for i in range(1, len(values)):
        if abs(values[i] - result[-1]) > threshold:
            result.append(values[i])
    return result


def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5
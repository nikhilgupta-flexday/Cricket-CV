import cv2
import numpy as np

def check_violation_simple(shoe_box, line_box, buffer_percent=0.05):
    shoe_x1, shoe_y1, shoe_x2, shoe_y2 = shoe_box
    line_x1, line_y1, line_x2, line_y2 = line_box
    
    line_center_x = (line_x1 + line_x2) / 2
    shoe_width = shoe_x2 - shoe_x1
    
    buffer = shoe_width * buffer_percent
    effective_shoe_x1 = shoe_x1 + buffer
    effective_shoe_x2 = shoe_x2 - buffer
    
    if effective_shoe_x1 < line_center_x < effective_shoe_x2:
        dist_from_left = line_center_x - effective_shoe_x1
        dist_from_right = effective_shoe_x2 - line_center_x
        effective_width = effective_shoe_x2 - effective_shoe_x1
        
        min_dist = min(dist_from_left, dist_from_right)
        confidence = min_dist / (effective_width / 2)
        
        return True, confidence
    
    return True, 0.0

# Linear interpolation between line width at top and bottom of the bounding box to infer the line width
# as well as interpolation along the slope of the box diagonal to infer the line midpoint
def check_violation_perspective(frame, shoe_box, line_box, tolerance=10):
    shoe_x1, shoe_y1, shoe_x2, shoe_y2 = shoe_box
    line_x1, line_y1, line_x2, line_y2 = [int(v) for v in line_box]
    
    # Extract line region and find actual line edges
    line_region = frame[line_y1:line_y2, line_x1:line_x2]
    gray = cv2.cvtColor(line_region, cv2.COLOR_BGR2GRAY)
    
    # Lower threshold for garage lighting
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    height = thresh.shape[0]
    
    # Scan at 20% and 80% of height instead of fixed pixels from edges
    top_row = int(height * 0.2)
    bottom_row = int(height * 0.8)
    
    top_indices = np.where(thresh[top_row, :] > 0)[0]
    bottom_indices = np.where(thresh[bottom_row, :] > 0)[0]
    
    if len(top_indices) == 0 or len(bottom_indices) == 0:
        return False, 0.0
    
    # Get line center at top and bottom
    top_center = line_x1 + (top_indices[0] + top_indices[-1]) / 2
    bottom_center = line_x1 + (bottom_indices[0] + bottom_indices[-1]) / 2
    top_width = top_indices[-1] - top_indices[0]
    bottom_width = bottom_indices[-1] - bottom_indices[0]
    
    # Interpolate line position at shoe's y level
    shoe_mid_y = (shoe_y1 + shoe_y2) / 2
    t = (shoe_mid_y - (line_y1 + top_row)) / ((line_y1 + bottom_row) - (line_y1 + top_row))
    t = max(0, min(1, t))
    
    line_center = top_center + t * (bottom_center - top_center)
    line_width = top_width + t * (bottom_width - top_width)
    
    # Check if shoe right edge crosses line left edge
    line_left_edge = line_center - (line_width / 2)
    penetration = shoe_x2 - line_left_edge
    
    if penetration > tolerance:
        confidence = min(penetration / max(line_width, 1), 1.0)
        return True, confidence
    
    return False, 0.0
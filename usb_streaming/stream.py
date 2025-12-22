import cv2
import time, os
from ultralytics import YOLO
from datetime import datetime

model = YOLO('best_cricket.pt') # example model
save_folder = 'saved'
os.makedirs(save_folder, exist_ok=True)

def run_inference(frame):
    results = model(frame)
    
    line_box = None
    shoe_boxes = []
    
    for box in results[0].boxes:
        class_id = int(box.cls[0].item())
        coords = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
        confidence = box.conf[0].item()
        class_name = model.names[class_id]
        
        if class_name == 'line':
            line_box = coords
        elif class_name == 'shoe':
            shoe_boxes.append(coords)
    
    # If either missing, no violation possible
    if line_box is None or len(shoe_boxes) == 0:
        return results, False, None
    
    # Check each shoe
    for shoe in shoe_boxes:
        violation, confidence = check_line_violation(shoe, line_box)
        if violation:
            return results, True, confidence
    
    return results, False, None

# given coordinates of the shoe and the line, can we calculate a confidence that they are touching?
def check_line_violation(shoe_box, line_box, buffer_percent=0.05):
    shoe_x1, shoe_y1, shoe_x2, shoe_y2 = shoe_box
    line_x1, line_y1, line_x2, line_y2 = line_box
    
    line_center_x = (line_x1 + line_x2) / 2
    shoe_width = shoe_x2 - shoe_x1
    
    # Add buffer to edges in case of close calls
    buffer = shoe_width * buffer_percent
    effective_shoe_x1 = shoe_x1 + buffer
    effective_shoe_x2 = shoe_x2 - buffer
    
    if effective_shoe_x1 < line_center_x < effective_shoe_x2:
        # Calculate confidence
        dist_from_left = line_center_x - effective_shoe_x1
        dist_from_right = effective_shoe_x2 - line_center_x
        effective_width = effective_shoe_x2 - effective_shoe_x1
        
        min_dist = min(dist_from_left, dist_from_right)
        confidence = min_dist / (effective_width / 2)
        
        return True, confidence
    
    return False, 0.0

def find_cam():
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                print(f"Index {i}: {w}x{h}")
            cap.release()

def main():
    # Find available cameras first
    find_cam()
    
    # Set camera index (change this to match your GoPro)
    CAMERA_INDEX = 1
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print(f"ERROR: Could not open camera at index {CAMERA_INDEX}")
        return
    
    # let the gopro connection establish before checking frames
    time.sleep(2)

    # discard a few frames while the camera calibrates
    for _ in range(10):
        cap.read()

    # Can set the resolution this way in the future
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print(f"Successfully connected to camera {CAMERA_INDEX}")
    print("Press 'q' to quit, 's' to save a frame")    
    frame_count = 0
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to read frame")
            break
        frame_count += 1

        # Calculate FPS every 30 frames
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            h, w = frame.shape[:2]
            print(f"Frame {frame_count} | {w}x{h} | {fps:.1f} FPS")
        
        # Run inference
        results, violation, confidence = run_inference(frame)
        
        # Draw detections
        annotated_frame = results[0].plot()
        
        # Add violation indicator
        if violation:
            cv2.putText(annotated_frame, f"STEPPING ON LINE: ({confidence:.0%})", 
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        
        # Display the frame
        cv2.imshow('GoPro Stream', annotated_frame)
        
        # Handle quit and save
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = os.path.join(save_folder, f'frame_{timestamp}.jpg')
            cv2.imwrite(filename, annotated_frame)
            print(f"Saved {filename}")
    
    # unmount camera and connections
    cap.release()
    cv2.destroyAllWindows()
    
    total_time = time.time() - start_time
    print(f"\nProcessed {frame_count} frames in {total_time:.1f}s ({frame_count/total_time:.1f} FPS)")

if __name__ == '__main__':
    main()
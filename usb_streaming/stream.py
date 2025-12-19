import cv2
import time, os
from ultralytics import YOLO
from datetime import datetime

model = YOLO('yolov8n-pose.pt') # example model
save_folder = 'saved'
os.makedirs(save_folder, exist_ok=True)

def run_inference(frame):
    # Plugin .pt model when it is done
    results = model(frame)
    return results

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
        results = run_inference(frame)
        
        if results is not None:
            # do something with results when they are integrated
            frame = results[0].plot()
            #pass
        
        # Display the frame
        cv2.imshow('GoPro Stream', frame)
        
        # Handle quit and save
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = os.path.join(save_folder, f'frame_{timestamp}.jpg')
            cv2.imwrite(filename, frame)
            print(f"Saved {filename}")
    
    # unmount camera and connections
    cap.release()
    cv2.destroyAllWindows()
    
    total_time = time.time() - start_time
    print(f"\nProcessed {frame_count} frames in {total_time:.1f}s ({frame_count/total_time:.1f} FPS)")

if __name__ == '__main__':
    main()
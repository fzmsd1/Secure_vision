from ultralytics import YOLO
import cv2
import math


def video_detection(path_x):
    video_capture = path_x
    cap = cv2.VideoCapture(video_capture)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
    model = YOLO('best.pt')
    classNames = {0: 'Hardhat', 1: 'Mask', 2: 'NO-Hardhat', 3: 'NO-Mask', 4: 'NO-Safety Vest', 5: 'Person', 6: 'Safety Cone', 7: 'Safety Vest', 8: 'machinery', 9: 'vehicle'}

    # Define colors for each class
    colors = {
        'Hardhat': (255, 0, 0),         # Red
        'Mask': (0, 255, 0),            # Green
        'NO-Hardhat': (0, 0, 255),      # Blue
        'NO-Mask': (255, 255, 0),       # Cyan
        'NO-Safety Vest': (0, 255, 255),# Yellow
        'Person': (255, 0, 255),        # Magenta
        'Safety Cone': (255, 255, 255), # White
        'Safety Vest': (128, 128, 128), # Gray
        'machinery': (128, 0, 128),     # Purple
        'vehicle': (0, 128, 128)        # Teal
    }

    try:
        while True:
            success, img = cap.read()
            if not success:
                break

            results = model(img, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]  # Tensors
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls_index = int(box.cls)
                    if cls_index in classNames:
                        class_name = classNames[cls_index]
                        label = f'{class_name} {conf:.2f}'
                        t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                        c2 = (x1 + t_size[0], y1 - t_size[1] - 3)
                        color = colors.get(class_name, (0, 0, 0))  # Get color for the class or default to black
                        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                        cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)
                        cv2.putText(img, label, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA, False)

            yield img
    finally:
        # Release the video capture object and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

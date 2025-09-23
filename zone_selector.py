import cv2
import json

zones = []
drawing = False
start_point = None

def draw(event, x, y, flags, param):
    global drawing, start_point

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        zones.append((start_point[0], start_point[1], end_point[0], end_point[1]))
        print(f"Zone defined: {zones[-1]}")

def select_zones_from_webcam():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Draw Zones")
    cv2.setMouseCallback("Draw Zones", draw)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Draw current zones
        for (x1, y1, x2, y2) in zones:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

        cv2.imshow("Draw Zones", frame)
        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save zones to JSON
    with open("zones.json", "w") as f:
        json.dump(zones, f)

if __name__ == "__main__":
    select_zones_from_webcam()

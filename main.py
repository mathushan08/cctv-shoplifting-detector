import cv2
import time
import json
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load zones from zones.json
with open("zones.json") as f:
    zones = json.load(f)
SHELF_ZONE = zones[0]
EXIT_ZONE = zones[1]

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Initialize DeepSORT tracker
tracker = DeepSort(max_age=30)

# Person state tracker
person_states = {}

# Utility function: overlap check
def is_inside_zone(bbox, zone):
    bx1, by1, bx2, by2 = bbox
    zx1, zy1, zx2, zy2 = zone
    return not (bx2 < zx1 or bx1 > zx2 or by2 < zy1 or by1 > zy2)

# Optional: crop for better webcam detection


# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

   

    # Run YOLOv8 detection
    results = model(frame, imgsz=640)
    detections = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        label = model.names[cls_id]

        if label == "person" and conf > 0.5:
            detections.append(([x1, y1, x2 - x1, y2 - y1], conf, label))

    # Run DeepSORT tracking
    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = map(int, track.to_ltrb())
        person_box = (l, t, r, b)

        # Initialize state if new
        if track_id not in person_states:
            person_states[track_id] = {
                "entered_shelf": False,
                "picked": False,
                "concealed": False,
                "exited": False,
                "timestamps": {}
            }
        state = person_states[track_id]

        # Shelf zone logic
        if is_inside_zone(person_box, SHELF_ZONE):
            if not state["entered_shelf"]:
                state["entered_shelf"] = True
                state["timestamps"]["shelf"] = time.time()
            else:
                duration = time.time() - state["timestamps"]["shelf"]
                if duration > 2 and not state["picked"]:
                    state["picked"] = True
                    print(f"[PICK] Person {track_id} picked item.")

        # Simulated concealment after pick
        if state["picked"] and not state["concealed"]:
            state["concealed"] = True
            print(f"[CONCEAL] Person {track_id} concealed item.")

        # Exit zone logic
        if state["concealed"] and is_inside_zone(person_box, EXIT_ZONE):
            if not state["exited"]:
                print(f"[ALERT] Person {track_id} EXITED with item!")
                state["exited"] = True
                cv2.imwrite(f"logs/alert_{track_id}_{int(time.time())}.jpg", frame)

        # Draw person box
        color = (0, 255, 0)  # Green by default
        if state["concealed"] and not state["exited"]:
            color = (0, 0, 255)  # Red for suspicious
        cv2.rectangle(frame, (l, t), (r, b), color, 2)
        cv2.putText(frame, f"ID:{track_id}", (l, t - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Draw zones
    zx1, zy1, zx2, zy2 = SHELF_ZONE
    cv2.rectangle(frame, (zx1, zy1), (zx2, zy2), (0, 255, 255), 2)
    cv2.putText(frame, "Shelf Zone", (zx1, zy1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    zx1, zy1, zx2, zy2 = EXIT_ZONE
    cv2.rectangle(frame, (zx1, zy1), (zx2, zy2), (255, 0, 255), 2)
    cv2.putText(frame, "Exit Zone", (zx1, zy1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

    # Show output
    cv2.imshow("Shoplifting Detector", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

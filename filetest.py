import cv2
import numpy as np

# Öffne das Video
cap = cv2.VideoCapture("testdata/ttgame1.mp4")


def get_dur(filename):
    video = cv2.VideoCapture(filename)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    seconds = frame_count / fps
    minutes = int(seconds / 60)
    rem_sec = int(seconds % 60)
    return f"{minutes}:{rem_sec}"

print(get_dur("dafuck.mp4"))
# Prüfen, ob das Video erfolgreich geöffnet wurde
if not cap.isOpened():
    print("Fehler beim Öffnen der Videodatei.")
else:
    print("Videodatei erfolgreich geöffnet.")

for _ in range(frame_count):  # Versuche, nur die ersten 5 Frames zu lesen
    ret, frame = cap.read()
    if not ret:
        print("Kein Frame mehr zum Lesen.")
        break
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
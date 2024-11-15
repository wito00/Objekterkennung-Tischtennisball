import cv2
import numpy as np

# Öffne das Video
cap = cv2.VideoCapture("testdata/ttgame1.mp4")

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# Prüfen, ob das Video erfolgreich geöffnet wurde
if not cap.isOpened():
    print("Fehler beim Öffnen der Videodatei")
    exit()

# Hole die Videoeigenschaften (Breite, Höhe, FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Erstelle einen VideoWriter, um das bearbeitete Video zu speichern
out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

# Farbbereich für Orange im HSV-Farbraum
lower_orange = np.array([5, 150, 150])   # untere Grenze für Orange
upper_orange = np.array([15, 255, 255])  # obere Grenze für Orange

# Kontrastfaktor (z.B. 1.2 für eine leichte Verstärkung des Kontrasts)
alpha = 1.2  # Kontrastfaktor
beta = 0     # Helligkeit (0 bedeutet keine Änderung)

# Verarbeite alle Frames im Video
for i in range(frame_count):
    # Lese den nächsten Frame
    ret, frame = cap.read()

    # Wenn kein Frame mehr vorhanden ist (Ende des Videos)
    if not ret:
        print("Fehler beim Lesen des Frames")
        break

    # **Kontrastanpassung**: Bild mit Kontrastfaktor anpassen
    adjusted_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # Umwandeln in den HSV-Farbraum
    hsv = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2HSV)

    # Maske erstellen, um nur den orange Bereich herauszufiltern
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Optional: Rauschunterdrückung durch Weichzeichnen der Maske
    mask = cv2.GaussianBlur(mask, (15, 15), 0)

    # Finde die Kreise (nur im orangen Bereich)
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=50)

    # Wenn Kreise gefunden wurden
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")  # Konvertiere die Koordinaten zu Ganzzahlen

        for (x, y, r) in circles:
            # Zeichne den Kreis
            cv2.circle(adjusted_frame, (x, y), r, (0, 255, 0), 4)  # Grüner Kreis

            # Zeichne das Zentrum des Kreises
            cv2.circle(adjusted_frame, (x, y), 3, (0, 0, 255), 3)  # Rotes Zentrum

            # Füge den Text "Ball" hinzu
            cv2.putText(adjusted_frame, "Ball", (x - 20, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Schreibe den bearbeiteten Frame in die Ausgabedatei
    out.write(adjusted_frame)

# Ressourcen freigeben und Fenster schließen
cap.release()
out.release()  # Schließe den VideoWriter
cv2.destroyAllWindows()

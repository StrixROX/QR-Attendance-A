import cv2
import os
from datetime import datetime as dt

cam = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

date = dt.today()
fname = "{0:>02d}-{1:>02d}-{2:d}".format(date.day, date.month, date.year)

if not os.path.isdir(os.path.join(os.getcwd(), "attendance")):
    print("> Created folder \"attendance\"")
    os.mkdir(os.path.join(os.getcwd(), "attendance"))

if not os.path.isfile(os.path.join(os.getcwd(), f"attendance\\{fname}.csv")):
    with open(os.path.join(os.getcwd(), f"attendance\\{fname}.csv"), "w") as f:
        f.write("Roll No.,Name,Email\n")

with open(os.path.join(os.getcwd(), f"attendance\\{fname}.csv"), "r") as f:
    scans = f.read().split("\n")[1:-1]
    for i in range(len(scans)):
        scans[i] = tuple(scans[i].split(",")[:2])

def processData(data):
    name, roll, _ = data.split("\n")

    if (roll, name) not in scans:
        scans.append((roll, name))
        return True

    return False

print(f">>> Attendance: {fname} <<<")
for i in scans:
    print(i[0], i[1], sep="\t")

while True:
    _, img = cam.read()
    qr_data, bbox, _ = detector.detectAndDecode(img)

    if qr_data != "":
        if processData(qr_data):
            print(scans[-1][0], scans[-1][1], sep="\t")

    cv2.imshow("QR Scanner", img)
    if cv2.waitKey(1) == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()

with open(os.path.join(os.getcwd(), f"attendance\\{fname}.csv"), "w") as f:
    f.write("Roll No.,Name,Email\n")
    scans.sort(key=lambda x: x[0])
    for i in scans:
        f.write(f"{i[0]},{i[1]},\n")

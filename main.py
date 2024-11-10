import cv2
import numpy as np
import re

from pyzbar.pyzbar import decode
from URL_predict import predict

# Open web-cam with height 640 width 480:
capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)


while True:
    # Get image from video & Get data from QR code:
    success, img = capture.read()

    for code in decode(img):

        # Decode the QR code data
        data = code.data.decode("utf-8")
        url_pattern = r"(https?://[^\s]+)"
        match = re.search(url_pattern, data)

        if match:
            url = match.group(0)
            prediction, _ = predict(str(url))
        else:
            print("No URL found in decoded data:", data)

        # Set text & color based on authorization:
        if prediction == 0:
            output = "Benign"
            color = (0, 255, 0)
        else:
            output = "Malware"
            color = (0, 0, 255)

        # Get polygon points as a reshaped np-array for line the QR code:
        points = np.array([code.polygon], np.int32)
        points = points.reshape((-1, 1, 2))
        cv2.polylines(
            img=img,
            pts=[points],
            isClosed=True,
            color=color,
            thickness=5,
        )

        # Set text on boundary box as rectangle for not making text rotate with image:
        points2 = code.rect
        cv2.putText(
            img=img,
            text=output,
            org=(points2[0], points2[1]),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.9,
            color=color,
            thickness=2,
        )

    # IMG show & delay 1 ms:
    cv2.imshow("Result", img)
    cv2.waitKey(1)  # delay 1ms

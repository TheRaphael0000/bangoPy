import cv2
import random

i00 = cv2.imread("00.png")
i01 = cv2.imread("01.png")
i10 = cv2.imread("10.png")
i11 = cv2.imread("11.png")

img = [i00, i01, i10, i11]
size = 600
img = list(map(lambda i: cv2.resize(i, (size, size)), img))
while True:
    cv2.imshow("", random.choice(img))
    cv2.waitKey(100)

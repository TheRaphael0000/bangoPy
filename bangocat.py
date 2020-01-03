import cv2
import random
import argparse


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", default=100, type=int, help="Delta T")
    parser.add_argument("-s", "--size", default=600, type=int, help="Size")

    args = parser.parse_args()

    img = [cv2.imread("00.png"), cv2.imread("01.png"),
           cv2.imread("10.png"), cv2.imread("11.png")]

    img = [cv2.resize(i, (args.size, args.size)) for i in img]

    while True:
        cv2.imshow("", random.choice(img))
        cv2.waitKey(args.time)


if __name__ == '__main__':
    run()

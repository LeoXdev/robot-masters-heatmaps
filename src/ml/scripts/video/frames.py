"""
frames.py

Purpose:
    Extract all frames of a video and save them to a temp directory on project root.
    Option to save the input video down to a 4:3 aspect ratio, the left and right sides will be trimmed although audio will be lost.
    Warning: An HD video may surpass the GBs mark even with less than a minute of duration.

Usage:
    py frames.py <<VIDEO_PATH>> <<OUTPUT_NAME>>
    py frames.py C:/Users/LeoXdev/Videos/enker.mp4 enker
"""

import sys
import os

import cv2

def crop(img):
    """
    Crops the resolution of a video frame down to 4:3, this operation is expected to be always safe by
    removing noisy letterboxing.
    """
    h, w = img.shape[:2]
    aspect_ratio = w / h

    target_ratio = 4 / 3
    tolerance = 0.02  # tolerance margin

    if abs(aspect_ratio - target_ratio) < tolerance:  # if video is already in 4:3
        return img
    elif aspect_ratio > target_ratio:
        new_w = int(h * target_ratio)
        start_x = (w - new_w) // 2
        cropped = img[:, start_x:start_x + new_w]
        return cropped

VIDEO_PATH = sys.argv[1]
OUTPUT_NAME = sys.argv[2]
os.makedirs(f"../../../../temp/{OUTPUT_NAME}", exist_ok=True)

read = cv2.VideoCapture(VIDEO_PATH)
code = cv2.VideoWriter_fourcc(*'mp4v')
write = None

i = 1
while True:
    res, frame = read.read()  # res becomes None when there's no more frames
    if not res:
        break

    cropped = crop(frame)

    if write is None:  # this if statement guarantees a single execution of the following block
        h, w = cropped.shape[:2]
        # uncomment the following two lines to save a cropped video too
        #write = cv2.VideoWriter(f"../../../../temp/{OUTPUT_NAME}.mp4", code, read.get(cv2.CAP_PROP_FPS), (w, h))
    #write.write(cropped)

    cv2.imwrite(f"../../../../temp/{OUTPUT_NAME}/{OUTPUT_NAME}_{i:04}.png", cropped)
    i += 1

read.release()
if write:
    write.release()

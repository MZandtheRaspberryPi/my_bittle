# D:\ziegl\python39\python.exe test_cv.py
# ffmpeg -framerate 10 -f image2 -i D:\ziegl\Downloads\vid\20240122-220206\frame_%d.png test.avi
import cv2
from datetime import datetime
import os
import numpy as np
import time
import urllib.request
import sys

SAVE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(SAVE_DIR, datetime.now().strftime("%Y%m%d-%H%M%S"))
print(SAVE_DIR)
os.mkdir(SAVE_DIR)

frame_times = []
stream = urllib.request.urlopen('http://192.168.1.174:8888/stream')
byte_arr = bytearray()
frame_counter = 0
image_name = "frame_{}.png"
while True:
    start_time = time.time()
    byte_arr += stream.read(1024)
    a = byte_arr.find(b'\xff\xd8')
    b = byte_arr.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes(byte_arr[a:b+2])
        byte_arr = byte_arr[b+2:]
        i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        frame_times.append(time.time() - start_time)
        if len(frame_times) > 30:
            frame_times.pop(0)
        # cv2.imshow('i', i)
        frame_counter += 1
        cv2.imwrite(os.path.join(SAVE_DIR, image_name.format(frame_counter)), i)
        if cv2.waitKey(1) == 27:
            exit(0)
        print(round(sum(frame_times) / 30, 2))

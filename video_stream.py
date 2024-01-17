# D:\ziegl\python39\python.exe test_cv.py
import cv2
import numpy as np
import time
import urllib.request
import sys

frame_times = []
stream = urllib.request.urlopen('http://192.168.x.x:8888/stream')
byte_arr = bytearray()
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
        cv2.imshow('i', i)
        if cv2.waitKey(1) == 27:
            exit(0)
        print(round(sum(frame_times) / 30, 2))

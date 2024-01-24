"""
This is an example that uses the MU3 Vision sensor to get video, and if it finds a face tells the bittle to walk forward. If not, to stand.
It is a proof of concept to use video stream from the MU3 with serial control of the bittle and a little computer vision.

Lots of stuff has to be setup like the pi and MU3 have to be connected to the same network, the MU3 has to have a known IP, and the PI has to have
some libraries installed.

I used a software serial port on the pi zero 2 w. The setup_wlan.py uses this software port to talk to the MU3 Vision sensor.
https://github.com/adrianomarto/soft_uart

Useful command to make a video
ffmpeg -framerate 10 -i ./20240122-233344/frame_%d.png -c:v libx264 -pix_fmt yuv420p out.mp4

"""

import cv2
from datetime import datetime
import os
import numpy as np
import time
import threading
import urllib.request
import sys

from my_bittle.keyboard_listener import KeyboardListener
from my_bittle.bittle_serial_controller import BittleSerialController, BittleCommand

port = "/dev/ttyS0"
my_bittle_controller = BittleSerialController(port=port)
my_bittle_controller.start()

SAVE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(SAVE_DIR, datetime.now().strftime("%Y%m%d-%H%M%S"))
print(SAVE_DIR)
os.mkdir(SAVE_DIR)

stream = urllib.request.urlopen('http://192.168.1.179:8888/stream')
frame_counter = 0
image_name = "frame_{}.png"
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

CUR_IMAGE = None
EXIT_FLAG = False
IMAGE_LOCK = threading.Lock()

my_keyboard_listener = KeyboardListener(key_timeout=0.01)

def read_image():
    global CUR_IMAGE
    byte_arr = bytearray()
    while not EXIT_FLAG:
        byte_arr += stream.read(1024)
        a = byte_arr.find(b'\xff\xd8')
        b = byte_arr.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes(byte_arr[a:b+2])
            byte_arr = byte_arr[b+2:]
            np_arr = np.frombuffer(jpg, dtype=np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            with IMAGE_LOCK:
            	if image is None or image.size != 129600:
                    continue
            	else:
                    CUR_IMAGE = image
        time.sleep(0.01)
thread_obj = threading.Thread(target=read_image)
thread_obj.start()

prev_cmd = BittleCommand.BALANCE
last_cmd_time = 0
start_time = time.time()
while not EXIT_FLAG:
    time.sleep(0.01)
    with IMAGE_LOCK:
        if CUR_IMAGE is not None:
            image = CUR_IMAGE
            CUR_IMAGE = None
        else:
            continue 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = face_classifier.detectMultiScale(
             gray_image, minNeighbors=5, minSize=(20, 20)
                )
    face_found = False
    for (x, y, w, h) in face:
        face_found = True
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)
    # cv2.imshow('image', image)
    if face_found:
        cur_cmd = BittleCommand.FORWARD
    else:
        cur_cmd = BittleCommand.BALANCE

    if prev_cmd != cur_cmd and time.time() - last_cmd_time > 1:
        my_bittle_controller.command_bittle(cur_cmd)
        prev_cmd = cur_cmd
        last_cmd_time = time.time()
    frame_counter += 1
    cv2.imwrite(os.path.join(SAVE_DIR, image_name.format(frame_counter)), image)
    key = my_keyboard_listener.get_key()
    if key == "q":
        EXIT_FLAG = True
        end_time = time.time()

my_bittle_controller.stop()
thread_obj.join()

print(f"fps: {frame_counter / (end_time - start_time)}")

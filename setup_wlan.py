import logging
import serial
import subprocess
import sys
import time

SSID_NAME = sys.argv[1]
SSID_PASS = sys.argv[2]

format = ' %(asctime)s - %(levelname)s- %(message)s'

logFormatter = logging.Formatter(format)
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

fileHandler = logging.FileHandler("/home/mikey/cam_setup_uart.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)


EXIT_FLAG = False

logging.info("starting soft uart")
p = subprocess.Popen(["sudo", "insmod", "/home/mikey/soft_uart/soft_uart.ko", "gpio_tx=5", "gpio_rx=6"])

time.sleep(2)


with serial.Serial() as ser:
    ser.baudrate = 9600
    ser.port = '/dev/ttySOFT0'
    ser.timeout = 5
    ser.open()

    def wait_for_ok():
        line = ser.readline()
        while "OK" not in line.decode():
            logging.info(f"waiting for ok, received {line.decode()}")
            time.sleep(0.01)
            line = ser.readline()

    WIFISET_CMD = f"AT+WIFISET={SSID_NAME},{SSID_PASS},STA "
    WIFICON_CMD = "AT+WIFICON=1 "
    IP_CHECK_CMD = "AT+WIFISIP "

    logging.info("setting wifi details")
    ser.write(WIFISET_CMD.encode())
    wait_for_ok()
    logging.info("connecting to wifi")
    ser.write(WIFICON_CMD.encode())
    wait_for_ok()
    logging.info("checking ip")
    ser.write(IP_CHECK_CMD.encode())

    output_lines = []
    line = ser.readline()
    while line:
        output_lines.append(line)
        line = ser.readline()
    logging.info(f"ip is {output_lines}")

p = subprocess.Popen(["sudo", "rmmod", "soft_uart.ko"])


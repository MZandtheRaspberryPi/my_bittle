import serial
import time
import threading

EXIT_FLAG = False



with serial.Serial() as ser:
    ser.baudrate = 9600
    ser.port = '/dev/ttySOFT0'
    ser.timeout = 5
    ser.open()

    def read_serial():
        while not EXIT_FLAG:
            line = ser.readline()
            if line:
                print(line)
            time.sleep(0.01)

 #   thread = threading.Thread(target=read_serial)

    cmd = input()
    while cmd != "exit":
        ser.write(cmd.encode())
        line = ser.readline()
        while line:
            print(line)
            line = ser.readline()
        cmd = input()
    #thread.start()
    #time.sleep(5)
    #EXIT_FLAG = True
    #thread.join()

import enum
import queue
import threading
import time

import serial

from my_bittle.keyboard_listener import KEYBOARD_FORWARD_KEY, KEYBOARD_BACKWARD_KEY, KEYBOARD_LEFT_KEY, \
    KEYBOARD_RIGHT_KEY, KEYBOARD_STAND_KEY, KEYBOARD_REST_KEY, KEYBOARD_SIT_KEY, KEYBOARD_STRETCH_KEY, KEYBOARD_BEEP_KEY

BITTLE_BAUD_RATE = 115200


class BittleCommand(enum):
    # Walking
    FORWARD = "wkF"
    FORWARD_LEFT = "wkL"
    FORWARD_RIGHT = "wkR"
    BACKWARD = "bk"
    BACKWARD_LEFT = "bkL"
    BACKWARD_RIGHT = "bkR"
    # posture
    BALANCE = "balance"
    REST = "rest"
    SIT = "sit"
    STRETCH = "str"
    # util
    BEEP = "b12 8 14 8 16 18 8 17 819 4"  # b then note duration note duration, ect
    QUERY = "?"


BITTLE_COMMAND_MAPPING = {KEYBOARD_FORWARD_KEY: BittleCommand.FORWARD,
                          KEYBOARD_BACKWARD_KEY: BittleCommand.BACKWARD,
                          KEYBOARD_LEFT_KEY: BittleCommand.FORWARD_LEFT,
                          KEYBOARD_RIGHT_KEY: BittleCommand.FORWARD_RIGHT,
                          KEYBOARD_STAND_KEY: BittleCommand.BALANCE,
                          KEYBOARD_REST_KEY: BittleCommand.REST,
                          KEYBOARD_SIT_KEY: BittleCommand.SIT,
                          KEYBOARD_STRETCH_KEY: BittleCommand.STRETCH,
                          KEYBOARD_BEEP_KEY: BittleCommand.BEEP}

SERIAL_CHECK_FOR_COMMANDS_DELAY = 0.02


class BittleSerialController:
    def __init__(self, port: str = "/dev/ttyS0", timeout: float = 1):
        self.port = port
        self.timeout = timeout
        self.__serial_comm = serial.Serial()
        self.__configure_serial_port()
        self.__exit_flag = False
        self.__serial_thread = threading.Thread(target=self.__run_serial_communicator)
        self.__command_q = queue.Queue()

    def __del__(self):
        self.sleep_bittle()
        time.sleep(SERIAL_CHECK_FOR_COMMANDS_DELAY * 10)
        self.__exit_flag = True
        self.__serial_thread.join()
        self.__serial_comm.close()

    def _send_cmd(self, cmd: str):
        self.__command_q.put(cmd.encode())

    def __run_serial_communicator(self):
        while not self.__exit_flag:
            if self.__command_q.qsize() > 0:
                cmd = self.__command_q.get(block=False, timeout=SERIAL_CHECK_FOR_COMMANDS_DELAY / 2)
                self.__serial_comm.write(cmd)
            time.sleep(SERIAL_CHECK_FOR_COMMANDS_DELAY)

    def __configure_serial_port(self):
        self.__serial_comm.baudrate = BITTLE_BAUD_RATE
        self.__serial_comm.port = self.port
        self.__serial_comm.timeout = self.timeout

    def __start_communication(self):
        self.__serial_comm.open()
        self.serial_thread.start()
        self._send_cmd(BittleCommand.QUERY.value)

    def start(self):
        self.__start_communication()

    def command_bittle(self, cmd: BittleCommand):
        self._send_cmd(cmd.value)

    def command_bittle_stand(self):
        self._send_cmd(BittleCommand.BALANCE.value)

    def sleep_bittle(self):
        self._send_cmd(BittleCommand.REST.value)

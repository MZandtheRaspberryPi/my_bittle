import enum
import queue
import threading
import time

import serial

BITTLE_BAUD_RATE = 115200

READY_STR = "Ready"


class BittleCommand(enum.Enum):
    # Walking
    FORWARD = "kwkF"
    FORWARD_LEFT = "kwkL"
    FORWARD_RIGHT = "kwkR"
    BACKWARD = "kbk"
    BACKWARD_LEFT = "kbkL"
    BACKWARD_RIGHT = "kbkR"
    # posture
    BALANCE = "kbalance"
    REST = "krest"
    SIT = "ksit"
    STRETCH = "kstr"
    # util
    BEEP = "b12 8 14 8 16 18 8 17 819 4"  # b then note duration note duration, ect
    QUERY = "?"

    @staticmethod
    def print_all():
        for val in BittleCommand:
            print(val)


SERIAL_CHECK_FOR_COMMANDS_DELAY = 0.02


def log_msg_from_bittle(line: bytes):
    try:
        line = line.decode()
        print(f"from robot: {line}")
    except UnicodeDecodeError as err:
        print(f"from robot: {line}")
        line = ""
    return line


class BittleSerialController:
    def __init__(self, port: str = "/dev/ttyS0", timeout: float = 1, check_for_ready: bool = False):
        self.port = port
        self.timeout = timeout
        self.check_for_ready = check_for_ready
        self.__serial_comm = serial.Serial()
        self.__configure_serial_port()
        self.__exit_flag = False
        self.__command_q = queue.Queue()
        self.__serial_thread = threading.Thread(target=self.__run_serial_communicator)

    def _send_cmd(self, cmd: str):
        self.__command_q.put(cmd.encode())

    def __run_serial_communicator(self):

        line = ""
        while self.check_for_ready and not self.__exit_flag and READY_STR not in line:
            line = self.__serial_comm.readline()
            line = log_msg_from_bittle(line)
            time.sleep(SERIAL_CHECK_FOR_COMMANDS_DELAY)

        while not self.__exit_flag:
            if self.__command_q.qsize() > 0:
                cmd = self.__command_q.get(block=False, timeout=SERIAL_CHECK_FOR_COMMANDS_DELAY / 2)
                self.__serial_comm.write(cmd)
            line = self.__serial_comm.readline()
            if line:
                line = log_msg_from_bittle(line)
            time.sleep(SERIAL_CHECK_FOR_COMMANDS_DELAY)

    def __configure_serial_port(self):
        self.__serial_comm.baudrate = BITTLE_BAUD_RATE
        self.__serial_comm.port = self.port
        self.__serial_comm.timeout = self.timeout

    def __start_communication(self):
        self.__serial_comm.open()
        self.__serial_thread.start()
        self._send_cmd(BittleCommand.QUERY.value)

    def start(self):
        self.__start_communication()

    def stop(self):
        self.sleep_bittle()
        time.sleep(SERIAL_CHECK_FOR_COMMANDS_DELAY * 10)
        self.__exit_flag = True
        self.__serial_thread.join()
        self.__serial_comm.close()

    def command_bittle(self, cmd: BittleCommand):
        self._send_cmd(cmd.value)

    def command_bittle_stand(self):
        self._send_cmd(BittleCommand.BALANCE.value)

    def sleep_bittle(self):
        self._send_cmd(BittleCommand.REST.value)


if __name__ == "__main__":
    BittleCommand.print_all()

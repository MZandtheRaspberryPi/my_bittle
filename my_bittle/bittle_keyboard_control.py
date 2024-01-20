import time
import signal
import sys

from my_bittle.bittle_serial_controller import BittleCommand, BittleSerialController, BITTLE_COMMAND_MAPPING, \
    SERIAL_CHECK_FOR_COMMANDS_DELAY
from my_bittle.keyboard_listener import KeyboardListener, MSG


def main():
    if len(sys.argv) < 2:
        port = "/dev/ttyS0"
    else:
        port = sys.agv[1]

    exit_flag = False
    my_keyboard_listener = KeyboardListener()
    my_bittle_controller = BittleSerialController(port=port)

    def signal_handler(sig, frame):
        global exit_flag
        exit_flag = True

    signal.signal(signal.SIGINT, signal_handler)
    default_command = BittleCommand.BALANCE
    my_bittle_controller.start()

    while not exit_flag:
        print(MSG)
        key = my_keyboard_listener.get_key()
        if key == "":
            command = default_command
        else:
            command = BITTLE_COMMAND_MAPPING.get(key, default_command)
        my_bittle_controller.command_bittle(command)
        time.sleep(SERIAL_CHECK_FOR_COMMANDS_DELAY)

    my_bittle_controller.stop()


if __name__ == "__main__":
    main()

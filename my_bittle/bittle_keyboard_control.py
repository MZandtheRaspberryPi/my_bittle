import time
import sys

from my_bittle.bittle_serial_controller import BittleCommand, BittleSerialController, \
    SERIAL_CHECK_FOR_COMMANDS_DELAY
from my_bittle.keyboard_listener import KeyboardListener, MSG, BITTLE_COMMAND_MAPPING, KEYBOARD_QUIT_KEY

KEY_DEBOUNCE_SECONDS = 0.5


def main():
    if len(sys.argv) < 2:
        port = "COM10"
    else:
        port = sys.argv[1]

    exit_flag = False
    my_keyboard_listener = KeyboardListener()
    my_bittle_controller = BittleSerialController(port=port)

    default_command = BittleCommand.BALANCE
    my_bittle_controller.start()

    prior_command = default_command

    while not exit_flag:
        print(MSG)
        key = my_keyboard_listener.get_key()
        if key == "":
            command = default_command
        elif key == KEYBOARD_QUIT_KEY:
            exit_flag = True
            command = prior_command
        else:
            command = BITTLE_COMMAND_MAPPING.get(key, default_command)
        if command != prior_command:
            my_bittle_controller.command_bittle(command)
            prior_command = command
            time.sleep(KEY_DEBOUNCE_SECONDS)
        time.sleep(0.01)

    my_bittle_controller.stop()


if __name__ == "__main__":
    main()

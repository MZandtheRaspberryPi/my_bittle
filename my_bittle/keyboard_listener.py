from select import select
import sys

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

from my_bittle.bittle_serial_controller import BittleCommand

KEYBOARD_FORWARD_KEY = "w"
KEYBOARD_BACKWARD_KEY = "d"
KEYBOARD_LEFT_KEY = "a"
KEYBOARD_RIGHT_KEY = "d"
KEYBOARD_STAND_KEY = "e"
KEYBOARD_REST_KEY = "r"
KEYBOARD_SIT_KEY = "f"
KEYBOARD_STRETCH_KEY = "c"
KEYBOARD_BEEP_KEY = "b"
KEYBOARD_QUIT_KEY = "q"

MSG = f"""
Reading commands from the keyboard and sending to the Bittle robot.
---------------------------
Moving around:
    {KEYBOARD_FORWARD_KEY}
  {KEYBOARD_LEFT_KEY}   {KEYBOARD_RIGHT_KEY}
    {KEYBOARD_BACKWARD_KEY}

{KEYBOARD_STAND_KEY}: stand
{KEYBOARD_REST_KEY}: rest
{KEYBOARD_SIT_KEY}: sit
{KEYBOARD_STRETCH_KEY}: stretch
{KEYBOARD_BEEP_KEY}: beep melody

{KEYBOARD_QUIT_KEY} to quit
"""

BITTLE_COMMAND_MAPPING = {KEYBOARD_FORWARD_KEY: BittleCommand.FORWARD,
                          KEYBOARD_BACKWARD_KEY: BittleCommand.BACKWARD,
                          KEYBOARD_LEFT_KEY: BittleCommand.FORWARD_LEFT,
                          KEYBOARD_RIGHT_KEY: BittleCommand.FORWARD_RIGHT,
                          KEYBOARD_STAND_KEY: BittleCommand.BALANCE,
                          KEYBOARD_REST_KEY: BittleCommand.REST,
                          KEYBOARD_SIT_KEY: BittleCommand.SIT,
                          KEYBOARD_STRETCH_KEY: BittleCommand.STRETCH,
                          KEYBOARD_BEEP_KEY: BittleCommand.BEEP}


class KeyboardListener:
    def __init__(self, key_timeout: float = 0.5):
        self.key_timeout = key_timeout
        self.settings = KeyboardListener.__save_terminal_settings()

    def __del__(self):
        KeyboardListener.__restore_terminal_settings(self.settings)

    def __get_key_windows(self):
        # note this blocks
        return msvcrt.getwch()

    def __get_key_linux(self):
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        rlist, _, _ = select([sys.stdin], [], [], self.key_timeout)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def get_key(self):
        if sys.platform == 'win32':
            return self.__get_key_windows()
        else:
            return self.__get_key_linux()

    @staticmethod
    def __save_terminal_settings():
        if sys.platform == 'win32':
            return None
        return termios.tcgetattr(sys.stdin)

    @staticmethod
    def __restore_terminal_settings(old_settings):
        if sys.platform == 'win32':
            return
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

import gc
import time
import unittest
from unittest.mock import patch, MagicMock

from my_bittle.bittle_serial_controller import BittleCommand, BittleSerialController
from my_bittle.keyboard_listener import BITTLE_COMMAND_MAPPING


class TestBittleSerialController(unittest.TestCase):

    def test_BITTLE_COMMAND_MAPPING(self):
        for key, val in BITTLE_COMMAND_MAPPING.items():
            self.assertIn(val, BittleCommand)

    @patch("my_bittle.bittle_serial_controller.serial.Serial")
    def test_bittle_start_stop(self, MockSerial):
        """
        Check that before exiting we tell the bittle to rest
        :param MockSerial:
        :return:
        """
        my_mock_serial = MagicMock()
        MockSerial.return_value = my_mock_serial
        my_mock_serial.readline.return_value = b"Ready"
        my_controller = BittleSerialController()
        my_controller.start()
        my_controller.command_bittle(BittleCommand.FORWARD)
        my_controller.stop()
        self.assertEqual(my_mock_serial.write.call_args_list[-1].args, (b'krest',))

import time

from my_bittle.bittle_serial_controller import BittleSerialController, BittleCommand

port = "COM11"
my_bittle_controller = BittleSerialController(port=port)
my_bittle_controller.start()
start_time = time.time()

my_bittle_controller.command_bittle(BittleCommand.FORWARD)

while time.time() - start_time < 30:
    time.sleep(0.01)

my_bittle_controller.stop()

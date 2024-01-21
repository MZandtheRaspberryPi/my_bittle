# my_bittle

![example workflow](https://github.com/MZandtheRaspberryPi/my_bittle/actions/workflows/pipeline.yaml/badge.svg)

This is a package that enables control via keyboard or api of
the [Bittle robot from Petoi](https://www.petoi.com/pages/bittle-open-source-bionic-robot-dog). This project is not
affiliated with petoi or bittle officially. Try this project with your bittle on a test stand first where bittle's feat
can't touch the ground, as it may result in commands that break your bittle.

The intent of this package is to make it easier to use a raspberry pi to control the bittle and build custom behavior
using a raspberry pi. That said if you have a serial port open to the bittle on windows, it'll work too.

## Installation

```
pip install my-bittle
```

## Keyboard Control Usage

Connect to the bittle via serial (bluetooth, cable, ect).

On windows, something like this:

```
bittle-keyboard-control COM11
```

On linux, something like this:

```
bittle-keyboard-control /dev/ttyS0
```

## API Usage

```python
import time

from my_bittle.bittle_serial_controller import BittleSerialController, BittleCommand

port = "/dev/ttyS0"
my_bittle_controller = BittleSerialController(port=port)

my_bittle_controller.start()
my_bittle_controller.command_bittle(BittleCommand.FORWARD)
time.sleep(2)
my_bittle_controller.stop()
```

To see all available commands:

```python
from my_bittle.bittle_serial_controller import BittleCommand

BittleCommand.print_all()
```

To send a custom command:

```python
import time

from my_bittle.bittle_serial_controller import BittleSerialController

port = "/dev/ttyS0"
my_bittle_controller = BittleSerialController(port=port)

my_bittle_controller.start()
my_bittle_controller._send_cmd("b1 2 4 6")
time.sleep(2)
my_bittle_controller.stop()
```

## Troubleshooting

Blank.
# my_bittle

This is a package that enables control via keyboard of
the [Bittle robot from Petoi](https://www.petoi.com/pages/bittle-open-source-bionic-robot-dog). This project is not
affiliated with petoi or bittle officially. Try this project with your bittle on a test stand first where bittle's feat
can't touch the ground, as it may result in commands that break your bittle.

The intent of this package is to make it easier to use a raspberry pi to control the bittle and build custom behavior
using a raspberry pi.

## Installation

```
pip install my-bittle
```

## Usage

```
bittle-keyboard-control
```

or to specify the port:

```
bittle-keyboard-control /dev/ttyS0
```

## Troubleshooting

Blank.
# my_bittle

## Bittle Serial References

https://docs.petoi.com/apis/serial-protocol#arduino-ide-as-an-interface

## doing a release

Run tests. If you get module not found then add the my_bittle location to path.

```commandline
python -m unittest discover tests
```

Update the version in pyproject.toml to match git tag you'll build
Build a git tag.
If adding more dependencies update pyproject.toml.

## OS

Use ubuntu 22.04 or raspberry pi os.

Increase swap memory:

```
sudo swapon --show # see if any swap currently
free -h # can also see here
df -h # check available space
sudo fallocate -l 1G /swapfile # make swapfile
sudo chmod 600 /swapfile # only root can read
sudo mkswap /swapfile
sudo swapon /swapfile # enable it
sudo cp /etc/fstab /etc/fstab.bak
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
sudo nano /etc/sysctl.conf # put in "vm.swappiness=10" # only use swap if needed
```

Note: If you installed Ubuntu OS on Raspberry Pi, please config it as follows:
add enable_uart=1 to /boot/firmware/config.txt
remove console=serial0,115200 from /boot/firmware/cmdline.txt on Ubuntu and similar to/boot/cmdline.txt on Raspberry Pi
OS
disable the serial console: sudo systemctl stop serial-getty@ttyS0.service && sudo systemctl disable
serial-getty@ttyS0.service
make sure you have pyserial installed if you're using the python serial library, not python-serial from apt.
create the following udev file (I created /etc/udev/rules.d/50-tty.rules):
KERNEL=="ttyS0", SYMLINK+="serial0" GROUP="tty" MODE="0660"
KERNEL=="ttyAMA0", SYMLINK+="serial1" GROUP="tty" MODE="0660"
reload your udev rules: sudo udevadm control --reload-rules && sudo udevadm trigger
change the group of the new serial devices:
sudo chgrp -h tty /dev/serial0
sudo chgrp -h tty /dev/serial1
The devices are now under the tty group. Need to add the user to the tty group and dialout group:
sudo adduser $USER tty
sudo adduser $USER dialout
update the permissions for group read on the devices:
sudo chmod g+r /dev/ttyS0
sudo chmod g+r /dev/ttyAMA0
reboot
Or just create a script that will do this automatically

## Configuring the MU3 Camera

Plug it into the raspberry pi to 3.3v power, ground, and then rx to pin 5 and tx to pin 6 on the GPIO.

If you want to expiriment with AT commands, you can use the chat_serial.py script. Run this, then type in `AT+HELP ` and
then hit enter. Note the space at the end. Also note that there can be no spaces in the wifi SSID name.

I installed soft UART as per https://github.com/adrianomarto/soft_uart. This let me run a software uart port on gpio
pins to talk to the camera (slowly).

```
sudo insmod soft_uart.ko gpio_tx=5 gpio_rx=6 # to add
sudo rmmod soft_uart.ko # to remove
```

It creates a software serial port at `/dev/ttySOFT'. The script below uses this to setup the wlan for your wifi on the
camera. You could add this to the crontab to run at reboot. Note you may have to change the log directory.

```
sudo python3 setup_wlan.py my_wifi_name my_password
```

set PYTHONPATH=%PYTHONPATH;D:\ziegl\git\my_bittle

venv\Scripts\python.exe my_bittle\bittle_keyboard_control.py
# my_bittle

## OS
Use ubuntu 22.04.

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
remove console=serial0,115200 from /boot/firmware/cmdline.txt on Ubuntu and similar to/boot/cmdline.txt on Raspberry Pi OS
disable the serial console: sudo systemctl stop serial-getty@ttyS0.service && sudo systemctl disable serial-getty@ttyS0.service
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

tips for AT commands
make sure to do space or new line stuff after
no spaces in wifi ssid name


for soft uart
https://github.com/adrianomarto/soft_uart

sudo insmod soft_uart.ko

## Portable Raspberry Pi Zero Device (PRPZD)
# Equipment
[Waveshare 1.44inch LCD HAT SPI](https://amzn.eu/d/cSOeuAg)<br />
[Raspberry Pi Zero 2w](https://amzn.eu/d/5fjt3Nu) <br />
[Raspberry Pi Zero Pin Headers (20 pins)](https://amzn.eu/d/ev8hWmw)  <br />
# WARNING!!
**This was only only tested on Kali Linux for Raspberry Pi Zero 2W. But system can only be 32 bits for the fbcp driver to work**, other systems might not work.
# Tools
In the tools folder, there is a folder named stats, inside of it there is a file named **stat.py**. This file will run a status report webpage that can be accessed on port 5000 on your raspberry pi zero IP with the user **admin** and password **admin**. YOu can see the RAM and CPU usage as well as be able to reboot the raspberry pi zero 2W.
# Installation.
```bash
sudo raspi-config
# go to Interfacing Options -> SPI -> enable
# and then Boot Options -> Desktop/CLI and choose Desktop Autologin, type root and enter.
cd /home/kali 
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
tar zxvf bcm2835-1.71.tar.gz 
cd bcm2835-1.71/
sudo ./configure && sudo make && sudo make check && sudo make install
cd /home/kali
```
```bash
wget https://github.com/joan2937/lg/archive/master.zip
unzip master.zip
cd lg-master
```
This shit will get some problems, so before **make install**, do nano Makefile and search for python3. Replace that line with: 
```bash
@if which python3; then cd PY_RGPIO && python3 -m pip install --user -e . $(PYINSTALLARGS) || echo "*** install of Python3 rgpio.py failed ***"; fi
```
And for python2 remove the line
```bash
sudo make install # I need to fix this fr
```
```bash
cd /home/kali
sudo apt-get update -y
sudo apt-get install python3-pip python3-pil python3-numpy cmake p7zip-full -y
sudo pip3 install spidev
git clone https://github.com/LoadingQ/PRPZD.git
git clone https://github.com/juj/fbcp-ili9341.git
cd fbcp-ili9341
mkdir build
cd build
cmake -DWAVESHARE_ST7735S_HAT=ON -DST7735S=ON -DSPI_BUS_CLOCK_DIVISOR=6 ..
make -j
sudo cp ./fbcp-ili9341 /usr/local/bin/fbcp
sudo nano /etc/systemd/system/fbcp.service
```
**Then add:**
```
[Unit]
Description=FBCP driver

[Service]
ExecStart=/usr/local/bin/fbcp

[Install]
WantedBy=default.target
```
Then do:
```bash
sudo systemctl enable fbcp
```
```bash
sudo nano /boot/config.txt
```
**Scroll down and add this:**
```
hdmi_force_hotplug=1
hdmi_cvt=340 340 60 1 0 0 0
hdmi_group=2
hdmi_mode=87
display_rotate=0
```
```bash
sudo apt-get -y install python3-xlib
sudo pip3 install PyMouse
sudo pip3 install unix
sudo pip3 install PyUserInput
sudo su
cd /root/.config
mkdir autostart
cd autostart
sudo nano local.desktop
```
**Then write this (remove the sudo if runnin on local user and not root):**
```
[Desktop Entry]
Type=Application
Exec=sudo python3 /home/kali/PRPZD/mouse.py
```
**Last requriments and reboot**
```bash
sudo python3 -m pip install pynput
sudo pip3 install RPi.GPIO
exit
sudo reboot
```
For customization just use google for the love of god

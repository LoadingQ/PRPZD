#!/bin/bash

echo '[+] Making directories...'
sudo mkdir /PRPZD
sudo mkdir /PRPZD/configs
echo '[+] Copying config files...'
sudo cp keys.json /PRPZD/configs/keys.json
echo '[+] Setup completed'

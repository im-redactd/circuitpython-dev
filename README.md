# circuitpython-dev
notes to build dev environment

resources: https://learn.adafruit.com/building-circuitpython/linux

VM build OS is Ubuntu 20.04.

### update os and install packages

sudo add-apt-repository ppa:pybricks/ppa\
sudo apt-get update\
sudo apt install build-essential git gettext uncrustify mtools\
sudo apt install python3-pip


cd ~/\
mkdir dev\
cd dev

### install gcc compiler for arm

wget https://developer.arm.com/-/media/Files/downloads/gnu-a/10.3-2021.07/binrel/gcc-arm-10.3-2021.07-x86_64-arm-none-eabi.tar.xz \
tar xvf gcc-arm-10.3-2021.07-x86_64-arm-none-eabi.tar.xz\
export PATH=/home/$USER/dev/gcc-arm-10.3-2021.07-x86_64-arm-none-eabi/arm-none-eabi/bin:$PATH

cd ~/dev

### build fs tools

wget https://github.com/dosfstools/dosfstools/releases/download/v4.2/dosfstools-4.2.tar.gz

tar xvf dosfstools-4.2.tar.gz \
cd dosfstools-4.2 \
./configure\
make\
cd ~/dev

### clone circuitpython and install python libraries

git clone https://github.com/adafruit/circuitpython.git \
cd circuitpython\
make fetch-submoules 

pip3 install --upgrade -r requirements-dev.txt \
pip3 install --upgrade -r requirements-doc.txt

### complile mpy-cross

make -C mpy-cross

### set active branch

git checkout 7.3.0

### test compile rp2040 board

cd ~/dev/circuitpython/ports/raspberrypi \
make -j8 BOARD=raspberry_pi_pico


## objective

build i2cperipheral library for circuitpython

here's the micropython implementation: https://github.com/adamgreen/i2cperipheral

here's adafruits circuitpython implementation for another board as a reference: https://github.com/adafruit/circuitpython/blob/main/ports/atmel-samd/common-hal/i2cperipheral/I2CPeripheral.c

here's the rp2040 i2c class for references to the apis that might be needed for i2cperipheral: https://github.com/adafruit/circuitpython/blob/main/ports/raspberrypi/common-hal/busio/I2C.c

here's a guide on how to extend circuitpython (old. not sure if still relevant): https://learn.adafruit.com/extending-circuitpython/overview





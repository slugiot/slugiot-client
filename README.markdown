## Readme

SlugIOT is a remote device management system for small embedded linux systems.

This is the version of code that runs on the client.

Clone this repository via: 

    git clone --recursive https://github.com/slugiot/slugiot-client.git

The --recursive option is important, or else you will be missing PyDAL, the database abstraction layer. 

## Running the code

    cd ~/slugiot-client
    sudo slugiot_install.sh
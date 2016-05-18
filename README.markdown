## Readme

SlugIOT is a remote device management system for small embedded linux systems.

This is the version of code that runs on the client.

Clone this repository via: 

    git clone --recursive https://github.com/slugiot/slugiot-client.git

The --recursive option is important, or else you will be missing PyDAL, the database abstraction layer. 

## Running the code

Enters startup script into the server initialization:

    sudo ./slugiot-client/slugiot_install.sh
    
The startup script safely starts the webserver and queues the sync tasks in scheduler.

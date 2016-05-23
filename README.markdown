## Readme

SlugIOT is a remote device management system for small embedded linux systems.

This is the version of code that runs on the client.  Install in Documents,
when logged in as user pi.
    
    cd /home/pi/Documents
    git clone --recursive https://github.com/slugiot/slugiot-client.git

The --recursive option is important, or else you will be missing PyDAL, the database abstraction layer. 

## Running the code on client

The script slugiot_install.sh enters the startup script into the server initialization.

    # cd into top level of project and execute
    cd /home/pi/Documents/slugiot-client/
    sudo chmod +x slugiot_install.sh 
    . slugiot_install.sh
    
The startup script safely starts the webserver and queues the sync tasks in scheduler.

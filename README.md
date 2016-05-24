## Readme

SlugIOT is a remote device management system for small embedded linux systems.

This is the version of code that runs on the client.  
Install it in the home directory, when logged in as user pi.
    
    cd /home/pi
    git clone --recursive https://github.com/slugiot/slugiot-client.git

The --recursive option is important, or else you will be missing PyDAL, the database abstraction layer. 

## Running the code on client

The script slugiot_install.sh enters the startup script into the server initialization.

    # cd into top level of project and execute
    cd /home/pi/slugiot-client/
    sudo chmod +x slugiot_install.sh 
    . slugiot_install.sh
    
The startup script safely starts the webserver and queues the sync tasks in scheduler.
The script currently works for Raspberry Pi; you need to change the location of the code
if you install the code on other architectures. 

## Running the code in test mode

To run the code in test mode, start it as follows:

    python web2py.py -e -a <password> -p 8600 -K client -i 0.0.0.0 -X
    
where 8600 is the port at which the process should be running (feel free to change it).
Once it is up and running, inject a job in the scheduler via:

    curl http://localhost:8600/startup/_startup.html

    

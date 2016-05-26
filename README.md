## Readme

SlugIOT is a remote device management system for small embedded linux systems.

This is the version of code that runs on the client.  
Install it in the home directory, when logged in as user pi.
    
    cd /home/pi
    git clone --recursive https://github.com/slugiot/slugiot-client.git

The --recursive option is important, or else you will be missing PyDAL, the database abstraction layer. 

## Running the code on client

The installation scripts can be found in the installation directory.

The script slugiot_install.sh enters the startup script into the server initialization.

    cd installation
    sh ./slugiot_install.sh
    
The startup script safely starts the webserver and queues the sync tasks in scheduler.
The script currently works for Raspberry Pi; you need to change the location of the code
if you install the code on other architectures. 

The startup scripts also create a ram disk, mounted at /ramfs. 
You need this ram disk in order to run SlugIOT client: a short-term database is created
in /ramfs/storage.sqlite. 

## Running the code in test mode

To run the code in test mode, there are two ways. 

### Running in testing mode

In this mode, SlugIOT does not rely on a RAM file system (you might be running this on
your laptop after all).  Run it as follows:

    SLUGIOT_TESTING=y
    python web2py.py -e -a <password> -p 8600 -K client -i 0.0.0.0 -X
    
where 8600 is the port at which the process should be running (feel free to change it).
Once it is up and running, inject a job in the scheduler via:

    curl http://localhost:8600/startup/_startup.html

### Running in production mode

If you have been testing on the same machine, remember to do

    SLUGIOT_TESTING=n
    
Then, start SlugIOT via:

    sudo /etc/init.d/slugiot_startup start

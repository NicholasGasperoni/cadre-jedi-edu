# jedi-edu

This software is licensed under the terms of the Apache Licence Version 2.0 which can be obtained at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0).

## Instructions to get started with the jedi-edu tutorials:

### Install docker on your laptop
Scroll down to the bottom of the page: https://docs.docker.com/desktop/
Open docker and wait for it to start.

Go to settings in the Docker window (gear icon at top), then scroll down to "Virtual Machine Options".
Under 'Choose Virtual Machine Manager (VMM)', select "QEMU (Legacy)", then click "Apply and Restart" at the bottom right.

### Clone the jedi-edu repository
Open a terminal window and clone the jedi-edu repository.
```
git clone https://github.com/NicholasGasperoni/cadre-jedi-edu.git
```

Enter the cadre-jedi-edu repository:
```
cd cadre-jedi-edu
```

### Build and enter the container for the first time
```
cd container
docker build -t educontainer --build-arg=Dockerfile .
docker run -it --rm -p 9999:8888 -v <your>/<path>/<to>/jedi-edu/notebooks/:/home/nonroot/shared educontainer
```
The next time you want to enter the container, you will only need to enter the `docker run` command.

Note you may get teh following warnings from the docker build step. These can be safely ignored.
```
 2 warnings found (use docker --debug to expand):
 - InvalidBaseImagePlatform: Base image jcsda/docker-clang-mpich-dev:edu was pulled with platform "linux/amd64", expected "linux/arm64" for current build (line 1)
 - LegacyKeyValueFormat: "ENV key=value" should be used instead of legacy "ENV key value" format (line 15)
```

If it worked, you will see a message resembling:
```
check start

Welcome to JEDI Tutorial!  To connect, open your browser to:
	 localhost:<port>

NOTE: Replace '<port>' with the port you specified in your 'docker run' command. For example, if you used the option:
	        -p 9999:8888

Then you should open the browser and go to:
	 localhost:9999
```

Open your favorite browser and go to `localhost:9999`
All that follows is done **in the container ON THE WEBPAGE you just opened**.

### Open the qg 3dvar tutorial
On the left of the web page there is a tree of files. Click on the little folder icon if you aren't on it already (open the one called `shared/`), and double click on `qg3Dvar_tutorial.ipynb`.

Note that in this file, you will be able to run commands by clicking on the cell that contains it and click the `play` button.
![welcome](img/run_command.png)

### Follow the tutorial instructions!

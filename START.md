# CADRE JEDI-edu Installation Guide

This software is licensed under the terms of the Apache Licence Version 2.0 which can be obtained at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0).

## Instructions to get started with the jedi-edu tutorials:

### Install docker on your personal laptop
- Navigate to the following URL in any web browser: https://docs.docker.com/desktop/
- Scroll down to the bottom of the page, under "Next Steps", the first box on the top left contains links to download Docker Desktop for Mac, Windows, or Linux devices. Follow the installation and download instructions
- After installation completes, restart your computer
```
Note for Mac Users:  Docker is fully supported only for MacOS 14 (Sonoma) or newer. It is recommmended users update to latest OS version if their OS is older, otherwise you may encounter issues with the Docker installation/running
```

### Open docker.
- Double-click on Docker to start it, and wait for the dashboard to pop up.
- (Mac Users Only) Go to settings in the Docker window (gear icon at top), then scroll down to "Virtual Machine Options". Make sure under 'Choose Virtual Machine Manager (VMM)' that "Docker VMM" is selected. If it is not, select it and then click "Apply and Restart" at the bottom right.
```
Note on some older Mac/Docker versions, there may be a "QEMU (Legacy)" option as Virtual Machine. This option may be selected in case the tutorial does not work upon first attempts below.
``` 

### Download (clone) the repository containing cadre-jedi-edu tutorials and jedi programs

- For Windows Users:
-- Download and install git following the instructions at the following link:  https://git-scm.com/install/windows
-- Open a Powershell terminal window.
   (Optional) Some users may find VS code to be more helpful/convenient, which is a program that can be downloaded for free online.
-- Double-check that git is installed correctly by running the command ```git --version```
-- Run the git command below
``` 
git clone https://github.com/NicholasGasperoni/cadre-jedi-edu.git
# Enter the cadre-jedi-edu repository:
cd cadre-jedi-edu
# List the contents of the repository
ls .
```

- For Mac Users: 
-- Open the terminal window from the Terminal app
-- Run the git command below (note git should automatically download & install if it is not already installed on your macbook)
```
git clone https://github.com/NicholasGasperoni/cadre-jedi-edu.git
# Enter the cadre-jedi-edu repository:
cd cadre-jedi-edu
# List the contents of the repository
ls .
```

- If the repository cloned correctly, the following contents will be listed from the `ls` command:
```
README.md	START.md	container	img		notebooks
```

### Build and enter the container for the first time
Navigate to the container directory and build the container with the following commands. 
*Note* 'educontainer' is the name of the container we are building.
```
cd container
docker build -t educontainer --build-arg=Dockerfile .
```

Once the container is built successfully, we can now attempt to run it from within the container directory!
Run the docker ommand below, making sure to replace "<your>/<path>/<to>" with the actual path on your local computer (run the `pwd` command if you are not sure what directory to input!)
```
# Make sure the folloring is invoked within the `cadre-jedi-edu/container` directory
# Run the following command for MAC users
docker run -it --rm -p 9999:8888 -v <your>/<path>/<to>/cadre-jedi-edu/notebooks/:/home/nonroot/shared educontainer
# -or- the following command for WINDOWS users
docker run -it --rm -p 9999:8888 --mount type=bind,source="$(Resolve-Path ..\notebooks)",target=/home/nonroot/shared --entrypoint /bin/sh educontainer -c "tr -d '\r' < /srv/start > /tmp/start && chmod +x /tmp/start && exec /tmp/start"
```


Each time you want to run the container, you will enter the docker run command above. The build step only needs to be done once.

*Note* you may get the following warnings from the docker build step. These can be safely ignored.
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

### View the container and tutorials!
- Open your favorite web browser and enter `localhost:9999` as URL. This may take up to ~20 seconds to load correctly, so be patient. 
All that follows in the tutorial is done **in the container ON THE WEBPAGE you just opened**.
- Open the first tutorial
On the left of the web page there is a tree of files. Click on the little folder icon if you aren't on it already (open the one called `shared/`), and double click on `0.qg_tutorial_start.ipynb`.

Note that in this file, you will be able to run commands by clicking on the cell that contains it and click the `play` button.
![welcome](img/run_command.png)

### Follow the tutorial instructions!

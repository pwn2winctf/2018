## Instructions to install and use the Platform via Docker:

**1** - Download the Dockerfile [here](https://static.pwn2win.party/Dockerfile) and put it alone in a folder.

**2** - Edit Dockerfile and put your GitHub infos in the variables.

**3** - Install docker:
```bash
$ sudo apt-get install docker.io
```

**4** - Enter the Dockerfile directory, and build the image:
```bash
$ sudo docker build -t pwn2win .
```

**5** - Create a container from image (we are assuming here that your user's ssh key is the key that is in GitHub):
```bash
$ sudo docker run --name pwn2win -it -v $HOME/.ssh/id_rsa:/root/.ssh/id_rsa pwn2win
```

 - **5.1** - If you want to detach, type:

	```bash
	CTRL + P + Q
	```

 - **5.2** - To go back to the box, after detached, type:

	```bash
	$ sudo docker exec -it pwn2win /bin/bash
	```

**Note**: this box is ephemeral, if you type "exit" or reboot the Host PC, you will need to delete the current container ($ sudo docker rm pwn2win) and run command "docker run [...]" again, to be able to login next time only with *team-secrets.json* file. So, don't forget, **save** *team-secrets.json*!

**6** - Back to [README](README.en.md) and follow from the fourth step onwards.
 
 

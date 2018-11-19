## Instructions to install and use the Platform via Docker:

**1** - Download the Dockerfile [here](https://static.pwn2win.party/Dockerfile) and put it alone in a folder.

**2** - Install docker:
```bash
$ sudo apt-get install docker.io
```

**3** - Enter the Dockerfile directory, and build the *base* image:
```bash
$ sudo docker build -t pwn2win .
```

**4** - Create a container from image (we are assuming here that your user's ssh key is the key that is in GitHub):
```bash
$ sudo docker run --name pwn2win -it -v $HOME/.ssh/id_rsa:/root/.ssh/id_rsa pwn2win
```

**5** - Replace your GitHub infos in the variables, and install the platform dependencies:
```bash
$ git config --global user.name "YOUR_USER_HERE" && git config --global user.email "YOUR_EMAIL_HERE" && git clone git@github.com:pwn2winctf/2018.git && cd $HOME_DIR/2018 && curl https://bootstrap.pypa.io/get-pip.py | sudo -H python && sudo -H python -m pip install -r pip-requirements.txt
```
 - **5.1** - Now, if you type "exit" or reboot your Host PC, you need to go back to the container:
 ```bash
    $ sudo docker restart pwn2win
    $ sudo docker exec -it pwn2win /bin/bash
 ```

**6** - Back to [README](README.en.md) and follow from the fourth step onwards.
 
 

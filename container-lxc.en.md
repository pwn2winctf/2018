## Instructions to install and use the container

**1**. Unless you already use LXD, install and setup it. [This document](https://linuxcontainers.org/lxd/getting-started-cli/#getting-the-packages) contains instructions for various distros. If you are using Ubuntu, just run:

```bash
$ sudo apt update
$ sudo apt install lxd
$ sudo lxd init   # Accept the default options
```  

**2**. [Download our image](https://static.pwn2win.party/pwn2win2018.tar.gz), import it to LXD, and create an instance of the container:

```bash
$ lxc image import pwn2win2018.tar.gz --alias=pwn2win2018
$ lxc launch pwn2win2018 pwn2win
```

**3**. The container already has this repository cloned for you. Just make sure your copy is up to date:

```bash
$ lxc exec pwn2win -- git pull
```

**4**. Either generate a new SSH key pair inside the container and [add it](https://github.com/settings/ssh/new) to the GitHub account you will be using:

```bash
$ lxc exec pwn2win -- ssh-keygen -t ed25519
$ lxc exec pwn2win -- cat .ssh/id_ed25519
```

**or** copy your existing key pair to the container:

```bash
$ lxc file push ~/.ssh/id_* pwn2win/root/.ssh/
```

**5**. Just follow the instructions in the [README](README.en.md) prefixing every command with `lxc exec pwn2win --`. For example, to login as the leader of your team, type `lxc exec pwn2win -- ./ctf init`. You can always spawn a shell by typing `lxc exec pwn2win sh`.

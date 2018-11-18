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
$ lxc init pwn2win2018 pwn2win
$ lxc start pwn2win
```

**3**. Make sure your container has the latest copy of this repository:

```bash
$ lxc exec pwn2win git pull
```

**4**. Just follow the instructions on the [README](README.md) prefixing every command with `lxc exec pwn2win`. For example, to list challenges, type `lxc exec pwn2win ./ctf challs`.

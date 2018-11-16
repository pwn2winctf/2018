## Instructions to install and use the container

1. First install and configure LXD:

```bash
add-apt-repository ppa:ubuntu-lxc/lxd-stable
apt update
apt install lxd
lxd init
```

2. Download the LXC container [image](https://cloud.ufscar.br:8080/v1/AUTH_c93b694078064b4f81afd2266a502511/static.pwn2win.party/pwn2win2018.tar.gz) and import it to LXD:

```bash
lxc image import pwn2win2018.tar.gz --alias=pwn2win2018
```

3. Create an instance of the container and log into it:

```bash
lxc init pwn2win2018 pwn2win
lxc list
ssh player@[ip_of_the_pwn2win_container]
```

  * The password is `pwn2win2018`, we recommend changing it after you login

4. Follow the instructions on the **README** file inside the container for setting up the __git__ environment.

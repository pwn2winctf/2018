## Instruções para instalação e uso do container

**1**. Primeiro instale e configure o LXD:

```bash
$ sudo add-apt-repository ppa:ubuntu-lxc/lxc-stable
$ sudo apt update
$ sudo apt install lxd
$ sudo lxd init   # Use as opções padrões
```  

**2**. Baixe a [imagem](https://static.pwn2win.party/pwn2win2018.tar.gz) do container LXC e importe no LXD:

```bash
$ lxc image import pwn2win2018.tar.gz --alias=pwn2win2018
```

**3**. Crie uma instância do container e logue nela:

```bash
$ lxc init pwn2win2018 pwn2win
$ lxc start pwn2win
$ lxc list
$ ssh player@[ip_do_container_pwn2win]
```

  * A senha é `pwn2win2018`, nós recomendamos que ela seja trocada.

**4**. Siga as instruções do **README** dentro do container para configurar o ambiente _git_.

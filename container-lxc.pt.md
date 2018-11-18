## Instruções para instalação e uso do container

**1**. Primeiro, instale e configure o LXD. [Este documento](https://linuxcontainers.org/lxd/getting-started-cli/#getting-the-packages) contém informaçes para várias distros. Se você está usando ubuntu, siga os passos abaixo:

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

**3**. Crie uma instância a partir da imagem:

```bash
$ lxc init pwn2win2018 pwn2win
$ lxc start pwn2win
```
**4**. Certifique-se que está com a última versão do repositório:

```bash
$ lxc exec pwn2win git pull
```

**5**. Siga as instruções do [README](https://github.com/pwn2winctf/2018/blob/master/README.pt.md) prefixando os comandos com *lxc exec pwn2win*. Por exemplo, para ver os *challenges*, digite:
```bash
$ lxc exec pwn2win ./ctf challs
```

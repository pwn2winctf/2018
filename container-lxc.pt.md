## Instruções para instalação e uso do container

1. Primeiro instale e configure o LXD:

```bash
add-apt-repository ppa:ubuntu-lxc/lxc-stable
apt update
apt install lxd
lxd init
```

2. Baixe a [imagem](https://cloud.ufscar.br:8080/v1/AUTH_c93b694078064b4f81afd2266a502511/static.pwn2win.party/pwn2win2018.tar.gz) do container LXC e importe no LXD:

```bash
lxc image import pwn2win2018.tar.gz --alias=pwn2win2018
```

3. Crie uma instância do container e logue nela:

```bash
lxc init pwn2win2018 pwn2win
lxc list
lxc start pwn2win
ssh player@[ip_do_container_pwn2win]
```

  * A senha é `pwn2win2018`, nós recomendamos que ela seja trocada.

4. Siga as instruções do **README** dentro do container para configurar o ambiente _git_.

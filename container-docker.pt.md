## Instruções para instalar e usar a plataforma com Docker:

**1** - Baixe o Dockerfile [aqui](https://static.pwn2win.party/Dockerfile) e coloque em uma pasta onde fique apenas ele.

**2** - Instale o docker:
```bash
$ sudo apt-get install docker.io
```

**3** - Entre no diretório onde está o Dockerfile, e crie a imagem base:
```bash
$ sudo docker build -t pwn2win .
```

**4** - Crie o container a partir da imagem (nós estamos assumindo aqui que a key do seu usuário é a que está adicionada no GitHub):
```bash
$ sudo docker run --name pwn2win -it -v $HOME/.ssh/id_rsa:/root/.ssh/id_rsa pwn2win
```

**5** - Substitua suas informações do GitHub nas variáveis, e instale as dependências da plataforma dentro do container:
```bash
root@c62ed90932e6:/ctf/2018# git config --global user.name "YOUR_USER_HERE" && git config --global user.email "YOUR_EMAIL_HERE" && git clone git@github.com:pwn2winctf/2018.git && cd $HOME_DIR/2018 && curl https://bootstrap.pypa.io/get-pip.py | sudo -H python && sudo -H python -m pip install -r pip-requirements.txt
```

 - **5.1** - Agora, se você digitar "exit" ou reiniciar sua máquina física, terá que retornar para o container:
   ```bash
   $ sudo docker restart pwn2win
   $ sudo docker exec -it pwn2win /bin/bash
   ```

**6** - Volte para o [README](README.pt.md) e continue a partir do passo 4.
 
 

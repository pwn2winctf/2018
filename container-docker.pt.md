## Instruções para instalar e usar a plataforma com Docker:

**1** - Baixe o Dockerfile [here](https://static.pwn2win.party/Dockerfile).

**2** - Edite-o e coloque suas informações do GitHub nas variáveis.

**3** - Instale o docker:
```bash
$ sudo apt-get install docker.io
```

**4** - Entre no diretório onde está o Dockerfile, e crie a imagem:
```bash
$ docker build -t pwn2win .
```

**5** - Crie o container a partir da imagem (nós estamos assumindo aqui que a key do seu usuário é a que está adicionada no GitHub):
```bash
$ docker run --name pwn2win -it -v $HOME/.ssh/id_rsa:/root/.ssh/id_rsa pwn2win
```

 - **5.1** - Caso você queira detachar, use:

	```bash
	CTRL + P + Q
	```

 - **5.2** - Pra voltar para a box, após detachado:

	```bash
	$ docker exec -it pwn2win /bin/bash
	```

**6** - Volte para o [README](README.pt.md) e continue a partir do passo 4.
 
 

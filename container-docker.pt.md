## Instruções para instalar e usar a plataforma com Docker:

**1** - Baixe o Dockerfile [aqui](https://static.pwn2win.party/Dockerfile) e coloque em uma pasta onde fique apenas ele.

**2** - Edite-o e coloque suas informações do GitHub nas variáveis.

**3** - Instale o docker:
```bash
$ sudo apt-get install docker.io
```

**4** - Entre no diretório onde está o Dockerfile, e crie a imagem:
```bash
$ sudo docker build -t pwn2win .
```

**5** - Crie o container a partir da imagem (nós estamos assumindo aqui que a key do seu usuário é a que está adicionada no GitHub):
```bash
$ sudo docker run --name pwn2win -it -v $HOME/.ssh/id_rsa:/root/.ssh/id_rsa pwn2win
```

 - **5.1** - Caso você queira detachar, use:

	```bash
	CTRL + P + Q
	```

 - **5.2** - Pra voltar para a box, após detachado:

	```bash
	$ sudo docker exec -it pwn2win /bin/bash
	```
**Nota Importante**: essa máquina é temporária, se você der um "exit" ou reiniciar o PC Host, terá que apagar o container atual ($ sudo docker rm pwn2win) e rodar o comando "docker run [...]" novamente, para logar na próxima vez usando apenas o *team-secrets.json*. Dito isso, **não esqueça** de salvar o *team-secrets.json*!

**6** - Volte para o [README](README.pt.md) e continue a partir do passo 4.
 
 

# Pwn2Win CTF 2018


## Registro
1. Todos os membros do time devem ter uma conta no GitHub e [configurar uma chave SSH nas suas configurações de conta](https://github.com/settings/keys).

2. Todos os membros do time devem ter um cliente git [corretamente configurado](https://git-scm.com/book/pt-br/v2/Começando-Configuração-Inicial-do-Git). Se você nunca usou git antes, execute:
   ```bash
   git config --global user.name "Fulano de Tal"
   git config --global user.email fulanodetal@exemplo.com.br
   ```

3. Todos os membros do time devem clonar o repositório e instalar as dependências:
   ```bash
   git clone git@github.com:pwn2winctf/2018.git
   cd 2018
   sudo apt-get install libsodium18 # Ou qualquer versão >= libsodium18
   curl https://bootstrap.pypa.io/get-pip.py | sudo -H python
   sudo -H python -m pip install -r pip-requirements.txt
   ```
   **Note**: Se você estiver usando Ubuntu 14.04, adicione [ppa:elt/libsodium](https://launchpad.net/~elt/+archive/ubuntu/libsodium) no seu sistema para poder instalar o `libsodium18`.

4. Se as dependencias estiverem corretamente instaladas, você deve conseguir ver o menu de ajuda executando:
   ```bash
   ./ctf -h
   ```

5. **O líder do time** deve executar o seguinte comando e seguir as instruções para registrar o time:
   ```bash
   ./ctf init
   ```

6. **Os demais membros** devem se logar com o github sem criar um novo time:
   ```bash
   ./ctf login
   ```

7. Após isso, **o líder** deve compartilhar o arquivo `team-secrets.json` com os demais mebros. **Os demais mebros** devem colocar o arquivo `team-secrets.json` na pasta `2018` clonada.

## Challenges

Os challenges estão disponíveis em https://pwn2win.github.io.

Se você Se você preferir, pode consultar localmente subindo um servidor usando `./ctf serve`, ou listar os challenges na Interface de Linha de Comando:
```bash
./ctf challs
```

## Submissão de flags

Para submeter uma flag:
```bash
./ctf submit --chall chall-id 'CTF-BR{flag123}'
```

Você pode omitir o `--chall chall-id` do comando, mas vai demorar mais para submeter. Nesse caso, será tentada a flag para cada um dos challenges liberados até então.

## VPN

Para pegar as credenciais da VPN, quando seu time desbloqueá-la, após resolver 5 challenges (veja a página de "regras" pra entender melhor):
```bash
./ctf news --pull
```

## Placar

Atualmente o placar está disponível apenas via linha de comando:
```bash
./ctf score --names --pull
```

Porém planejamos disponibilizá-lo via web num release futuro.

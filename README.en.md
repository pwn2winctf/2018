# Pwn2Win CTF 2018

About our NIZK (Non-Interactive Zero-Knowledge) Platform: [https://arxiv.org/pdf/1708.05844.pdf](https://arxiv.org/pdf/1708.05844.pdf)

## Registration
1. All team members must have a GitHub account and [configure a SSH key in their account settings](https://github.com/settings/keys).

   **Important Note**: If you are unable to follow the installation instructions below, ~~or is simply too lazy to do all the steps~~, we made a [LXD container preloaded with this platform](container-lxc.en.md). If you prefer Docker, we made a [Dockerfile](container-docker.en.md) too. If you want to install directly in your machine (instead of containers), just ignore this note.

2. All team members must clone the repository and install the dependencies:
   ```bash
   git clone git@github.com:pwn2winctf/2018.git
   cd 2018
   sudo apt-get install libsodium23 # Or any version >= libsodium18
   curl https://bootstrap.pypa.io/get-pip.py | sudo -H python
   sudo -H python -m pip install -r pip-requirements.txt
   ```
   
3. All team members must have the git client [correctly set up](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup). If you have never used git before, run:
   ```bash
   git config --global user.name "John Doe"
   git config --global user.email johndoe@example.com
   ```

4. If dependencies are installed correctly (or if you used one of our preloaded containers), you should now see the help menu when calling:
   ```bash
   ./ctf -h
   ```

5. The **leader of the team** must execute the following command and follow the instructions to register the team:
   ```bash
   ./ctf init
   ```

6. The **other members of the team** must login to GitHub without registering a new team, by running:
   ```bash
   ./ctf login
   ```

7. After that, **the leader** must share the `team-secrets.json` with the members of the team. The **other members of the team** must place the `team-secrets.json` file shared by the leader in their `2018` directory.

## Challenges

Challenges are available on https://pwn2.win/2018.

If you prefer to browse them locally, you may also run a local webserver by typing `./ctf serve`, or list challenges through the command line interface:
```bash
./ctf challs
```

## Flag submission

To submit a flag:
```bash
./ctf submit --chall chall-id 'CTF-BR{flag123}'
```

You may omit `--chall chall-id` from the command, however it will be slower to run this way. In this case, we will look for the flag in every challenge released until now.

## VPN

To get the VPN credentials after your team has unlocked it (by solving at least 6 challenges - see the [rules](https://pwn2win.party/rules) page for more details):
```bash
./ctf news --pull
```

## Scoreboard

You can see the scoreboard in the game link (https://pwn2.win/2018), locally (if you ran the local webserver) or through the command line interface:
```bash
./ctf score --names --pull
```

## Support

You may reach us through #pwn2win at irc.freenode.net.

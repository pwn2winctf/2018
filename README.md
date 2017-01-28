# Platform Test Edition

Welcome to the Pwn2Win CTF **Platform Test Edition**.

## Registration

1. All team members must have a GitHub account and [configure a SSH key in their account settings](https://github.com/settings/keys).

   **Note**: If you prefer team members to stay anonymous, you can create a single GitHub account for the entire team and share its credentials.
   
2. All team members must have the git client [correctly set up](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup). If you have never used git before, run:
   ```bash
   git config --global user.name "John Doe"
   git config --global user.email johndoe@example.com
   ```
   
2. All team members must clone the repository and install the dependencies:
   ```bash
   git clone git@github.com:pwn2winctf/PTE.git
   cd PTE
   sudo -H pip install -r pip-requirements.txt
   ```

3. Test if you can see the help menu:
  ```bash
  ./ctf -h
  ```
  **Note**: If you have problems with pysodium, you should install libsodium18 (e.g, https://packages.debian.org/sid/libsodium18)

4. The leader of the team must execute the following command and follow the instructions to register the team:
  ```bash
  ./ctf init
  ```

5. After that, the leader shares `team-secrets.json` with the members of the team and they are ready to go :)

## Challenges

Challenges are available on https://pwn2winctf.github.io.

If you prefer to browse them locally, you may also run a local webserver by typing `make`, or list challenges through the command line interface:
```bash
./ctf challs
```

## Flag submission

To submit a flag:
```bash
./ctf submit --chall chall-id 'CTF-BR{flag123}'
```

You may omit `--chall chall-id` from the command, however it will be slower to run this way. In this case, we will look for the flag in every challenge released until now.

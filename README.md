# Platform Test Edition

Welcome to the Pwn2Win CTF platform test edition.

## Registration

1. All team members must have a github account and a configured ssh key
2. All team members must clone the repository and install the dependencies:
```bash
git clone git@github.com:pwn2winctf/PTE.git
cd PTE
pip install -r pip-requirements.txt
```
3. Test if you can see the help menu:
```bash
./ctf -h
```
- Note: If you have problems with pysodium, you should install libsodium18 (e.g, https://packages.debian.org/sid/libsodium18)
4. The leader of the team must execute the following command and follow the instructions to register the team:
```bash
./ctf init
```
5. After that, the leader shares team-secrets.json with the members team and they are ready to go :)

## Challenges

The challenge instructions are located in the *challenges* directory.

## Flag submission

To submit a flag:
```bash
./ctf submit 'CTF-BR{flag123}'
```

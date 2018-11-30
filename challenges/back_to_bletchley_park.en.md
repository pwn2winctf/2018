
We have gone quantum. A collaborator of ours built this **quantum circuit** to compute the factorization of a Bavs RSA key and took note of the results. They are now stored in her server ([https://qc.pwn2.win](https://qc.pwn2.win)) inside the `/a/N` path, where `a` is the group generator and `N` is the modulus. Unfortunately we could not get in touch with her lately, so we need your help understanding what she did. Once you figure out how the circuit works and discover what are the values of `a` and `N`, we can see the results from her calculations and use them to decrypt the message.

[Link](https://cloud.ufscar.br:8080/v1/AUTH_c93b694078064b4f81afd2266a502511/static.pwn2win.party/back-to-bletchley-park_b349f5d19905bcdf8f4abd01f321f2e05adf0979dcf3b435465deaabbc913dec.tar.gz)

[Mirror](https://static.pwn2win.party/back-to-bletchley-park_b349f5d19905bcdf8f4abd01f321f2e05adf0979dcf3b435465deaabbc913dec.tar.tgz)

**Note**: We know that the message was originally encrypted with the following commands:

```
openssl rsautl -encrypt -oaep -pubin -inkey public.pem -in aes256.key -out aes256.key.enc
openssl aes-256-cbc -base64 -in secret_message.txt -out secret_message.enc -k $(cat aes256.key)
```

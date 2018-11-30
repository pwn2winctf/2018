
Agora temos computadores quânticos. Uma colaboradora nossa construiu este circuito quântico para calcular a fatoração de uma chave RSA dos Bavs
e anotou os resultados. Eles estão no servidor dela ([https://qc.pwn2.win](https://qc.pwn2.win)) no caminho `/a/N`, onde `a` é o gerador do grupo e `N` é o módulo. Infelizmente não conseguimos falar com ela nos últimos dias, então precisamos de sua ajuda para entender o que ela fez. Quando você descobrir como o circuito funciona e os valores de `a` e `N`, poderemos encontrar os seus resultados e usá-los para decifrar a mensagem.

[Link](https://cloud.ufscar.br:8080/v1/AUTH_c93b694078064b4f81afd2266a502511/static.pwn2win.party/back-to-bletchley-park_b349f5d19905bcdf8f4abd01f321f2e05adf0979dcf3b435465deaabbc913dec.tar.gz)

[Mirror](https://static.pwn2win.party/back-to-bletchley-park_b349f5d19905bcdf8f4abd01f321f2e05adf0979dcf3b435465deaabbc913dec.tar.tgz)

**Nota**: Nós sabemos que a mensagem foi originalmente cifrada com os seguintes comandos:

```
openssl rsautl -encrypt -oaep -pubin -inkey public.pem -in aes256.key -out aes256.key.enc
openssl aes-256-cbc -base64 -in secret_message.txt -out secret_message.enc -k $(cat aes256.key)
```

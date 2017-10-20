Para a infiltração, Case e Molly lidaram com a eletrônica dos chips, que eram extremamente difíceis de analisar. Para isso, pediram sua ajuda para dada a descrição do chip, calcular a resistência equivalente entre determinados pontos. A entrada é composta, a princípio, por uma descrição do circuito, onde, em cada linha, os dois primeiros inteiros indicam os dois extremos (números identificadores dos pontos de solda) de uma ligação e o terceiro indica a resistência dessa ligação. Para as linhas seguintes, você deve responder cada uma com uma linha contendo apenas um número, indicando a resistência equivalente entre os dois pontos de solda descritos na linha com três casas decimais de precisão.

**Exemplo:**

input:

1 2 1

2 3 1

1 2

2 3

1 3

output:

1.000

1.000

2.000

**Server:** openssl s_client -connect programming.pwn2win.party:9001

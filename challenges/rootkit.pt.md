Suspeitamos que um de nossos servidores foi ownado pela Inteligência da Bloodsuckers. Tudo indica para o fato de terem instalado um **binary rootkit** em nosso sistema, visando conseguir nossas credenciais para tentarem usar em outros servidores. Faça uma análise forense no dump do sistema, e ao identificar o comprometimento, faça um *reversing* para identificar a senha que dá acesso ao dump (*sniffer*) das senhas. Após isso, entendendo o funcionamento do rk, obtenha a última senha legítima utilizada pelo root na máquina, pois achamos que ela foi mudada pelo pessoal da Inteligência por uma default deles, e também pode nos ser útil em outros dos seus sistemas, como a de dump! (o feitiço virou contra o feiticeiro!). 

Submeta no formato **CTF-BR{SenhaUsadaParaDump,UltimaSenhaRootLegitima}**.

**Nota:** não temos as credenciais, isso faz parte do desafio.

[Link](https://cloud.ufscar.br:8080/v1/AUTH_c93b694078064b4f81afd2266a502511/static.pwn2win.party/rootkit_3e4df5d6a3926cbc81ebf014a82098ad0964653aaedf581cd1bbc06eb3756642.tar.gz)

[Mirror](https://static.pwn2win.party/rootkit_3e4df5d6a3926cbc81ebf014a82098ad0964653aaedf581cd1bbc06eb3756642.tar.gz)

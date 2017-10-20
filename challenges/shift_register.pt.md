A ButcherCorp desenvolveu um processo extremamente confiável para encapsulamento de CIs tolerantes a radiação. A única desvantagem desse processo é que ele requer que o ASIC seja fabricado usando uma tecnologia específica de 0.35μm, considerada ultrapassada pelos padrões atuais. Coletamos informações que indicam que a biblioteca padrão de células usada por eles é baseada na osu035.

Um de nossos colaboradores conseguiu exfiltrar um arquivo GDSII que a ButcherCorp enviou para uma fábrica de chips. Parece que se trata do CI responsável por validar o código de lançamento no mais recente motor de foguete colocado por eles no mercado.

O CI amostra o pino `in` na borda de subida do sinal de `clock`. Se a sequência de bits correta for apresentada ao IC, ele coloca o pino `unlocked` em nível lógico alto. Descubra essa sequência. Ela forma uma string em ASCII, que você deve submeter como flag.

[Link](https://cloud.ufscar.br:8080/v1/AUTH_c93b694078064b4f81afd2266a502511/static.pwn2win.party/shiftreg_e7f285dccca5788b157d72e7fde31a92ed765c64ec86d56164426b7c1cde1625.tar.gz)

[Mirror](https://static.pwn2win.party/shiftreg_e7f285dccca5788b157d72e7fde31a92ed765c64ec86d56164426b7c1cde1625.tar.gz)

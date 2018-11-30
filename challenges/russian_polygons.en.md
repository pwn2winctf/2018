
Tired of watching Russian roulette games between prisoners, the bavs decided to create a new game in which the prisoners' survival depends on luck. And it was even more sadistic: there was a chance that all prisioners would die...

Anyway... Let's go to the rules. The prisoner is fixed at center (0,0) of a circular radius R room with concrete walls. He cannot move. Around the room (outside of it) there are n shooters fixed at indicated positions. After everybody is positioned, N big extremely thin but heavy regular polygon plates of a super dense material, able to flatten even the walls, fall in the room region. Once a shooter has sight of the prisioner, there is a not null chance (indicated in each test) to miss their only shot. If two shooters are aligned, the one closer to the prisoner will shoot and leave.

Yes... the bavs think all this expense is worth it.

In the first line of the input there are 3 integers: the radius R, the number of shooters n and the number of polygons N. In each of the following n lines there are 3 real numbers indicating the cartesian coordinates of each shooter and the probability of, once the prisoner is seen, missing their shot. In each of the following N lines there are 4 real numbers and an integer, indicating the coordinates of a regular polygon's center, the coordinates of one of the polygon's vertexes and the number of edges.

The output must have a single real number with 5 decimal places indicating the probability of survival of the prisoner.

**Example:**

input:

10 2 2

11 0 0.1

0 11 0.1

10 0 11 0 3

0 10 0 10.5 3

output:

0.10000

**Server:** openssl s_client -connect programming.pwn2.win:9001

**Connection template:**

[Link](https://cloud.ufscar.br:8080/v1/AUTH_c93b694078064b4f81afd2266a502511/static.pwn2win.party/russian-polygons-template_3319bcb3c22f00875e8c17426dfa80ab579cfa14ff7fad546860718ce04965b4.tar.gz.tar.gz)

[Mirror](https://static.pwn2win.party/russian-polygons-template_3319bcb3c22f00875e8c17426dfa80ab579cfa14ff7fad546860718ce04965b4.tar.gz.tar.gz)


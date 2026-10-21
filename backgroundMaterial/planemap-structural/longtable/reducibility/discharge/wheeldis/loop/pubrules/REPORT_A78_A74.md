# Published rules on binder rows (pubrules.py; diagnostic map, not a claim)

Source rows: `binders_A78_A74.txt`. Sets: rsst, nl26. Units: 10(6-d) scale (1 unit = 0.1 in ours).

## Summary

| row | tag | rsst: u net at privates >= 6 | rsst: always-out at privates >= 6 | nl26: u net at privates >= 6 | nl26: always-out at privates >= 6 |
|---|---|---|---|---|---|
| 7 7766556 6567568 | A78 r58b face OPEN | -1..0 | w0(7) 2 [drule8, drule9]; w1(7) 2 [drule9m, drule21m] | -1..0 | w0(7) 2 [rule008_1, rule009_1]; w1(7) 2 [rule009_2, rule014_2] |
| 7 8665556 7675865 | A78 r58c face OPEN | 0 | w0(8) 4 [drule8, drule9, drule9m, drule20] | 0 | w0(8) 4 [rule008_1, rule009_1, rule009_2, rule014_2] |
| 7 8665566 6765765 | A78 r58g face OPEN | 0..1 | w0(8) 2 [drule9, drule9m] | -2..-1 | w0(8) 4 [rule009_1, rule009_2, rule014_1, rule014_2] |
| 7 7766556 6576576 | A78 face exhausted (also A74) | -1 | w0(7) 2 [drule8, drule9]; w1(7) 2 [drule9m, drule21m] | -1 | w0(7) 2 [rule008_1, rule009_1]; w1(7) 2 [rule009_2, rule014_2] |
| 7 7665566 6675676 | A78 face exhausted (also A74) | 0 | w0(7) 2 [drule9, drule9m] | -2 | w0(7) 4 [rule009_1, rule009_2, rule014_1, rule014_2] |
| 7 7766556 6567566 | A74 face (top A74 binder) | -1..0 | w0(7) 2 [drule8, drule9]; w1(7) 2 [drule9m, drule21m] | -1..0 | w0(7) 2 [rule008_1, rule009_1]; w1(7) 2 [rule009_2, rule014_2] |
| 7 7766556 6566576 | A74 face | -1..1 | w0(7) 2 [drule8, drule9]; w1(7) 2 [drule9m, drule21m] | -1..1 | w0(7) 2 [rule008_1, rule009_1]; w1(7) 2 [rule009_2, rule014_2] |
| 7 7665566 6775676 | A74 face (r57d) | 0 | w0(7) 2 [drule9, drule9m] | -2 | w0(7) 4 [rule009_1, rule009_2, rule014_1, rule014_2] |
| 7 8677656 5566555 | A78 r58a dead (control) | -1 | w0(8) 1 [drule8]; w3(7) 1 [drule8m] | -1 | w0(8) 1 [rule008_1]; w3(7) 1 [rule008_2] |
| 7 7656766 6666555 | A74 r57a dead (control) | -4 | w0(7) 1 [drule8m]; w4(7) 1 [drule8] | -4..-2 | w0(7) 1 [rule008_2]; w4(7) 1 [rule008_1] |

## 7 7766556 6567568   (cert weight -0.05701)

Privates: p0.1 p0.2 p1.1 p1.2 p2.1 p3.1 p6.1 (7; 78125 exact fillings over 5..9)
Base charge of u: 10(6-7) = -10.

### RSST (Gonthier drules; m = mirror)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w1 (7) | 1 | drule8 | always | 1.000 / 1.000 |
| in | w1 (7) | 1 | drule9 | p1.2=5 | 0.200 / 0.200 |
| in | w2 (6) | 1 | drule4' | p3.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | drule2' | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | drule4'm | p2.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | drule5m | p2.1<=6 | 0.400 / 0.400 |
| in | w4 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule3 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule2m | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule3m | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule2'm | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule4m | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule6m | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule8 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule9 | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | drule21m | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | drule9m | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -1..3, possible -1..3; certain > 0 in 29.6%, possibly > 0 in 29.6%
- u net charge, all privates >= 6: charge certain -1..0, possible -1..0; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 2 [drule8, drule9]; w1(7) 2 [drule9m, drule21m]; IN from 5s 8, from 6s 4, from 7s 1
- (certain, possible) histogram: -1:30000, 0:25000, 1:16875, 2:5625, 3:625

### NL26 (Inoue et al. 2026 rule files)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w1 (7) | 1 | rule008_1 | always | 1.000 / 1.000 |
| in | w1 (7) | 1 | rule009_1 | p1.2=5 | 0.200 / 0.200 |
| in | w1 (7) | 1 | rule019_1 | p1.1=5 & p1.2=6 | 0.040 / 0.040 |
| in | w2 (6) | 1 | rule004_1 | p3.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | rule004_2 | p2.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | rule005_1 | p2.1<=6 | 0.400 / 0.400 |
| in | w4 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w5 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule004_1 | p6.1=5 | 0.200 / 0.200 |
| in | w6 (6) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | rule004_2 | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | rule006_2 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule008_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule009_1 | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | rule009_2 | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | rule014_2 | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -1..4, possible -1..4; certain > 0 in 37.3%, possibly > 0 in 37.3%
- u net charge, all privates >= 6: charge certain -1..0, possible -1..0; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 2 [rule008_1, rule009_1]; w1(7) 2 [rule009_2, rule014_2]; IN from 5s 8, from 6s 4, from 7s 1
- (certain, possible) histogram: -1:22800, 0:26200, 1:18825, 2:8325, 3:1825, 4:150

## 7 8665556 7675865   (cert weight -0.05701)

Privates: p0.1 p0.2 p0.3 p1.1 p2.1 p6.1 (6; 15625 exact fillings over 5..9)
Base charge of u: 10(6-7) = -10.

### RSST (Gonthier drules; m = mirror)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w1 (6) | 1 | drule4' | p2.1=5 | 0.200 / 0.200 |
| in | w2 (6) | 1 | drule2' | always | 1.000 / 1.000 |
| in | w2 (6) | 1 | drule4'm | p1.1=5 | 0.200 / 0.200 |
| in | w3 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule3 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule2m | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule3m | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule2m | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule2'm | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | drule20 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | drule8 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | drule9 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | drule9m | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain 0..2, possible 0..2; certain > 0 in 36.0%, possibly > 0 in 36.0%
- u net charge, all privates >= 6: charge certain 0..0, possible 0..0; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(8) 4 [drule8, drule9, drule9m, drule20]; IN from 5s 12, from 6s 2
- (certain, possible) histogram: 0:10000, 1:5000, 2:625

### NL26 (Inoue et al. 2026 rule files)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (8) | 1 | rule042_2 | p0.1=5 & p0.2=5 & p0.3=5 | 0.008 / 0.008 |
| in | w1 (6) | 1 | rule004_1 | p2.1=5 | 0.200 / 0.200 |
| in | w2 (6) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w2 (6) | 1 | rule004_2 | p1.1=5 | 0.200 / 0.200 |
| in | w3 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w5 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule004_1 | p6.1=5 | 0.200 / 0.200 |
| in | w6 (6) | 1 | rule002_1 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | rule008_1 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | rule009_1 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | rule009_2 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | rule014_2 | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain 0..4, possible 0..4; certain > 0 in 49.2%, possibly > 0 in 49.2%
- u net charge, all privates >= 6: charge certain 0..0, possible 0..0; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(8) 4 [rule008_1, rule009_1, rule009_2, rule014_2]; IN from 5s 12, from 6s 2
- (certain, possible) histogram: 0:7936, 1:6016, 2:1536, 3:136, 4:1

## 7 8665566 6765765   (cert weight -0.02850)

Privates: p0.1 p0.2 p0.3 p1.1 p2.1 p5.1 p6.1 (7; 78125 exact fillings over 5..9)
Base charge of u: 10(6-7) = -10.

### RSST (Gonthier drules; m = mirror)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w2 (6) | 1 | drule2' | always | 1.000 / 1.000 |
| in | w2 (6) | 1 | drule4 | always | 1.000 / 1.000 |
| in | w2 (6) | 1 | drule6 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule3 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule2m | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule3m | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | drule2'm | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | drule4' | p6.1=5 | 0.200 / 0.200 |
| in | w5 (6) | 1 | drule5 | p6.1<=6 | 0.400 / 0.400 |
| in | w6 (6) | 1 | drule4'm | p5.1=5 | 0.200 / 0.200 |
| out | w0 (8) | 1 | drule9 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | drule9m | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain 0..3, possible 0..3; certain > 0 in 52.0%, possibly > 0 in 52.0%
- u net charge, all privates >= 6: charge certain 0..1, possible 0..1; certain > 0 in 25.0%, possibly > 0 in 25.0%
- at privates >= 6, rules that fire in every filling: OUT w0(8) 2 [drule9, drule9m]; IN from 5s 8, from 6s 4
- (certain, possible) histogram: 0:37500, 1:21875, 2:15625, 3:3125

### NL26 (Inoue et al. 2026 rule files)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (8) | 1 | rule042_2 | p0.1=5 & p0.2=5 & p0.3=5 | 0.008 / 0.008 |
| in | w2 (6) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w2 (6) | 1 | rule004_1 | always | 1.000 / 1.000 |
| in | w2 (6) | 1 | rule006_1 | always | 1.000 / 1.000 |
| in | w3 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | rule004_2 | p2.1=5 | 0.200 / 0.200 |
| in | w4 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | rule004_1 | p6.1=5 | 0.200 / 0.200 |
| in | w5 (6) | 1 | rule005_2 | p6.1<=6 | 0.400 / 0.400 |
| in | w6 (6) | 1 | rule004_2 | p5.1=5 | 0.200 / 0.200 |
| out | w0 (8) | 1 | rule009_1 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | rule009_2 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | rule014_1 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | rule014_2 | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -2..3, possible -2..3; certain > 0 in 8.2%, possibly > 0 in 8.2%
- u net charge, all privates >= 6: charge certain -2..-1, possible -2..-1; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(8) 4 [rule009_1, rule009_2, rule014_1, rule014_2]; IN from 5s 8, from 6s 4
- (certain, possible) histogram: -2:29760, -1:25040, 0:16940, 1:5715, 2:665, 3:5

## 7 7766556 6576576   (cert weight -0.00950)

Privates: p0.1 p0.2 p1.1 p1.2 p2.1 p3.1 p6.1 (7; 78125 exact fillings over 5..9)
Base charge of u: 10(6-7) = -10.

### RSST (Gonthier drules; m = mirror)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | drule21m | p0.1=5 & p0.2=5 | 0.040 / 0.040 |
| in | w0 (7) | 1 | drule9m | p0.1=5 | 0.200 / 0.200 |
| in | w1 (7) | 1 | drule8 | always | 1.000 / 1.000 |
| in | w1 (7) | 1 | drule9 | p1.2=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | drule2' | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | drule4 | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | drule6 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule3 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule2m | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule3m | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule2'm | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule8 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule9 | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | drule21m | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | drule9m | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -1..2, possible -1..2; certain > 0 in 7.2%, possibly > 0 in 7.2%
- u net charge, all privates >= 6: charge certain -1..-1, possible -1..-1; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 2 [drule8, drule9]; w1(7) 2 [drule9m, drule21m]; IN from 5s 8, from 6s 4, from 7s 1
- (certain, possible) histogram: -1:50000, 0:22500, 1:5000, 2:625

### NL26 (Inoue et al. 2026 rule files)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | rule009_2 | p0.1=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | rule014_2 | p0.1=5 & p0.2=5 & p6.1>=6 | 0.032 / 0.032 |
| in | w0 (7) | 1 | rule036_2 | p0.1=5 & p6.1=5 | 0.040 / 0.040 |
| in | w1 (7) | 1 | rule008_1 | always | 1.000 / 1.000 |
| in | w1 (7) | 1 | rule009_1 | p1.2=5 | 0.200 / 0.200 |
| in | w1 (7) | 1 | rule019_1 | p1.1=5 & p1.2=6 | 0.040 / 0.040 |
| in | w3 (6) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | rule004_1 | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | rule006_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule004_2 | p3.1=5 | 0.200 / 0.200 |
| in | w5 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | rule002_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule008_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule009_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule021_1 | p0.1=5 & p0.2>=6 | 0.160 / 0.160 |
| out | w1 (7) | 1 | rule009_2 | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | rule014_2 | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -1..3, possible -1..3; certain > 0 in 9.7%, possibly > 0 in 9.7%
- u net charge, all privates >= 6: charge certain -1..-1, possible -1..-1; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 2 [rule008_1, rule009_1]; w1(7) 2 [rule009_2, rule014_2]; IN from 5s 8, from 6s 4, from 7s 1
- (certain, possible) histogram: -1:44080, 0:26460, 1:6240, 2:1195, 3:150

## 7 7665566 6675676   (cert weight -0.00950)

Privates: p0.1 p0.2 p1.1 p2.1 p5.1 p6.1 (6; 15625 exact fillings over 5..9)
Base charge of u: 10(6-7) = -10.

### RSST (Gonthier drules; m = mirror)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | drule9 | p0.2=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | drule9m | p0.1=5 | 0.200 / 0.200 |
| in | w1 (6) | 1 | drule4' | p2.1=5 | 0.200 / 0.200 |
| in | w2 (6) | 1 | drule2' | always | 1.000 / 1.000 |
| in | w2 (6) | 1 | drule4'm | p1.1=5 | 0.200 / 0.200 |
| in | w3 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule3 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule2m | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule3m | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | drule2'm | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | drule4m | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | drule6m | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule9 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule9m | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain 0..4, possible 0..4; certain > 0 in 59.0%, possibly > 0 in 59.0%
- u net charge, all privates >= 6: charge certain 0..0, possible 0..0; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 2 [drule9, drule9m]; IN from 5s 8, from 6s 4
- (certain, possible) histogram: 0:6400, 1:6400, 2:2400, 3:400, 4:25

### NL26 (Inoue et al. 2026 rule files)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | rule009_1 | p0.2=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | rule009_2 | p0.1=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | rule014_1 | p0.1=5 & p0.2=5 & p1.1>=6 | 0.032 / 0.032 |
| in | w0 (7) | 1 | rule014_2 | p0.1=5 & p0.2=5 & p6.1>=6 | 0.032 / 0.032 |
| in | w1 (6) | 1 | rule004_1 | p2.1=5 | 0.200 / 0.200 |
| in | w2 (6) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w2 (6) | 1 | rule004_2 | p1.1=5 | 0.200 / 0.200 |
| in | w3 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule004_1 | p5.1=5 | 0.200 / 0.200 |
| in | w5 (6) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | rule004_2 | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | rule006_2 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule009_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule009_2 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule014_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule014_2 | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -2..4, possible -2..4; certain > 0 in 7.8%, possibly > 0 in 7.8%
- u net charge, all privates >= 6: charge certain -2..-2, possible -2..-2; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 4 [rule009_1, rule009_2, rule014_1, rule014_2]; IN from 5s 8, from 6s 4
- (certain, possible) histogram: -2:5120, -1:6400, 0:2880, 1:640, 2:400, 3:165, 4:20

## 7 7766556 6567566   (cert weight -0.09836)

Privates: p0.1 p0.2 p1.1 p1.2 p2.1 p3.1 p6.1 (7; 78125 exact fillings over 5..9)
Base charge of u: 10(6-7) = -10.

### RSST (Gonthier drules; m = mirror)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | drule21m | p0.1=5 & p0.2=5 | 0.040 / 0.040 |
| in | w0 (7) | 1 | drule9m | p0.1=5 | 0.200 / 0.200 |
| in | w1 (7) | 1 | drule8 | always | 1.000 / 1.000 |
| in | w1 (7) | 1 | drule9 | p1.2=5 | 0.200 / 0.200 |
| in | w2 (6) | 1 | drule4' | p3.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | drule2' | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | drule4'm | p2.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | drule5m | p2.1<=6 | 0.400 / 0.400 |
| in | w4 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule3 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule2m | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule3m | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule2'm | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule4m | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule6m | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule8 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule9 | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | drule21m | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | drule9m | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -1..5, possible -1..5; certain > 0 in 37.5%, possibly > 0 in 37.5%
- u net charge, all privates >= 6: charge certain -1..0, possible -1..0; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 2 [drule8, drule9]; w1(7) 2 [drule9m, drule21m]; IN from 5s 8, from 6s 4, from 7s 1
- (certain, possible) histogram: -1:24000, 0:24800, 1:18700, 2:8200, 3:2075, 4:325, 5:25

### NL26 (Inoue et al. 2026 rule files)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | rule009_2 | p0.1=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | rule014_2 | p0.1=5 & p0.2=5 & p6.1>=6 | 0.032 / 0.032 |
| in | w0 (7) | 1 | rule036_2 | p0.1=5 & p6.1=5 | 0.040 / 0.040 |
| in | w1 (7) | 1 | rule008_1 | always | 1.000 / 1.000 |
| in | w1 (7) | 1 | rule009_1 | p1.2=5 | 0.200 / 0.200 |
| in | w1 (7) | 1 | rule019_1 | p1.1=5 & p1.2=6 | 0.040 / 0.040 |
| in | w2 (6) | 1 | rule004_1 | p3.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | rule004_2 | p2.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | rule005_1 | p2.1<=6 | 0.400 / 0.400 |
| in | w4 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w5 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule004_1 | p6.1=5 | 0.200 / 0.200 |
| in | w6 (6) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | rule004_2 | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | rule006_2 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule008_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule009_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule021_1 | p0.1=5 & p0.2>=6 | 0.160 / 0.160 |
| out | w1 (7) | 1 | rule009_2 | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | rule014_2 | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -1..6, possible -1..6; certain > 0 in 41.0%, possibly > 0 in 41.0%
- u net charge, all privates >= 6: charge certain -1..0, possible -1..0; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 2 [rule008_1, rule009_1]; w1(7) 2 [rule009_2, rule014_2]; IN from 5s 8, from 6s 4, from 7s 1
- (certain, possible) histogram: -1:21888, 0:24240, 1:19076, 2:9312, 3:2857, 4:649, 5:97, 6:6

## 7 7766556 6566576   (cert weight -0.05464)

Privates: p0.1 p0.2 p1.1 p1.2 p2.1 p3.1 p6.1 (7; 78125 exact fillings over 5..9)
Base charge of u: 10(6-7) = -10.

### RSST (Gonthier drules; m = mirror)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | drule21m | p0.1=5 & p0.2=5 | 0.040 / 0.040 |
| in | w0 (7) | 1 | drule9m | p0.1=5 | 0.200 / 0.200 |
| in | w1 (7) | 1 | drule8 | always | 1.000 / 1.000 |
| in | w1 (7) | 1 | drule9 | p1.2=5 | 0.200 / 0.200 |
| in | w2 (6) | 1 | drule4' | p3.1=5 | 0.200 / 0.200 |
| in | w2 (6) | 1 | drule7 | p3.1=6 | 0.200 / 0.200 |
| in | w3 (6) | 1 | drule2' | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | drule4 | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | drule4'm | p2.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | drule5m | p2.1<=6 | 0.400 / 0.400 |
| in | w3 (6) | 1 | drule6 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule3 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule2m | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule3m | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule2'm | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule8 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule9 | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | drule21m | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | drule9m | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -1..5, possible -1..5; certain > 0 in 43.6%, possibly > 0 in 43.6%
- u net charge, all privates >= 6: charge certain -1..1, possible -1..1; certain > 0 in 6.2%, possibly > 0 in 6.2%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 2 [drule8, drule9]; w1(7) 2 [drule9m, drule21m]; IN from 5s 8, from 6s 4, from 7s 1
- (certain, possible) histogram: -1:18000, 0:26100, 1:19900, 2:10525, 3:3025, 4:525, 5:50

### NL26 (Inoue et al. 2026 rule files)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | rule009_2 | p0.1=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | rule014_2 | p0.1=5 & p0.2=5 & p6.1>=6 | 0.032 / 0.032 |
| in | w0 (7) | 1 | rule036_2 | p0.1=5 & p6.1=5 | 0.040 / 0.040 |
| in | w1 (7) | 1 | rule008_1 | always | 1.000 / 1.000 |
| in | w1 (7) | 1 | rule009_1 | p1.2=5 | 0.200 / 0.200 |
| in | w1 (7) | 1 | rule019_1 | p1.1=5 & p1.2=6 | 0.040 / 0.040 |
| in | w2 (6) | 1 | rule004_1 | p3.1=5 | 0.200 / 0.200 |
| in | w2 (6) | 1 | rule007_1 | p3.1<=6 | 0.400 / 0.400 |
| in | w3 (6) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | rule004_1 | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | rule004_2 | p2.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | rule005_1 | p2.1<=6 | 0.400 / 0.400 |
| in | w3 (6) | 1 | rule006_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule004_2 | p3.1=5 | 0.200 / 0.200 |
| in | w5 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | rule002_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule008_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule009_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule021_1 | p0.1=5 & p0.2>=6 | 0.160 / 0.160 |
| out | w1 (7) | 1 | rule009_2 | always | 1.000 / 1.000 |
| out | w1 (7) | 1 | rule014_2 | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -1..7, possible -1..7; certain > 0 in 48.8%, possibly > 0 in 48.8%
- u net charge, all privates >= 6: charge certain -1..1, possible -1..1; certain > 0 in 6.2%, possibly > 0 in 6.2%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 2 [rule008_1, rule009_1]; w1(7) 2 [rule009_2, rule014_2]; IN from 5s 8, from 6s 4, from 7s 1
- (certain, possible) histogram: -1:19836, 0:20172, 1:14519, 2:12888, 3:5948, 4:3572, 5:1011, 6:149, 7:30

## 7 7665566 6775676   (cert weight -0.02186)

Privates: p0.1 p0.2 p1.1 p2.1 p5.1 p6.1 (6; 15625 exact fillings over 5..9)
Base charge of u: 10(6-7) = -10.

### RSST (Gonthier drules; m = mirror)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | drule9 | p0.2=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | drule9m | p0.1=5 | 0.200 / 0.200 |
| in | w2 (6) | 1 | drule2' | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | drule3 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule2m | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | drule3m | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | drule2'm | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | drule4m | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | drule6m | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule9 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | drule9m | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain 0..2, possible 0..2; certain > 0 in 36.0%, possibly > 0 in 36.0%
- u net charge, all privates >= 6: charge certain 0..0, possible 0..0; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 2 [drule9, drule9m]; IN from 5s 8, from 6s 4
- (certain, possible) histogram: 0:10000, 1:5000, 2:625

### NL26 (Inoue et al. 2026 rule files)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | rule009_1 | p0.2=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | rule009_2 | p0.1=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | rule014_1 | p0.1=5 & p0.2=5 & p1.1>=6 | 0.032 / 0.032 |
| in | w0 (7) | 1 | rule014_2 | p0.1=5 & p0.2=5 & p6.1>=6 | 0.032 / 0.032 |
| in | w2 (6) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w3 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w3 (5) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w4 (5) | 1 | rule004_1 | p5.1=5 | 0.200 / 0.200 |
| in | w5 (6) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | rule004_2 | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | rule006_2 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule009_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule009_2 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule014_1 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule014_2 | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -2..3, possible -2..3; certain > 0 in 3.9%, possibly > 0 in 3.9%
- u net charge, all privates >= 6: charge certain -2..-2, possible -2..-2; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 4 [rule009_1, rule009_2, rule014_1, rule014_2]; IN from 5s 8, from 6s 4
- (certain, possible) histogram: -2:8000, -1:6000, 0:1020, 1:165, 2:360, 3:80

## 7 8677656 5566555   (cert weight -0.05701)

Privates: p0.1 p0.2 p0.3 p1.1 p2.1 p2.2 p3.1 p3.2 p4.1 p6.1 (10; 400000 sampled fillings over 5..9)
Base charge of u: 10(6-7) = -10.

### RSST (Gonthier drules; m = mirror)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w2 (7) | 1 | drule8m | always | 1.000 / 1.000 |
| in | w2 (7) | 1 | drule9m | p2.1=5 | 0.199 / 0.199 |
| in | w3 (7) | 1 | drule21 | p3.1=5 & p3.2=5 | 0.040 / 0.040 |
| in | w3 (7) | 1 | drule9 | p3.2=5 | 0.200 / 0.200 |
| in | w4 (6) | 1 | drule2' | always | 1.000 / 1.000 |
| in | w4 (6) | 1 | drule3' | always | 1.000 / 1.000 |
| in | w4 (6) | 1 | drule4 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule3 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | drule3m | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule2'm | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule3'm | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule4m | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | drule8 | always | 1.000 / 1.000 |
| out | w3 (7) | 1 | drule8m | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -1..2, possible -1..2; certain > 0 in 7.2%, possibly > 0 in 7.2%
- u net charge, all privates >= 6: charge certain -1..-1, possible -1..-1; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(8) 1 [drule8]; w3(7) 1 [drule8m]; IN from 5s 4, from 6s 6, from 7s 1
- (certain, possible) histogram: -1:256419, 0:114745, 1:25602, 2:3234

### NL26 (Inoue et al. 2026 rule files)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (8) | 1 | rule042_1 | p0.1=5 & p0.2=5 & p0.3=5 | 0.008 / 0.008 |
| in | w0 (8) | 1 | rule042_2 | p0.1=5 & p0.2=5 & p0.3=5 | 0.008 / 0.008 |
| in | w2 (7) | 1 | rule008_2 | always | 1.000 / 1.000 |
| in | w2 (7) | 1 | rule009_2 | p2.1=5 | 0.199 / 0.199 |
| in | w2 (7) | 1 | rule019_2 | p2.1=6 & p2.2=5 | 0.040 / 0.040 |
| in | w3 (7) | 1 | rule009_1 | p3.2=5 | 0.200 / 0.200 |
| in | w3 (7) | 1 | rule014_1 | p3.1=5 & p3.2=5 & p4.1>=6 | 0.032 / 0.032 |
| in | w3 (7) | 1 | rule036_1 | p3.2=5 & p4.1=5 | 0.040 / 0.040 |
| in | w4 (6) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w4 (6) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w4 (6) | 1 | rule004_1 | always | 1.000 / 1.000 |
| in | w5 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w5 (5) | 1 | rule004_1 | p6.1=5 | 0.199 / 0.199 |
| in | w5 (5) | 1 | rule004_2 | p4.1=5 | 0.200 / 0.200 |
| in | w6 (6) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | rule004_2 | always | 1.000 / 1.000 |
| out | w0 (8) | 1 | rule008_1 | always | 1.000 / 1.000 |
| out | w3 (7) | 1 | rule008_2 | always | 1.000 / 1.000 |
| out | w3 (7) | 1 | rule021_2 | p3.1>=6 & p3.2=5 | 0.159 / 0.159 |

- u net charge, all fillings: charge certain -1..6, possible -1..6; certain > 0 in 17.8%, possibly > 0 in 17.8%
- u net charge, all privates >= 6: charge certain -1..-1, possible -1..-1; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(8) 1 [rule008_1]; w3(7) 1 [rule008_2]; IN from 5s 4, from 6s 6, from 7s 1
- (certain, possible) histogram: -1:185522, 0:143417, 1:53003, 2:14980, 3:2780, 4:273, 5:23, 6:2

## 7 7656766 6666555   (cert weight -0.08197)

Privates: p0.1 p0.2 p1.1 p3.1 p4.1 p4.2 p5.1 p6.1 (8; 390625 exact fillings over 5..9)
Base charge of u: 10(6-7) = -10.

### RSST (Gonthier drules; m = mirror)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | drule20m | p0.1=5 & p0.2=5 | 0.040 / 0.040 |
| in | w0 (7) | 1 | drule21 | p0.1=5 & p0.2=5 | 0.040 / 0.040 |
| in | w0 (7) | 1 | drule8m | always | 1.000 / 1.000 |
| in | w0 (7) | 1 | drule9 | p0.2=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | drule9m | p0.1=5 | 0.200 / 0.200 |
| in | w1 (6) | 1 | drule2' | always | 1.000 / 1.000 |
| in | w2 (5) | 1 | drule1 | always | 1.000 / 1.000 |
| in | w2 (5) | 1 | drule1#2 | always | 1.000 / 1.000 |
| in | w3 (6) | 1 | drule2'm | always | 1.000 / 1.000 |
| in | w4 (7) | 1 | drule20 | p4.1=5 & p4.2=5 | 0.040 / 0.040 |
| in | w4 (7) | 1 | drule21m | p4.1=5 & p4.2=5 | 0.040 / 0.040 |
| in | w4 (7) | 1 | drule8 | always | 1.000 / 1.000 |
| in | w4 (7) | 1 | drule9 | p4.2=5 | 0.200 / 0.200 |
| in | w4 (7) | 1 | drule9m | p4.1=5 | 0.200 / 0.200 |
| in | w5 (6) | 1 | drule3' | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | drule4' | p6.1=5 | 0.200 / 0.200 |
| in | w6 (6) | 1 | drule3'm | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | drule4'm | p5.1=5 | 0.200 / 0.200 |
| out | w0 (7) | 1 | drule8m | always | 1.000 / 1.000 |
| out | w4 (7) | 1 | drule8 | always | 1.000 / 1.000 |

- u net charge, all fillings: charge certain -4..6, possible -4..6; certain > 0 in 4.6%, possibly > 0 in 4.6%
- u net charge, all privates >= 6: charge certain -4..-4, possible -4..-4; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 1 [drule8m]; w4(7) 1 [drule8]; IN from 5s 2, from 6s 4, from 7s 2
- (certain, possible) histogram: -4:102400, -3:153600, -2:83200, -1:19200, 0:14400, 1:12800, 2:4000, 3:400, 4:400, 5:200, 6:25

### NL26 (Inoue et al. 2026 rule files)

| dir | partner | units | rule | fires when | share of fillings (sure / possible) |
|---|---|---|---|---|---|
| in | w0 (7) | 1 | rule008_2 | always | 1.000 / 1.000 |
| in | w0 (7) | 1 | rule009_1 | p0.2=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | rule009_2 | p0.1=5 | 0.200 / 0.200 |
| in | w0 (7) | 1 | rule014_1 | p0.1=5 & p0.2=5 & p1.1>=6 | 0.032 / 0.032 |
| in | w0 (7) | 1 | rule019_2 | p0.1=6 & p0.2=5 | 0.040 / 0.040 |
| in | w0 (7) | 1 | rule020_1 | p0.1=5 & p0.2=6 & p1.1>=6 | 0.032 / 0.032 |
| in | w1 (6) | 1 | rule002_2 | always | 1.000 / 1.000 |
| in | w2 (5) | 2 | rule001 | always | 1.000 / 1.000 |
| in | w2 (5) | 1 | rule004_1 | p3.1=5 | 0.200 / 0.200 |
| in | w2 (5) | 1 | rule004_2 | p1.1=5 | 0.200 / 0.200 |
| in | w3 (6) | 1 | rule002_1 | always | 1.000 / 1.000 |
| in | w4 (7) | 1 | rule008_1 | always | 1.000 / 1.000 |
| in | w4 (7) | 1 | rule009_1 | p4.2=5 | 0.200 / 0.200 |
| in | w4 (7) | 1 | rule009_2 | p4.1=5 | 0.200 / 0.200 |
| in | w4 (7) | 1 | rule014_2 | p3.1>=6 & p4.1=5 & p4.2=5 | 0.032 / 0.032 |
| in | w4 (7) | 1 | rule019_1 | p4.1=5 & p4.2=6 | 0.040 / 0.040 |
| in | w4 (7) | 1 | rule020_2 | p3.1>=6 & p4.1=6 & p4.2=5 | 0.032 / 0.032 |
| in | w5 (6) | 1 | rule003_1 | always | 1.000 / 1.000 |
| in | w5 (6) | 1 | rule004_1 | p6.1=5 | 0.200 / 0.200 |
| in | w5 (6) | 1 | rule005_2 | p6.1<=6 | 0.400 / 0.400 |
| in | w6 (6) | 1 | rule003_2 | always | 1.000 / 1.000 |
| in | w6 (6) | 1 | rule004_2 | p5.1=5 | 0.200 / 0.200 |
| in | w6 (6) | 1 | rule005_1 | p5.1<=6 | 0.400 / 0.400 |
| out | w0 (7) | 1 | rule008_2 | always | 1.000 / 1.000 |
| out | w0 (7) | 1 | rule021_2 | p0.1>=6 & p0.2=5 | 0.160 / 0.160 |
| out | w4 (7) | 1 | rule008_1 | always | 1.000 / 1.000 |
| out | w4 (7) | 1 | rule021_1 | p4.1=5 & p4.2>=6 | 0.160 / 0.160 |

- u net charge, all fillings: charge certain -4..6, possible -4..6; certain > 0 in 9.4%, possibly > 0 in 9.4%
- u net charge, all privates >= 6: charge certain -4..-2, possible -4..-2; certain > 0 in 0.0%, possibly > 0 in 0.0%
- at privates >= 6, rules that fire in every filling: OUT w0(7) 1 [rule008_2]; w4(7) 1 [rule008_1]; IN from 5s 2, from 6s 4, from 7s 2
- (certain, possible) histogram: -4:51984, -3:82536, -2:95689, -1:76860, 0:46786, 1:23632, 2:9155, 3:3032, 4:786, 5:140, 6:25


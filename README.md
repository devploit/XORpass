<p align="center">
<img src="https://i.imgur.com/iqe1grK.png" width="600" height="200" >
</p>

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)

XORpass is an encoder to bypass WAF filters using XOR operations.

### Installation & Usage
```
git clone https://github.com/devploit/XORpass
cd XORpass

$ python3 xorpass.py -h
```

### Example of bypass:
Using clear PHP function:
<img src="https://i.imgur.com/qMhGrCA.png" width="800" height="200">

Using XOR bypass of that function:
```bash
$ python3 xorpass.py -e "system(ls)"
```
<img src="https://i.imgur.com/iLF2rg7.png" width="800" height="200">

#### Why does PHP treat our payload as a string?

The ^ is the exclusive or operator, which means that we're in reality working with binary values. So lets break down what happens.

The XOR operator on binary values will return 1 where just one of the bits were 1, otherwise it returns 0 (0^0 = 0, 0^1 = 1, 1^0 = 1, 1^1 = 0). When you use XOR on characters, you're using their ASCII values. These ASCII values are integers, so we need to convert those to binary to see what's actually going on.

```
A = 65 = 1000001
S = 83 = 1010011
B = 66 = 1000010

A       1000001
        ^
S       1010011
        ^
B       1000010
----------------
result  1010000 = 80 = P

A^S^B = P
```

If we do an 'echo "A"^"S"^"B";' PHP will return us a P as we see.

<img src="https://i.imgur.com/7IAD6ZY.png" width="250" height="100">

### Contributors
[@julianjm](https://github.com/julianjm)

### Contact
[![Twitter: devploit](https://img.shields.io/badge/-Twitter-blue?style=flat-square&logo=Twitter&logoColor=white&link=https://twitter.com/devploit/)](https://twitter.com/devploit/)

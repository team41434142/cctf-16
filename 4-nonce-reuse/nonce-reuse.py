#!/usr/bin/env python

import binascii

# Ciphertexts encrypted with same key and nonce in AES-CTR
c1 = "369f9e696bffa098d2bb383fb148bd90"
c1 = int(c1, 16)
c2 = "23d7847f28e4b6cc86be386cb64ca281"
c2 = int(c2, 16)

# The xor of these ciphertexts is equal to the xor of the plaintexts
xor_ps = c1 ^ c2
xor_ps = bin(xor_ps)[2:]

class CharacterFound(Exception):
    """Raised to break both loops through ascii characters when characters that
    satisfy the binary relation for each xor-of-plaintext character are
    found."""

for character in range(int(len(xor_ps) / 7)):
    ps_char = xor_ps[(character*7):((character+1)*7)]
    try:
        for i in range(32, 127):
            for j in range(32, 127):
                xor = i ^ j
                xor = bin(xor)[2:]
                if xor == ps_char:
                    print("{},{}".format(chr(i),chr(j)))
                    raise CharacterFound
    except CharacterFound:
        continue

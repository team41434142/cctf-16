#!/usr/bin/env python

import binascii
import rsa
import sys
import urllib.request

# Import the server public key
with open("pubk.pem") as pubk:
    pubk = rsa.PublicKey.load_pkcs1_openssl_pem(pubk.read())

# The ciphertext of which to find the corresponding plaintext
c = "912fcd40a901aa4b7b60ec37ce6231bb87783b0bf36f824e51fe77e9580ce1adb5cf894410ff87684969795525a63e069ee962182f3ff876904193e5eb2f34b20cfa37ec7ae0e9391bec3e5aa657246bd80276c373798885e5a986649d27b9e04f1adf8e6218f3c805c341cb38092ab771677221f40b72b19c75ad312b6b95eafe2b2a30efe49eb0a5b19a75d0b31849535b717c41748a6edd921142cfa7efe692c9a776bb4ece811afbd5a1bbd82251b76e76088d91ed78bf328c6b608bbfd8cf1bdf388d4dfa4d4e034a54677a16e16521f7d0213a3500e91d6ad4ac294c7a01995e1128a5ac68bfc26304e13c60a6622c1bb6b54b57c8dcfa7651b81576fc"
c = int(c, 16)

# "Arbitrary" message to use in our CCA
r = b"ACAB"
r = int(binascii.hexlify(r), 16)
c_r = pow(r, pubk.e, pubk.n)

# Find the product of the ciphertext of our message and the given ciphertext
c_prod = c_r * c
c_prod = hex(c_prod)[2:] # Remove the "0x"

# Query our decryption oracle to return the product of our message and the
# plaintext of the given ciphertext
response = urllib.request.urlopen("https://id0-rsa.pub/problem/rsa_oracle/{}".format(c_prod))
prod = response.read()
prod = int(prod, 16)


# Find the multiplicative modular inverse of r modulo n
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
sys.setrecursionlimit(1000000)  # long type,32bit OS 4B,64bit OS 8B(1bit for sign)

# return (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

i_r = mulinv(r, pubk.n)

# Multiple the prod by the inverse of r module n to find the plaintext of the
# given ciphertext
p = (prod * i_r) % pubk.n
p = hex(p)[2:]
print(p)
p = binascii.unhexlify(p)
print(p)

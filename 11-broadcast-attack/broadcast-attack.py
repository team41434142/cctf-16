#!/usr/bin/env python

# Håstad's Broadcast Attack
# RSA with a small exponent is fast to compute but it has a serious weakness.

# A message was encrypted with three different 1024 bit RSA public keys, all of
# which have the exponent e=3 and different moduli N, resulting in three
# ciphertexts. Luckily, there is an attack that we can use to recover the
# message without having to recover the private key / factor the moduli. Given
# the following ciphertext / modulus pairs, recover the original message in
# ASCII string format. (Hint: check out the Chinese Remainder Theorem).
c1 = "94f145679ee247b023b09f917beea7e38707452c5f4dc443bba4d089a18ec42de6e32806cc967e09a28ea6fd2e683d5bb7258bce9e6f972d6a30d7e5acbfba0a85610261fb3e0aac33a9e833234a11895402bc828da3c74ea2979eb833cd644b8ab9e3b1e46515f47a49ee602c608812241e56b94bcf76cfbb13532d9f4ff8ba"
n1 = "a5d1c341e4837bf7f2317024f4436fb25a450ddabd7293a0897ebecc24e443efc47672a6ece7f9cac05661182f3abbb0272444ce650a819b477fd72bf01210d7e1fbb7eb526ce77372f1aa6c9ce570066deee1ea95ddd22533cbc68b3ba20ec737b002dfc6f33dcb19e6f9b312caa59c81bb80cda1facf16536cb3c184abd1d5"
c2 = "5ad248df283350558ba4dc22e5ec8325364b3e0b530b143f59e40c9c2e505217c3b60a0fae366845383adb3efe37da1b9ae37851811c4006599d3c1c852edd4d66e4984d114f4ea89d8b2aef45cc531cfa1ab16c7a2e04d8884a071fed79a8d30af66edf1bbbf695ff8670b9fccf83860a06e017d67b1788b19b72d597d7d8d8"
n2 = "af4ed50f72b0b1eec2cde78275bcb8ff59deeeb5103ccbe5aaef18b4ddc5d353fc6dc990d8b94b3d0c1750030e48a61edd4e31122a670e5e942ae224ecd7b5af7c13b6b3ff8bcc41591cbf2d8223d32eeb46ba0d7e6d9ab52a728be56cd284842337db037e1a1da246ed1da0fd9bdb423bbe302e813f3c9b3f9414b25e28bda5"
c3 = "8a9315ee3438a879f8af97f45df528de7a43cd9cf4b9516f5a9104e5f1c7c2cdbf754b1fa0702b3af7cecfd69a425f0676c8c1f750f32b736c6498cac207aa9d844c50e654ceaced2e0175e9cfcc2b9f975e3183437db73111a4a139d48cc6ce4c6fac4bf93b98787ed8a476a9eb4db4fd190c3d8bf4d5c4f66102c6dd36b73"
n3 = "5ca9a30effc85f47f5889d74fd35e16705c5d1a767004fec7fdf429a205f01fd7ad876c0128ddc52caebaa0842a89996379ac286bc96ebbb71a0f8c3db212a18839f7877ebd76c3c7d8e86bf6ddb17c9c93a28defb8c58983e11304d483fd7caa19b4b261fc40a19380abae30f8d274481a432c8de488d0ea7b680ad6cf7776b"
e = 3

# *~*~*~*

import binascii

c1 = int(c1,16)
c2 = int(c2,16)
c3 = int(c3,16)
n1 = int(n1,16)
n2 = int(n2,16)
n3 = int(n3,16)

cprod = c1 * c2 * c3

class CongruenceClass:
    def __init__(self, c, n):
        self.c = c
        self.n = n

cc1 = CongruenceClass(c1, n1)
cc2 = CongruenceClass(c2, n2)
cc3 = CongruenceClass(c3, n3)
ccs= [cc1, cc2, cc3]
ccs = sorted(ccs, key=lambda cc: cc.n, reverse=True)

# The Chinese remainder theorem guarantees a unique solution c such that 
# ci = c % ni

# We begin by considering the integers i congruent to ciphertext
# with the largest modulus, where 0 <= i < cprod

for i in range(cprod // ccs[0].n):
    c = ccs[0].c + (ccs[0].n * i)
    if ((c % ccs[1].n) == ccs[1].c):
        print("hit")
        if ((c % ccs[2].n) == ccs[2].c):
            break

m = pow(c, 1/3)
m = hex(m)[2:]
m = binascii.unhexlify(m)
print(m)

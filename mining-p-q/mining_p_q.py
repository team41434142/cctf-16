import pdb
import pyasn1.codec.der.encoder
import pyasn1.type.univ
import base64


def pempriv(n, e, d, p, q):
    dP = d % p
    dQ = d % q
    qInv = pow(q, p - 2, p)

    template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'
    seq = pyasn1.type.univ.Sequence()

    for x in [0, n, e, d, p, q, dP, dQ, qInv]:
        seq.setComponentByPosition(len(seq), pyasn1.type.univ.Integer(x))

    der = pyasn1.codec.der.encoder.encode(seq)
    return template.format(base64.encodestring(der).decode('ascii'))


def egcd(a, b):
    # liberated from stackoverflow
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    # liberated from stackoverflow
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def gcd(*numbers):
    from fractions import gcd
    return reduce(gcd, numbers)


def main():
    # used openssl asn1parse 
    msg = 'f5ed9da29d8d260f22657e091f34eb930bc42f26f1e023f863ba13bee39071d1ea988ca62b9ad59d4f234fa7d682e22ce3194bbe5b801df3bd976db06b944da'
    pubkey_raw_1 = 'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKzl5VggSXb/Jm2oqkPeRQwtpmGlLnJTNre4LKx3VUljtLzYWj4xoG+aHBouwJT7DyeibpasCH8Yderr4zIGTNUCAwEAAQ=='
    pubkey_1 = 'ACE5E558204976FF266DA8AA43DE450C2DA661A52E725336B7B82CAC77554963B4BCD85A3E31A06F9A1C1A2EC094FB0F27A26E96AC087F1875EAEBE332064CD5'
    pubkey_raw_2 = 'MF0wDQYJKoZIhvcNAQEBBQADTAAwSQJCAPsrpwx56OTlKtGAWn24bo5HUg3xYtnznTj1X/8Hq7pLYNIVE57Yxoyr3zTOOBJufgTNzdKS0Rc5Ti4zZUkCkQvpAgMBAAE='
    pubkey_2 = 'FB2BA70C79E8E4E52AD1805A7DB86E8E47520DF162D9F39D38F55FFF07ABBA4B60D215139ED8C68CABDF34CE38126E7E04CDCDD292D117394E2E33654902910BE9'

    n = int(pubkey_1, 16)

    # p is a common prime
    p = gcd(n, int(pubkey_2, 16))
    
    # factoring n 
    q = n / p
 
    e = 65537
    d = modinv(e, (p-1) * (q-1))
    privatekey = pempriv(n, e, d, p, q)

    m = pow(int(msg, 16), d, n)
    print(hex(m))

import ecdsa
from ecdsa import SigningKey

z1 = 78963682628359021178354263774457319969002651313568557216154777320971976772376
s1 = 5416854926380100427833180746305766840425542218870878667299
r1 = 5568285309948811794296918647045908208072077338037998537885

z2 = 62159883521253885305257821420764054581335542629545274203255594975380151338879
s2 = 1063435989394679868923901244364688588218477569545628548100
r2 = 5568285309948811794296918647045908208072077338037998537885

n = 6277101735386680763835789423176059013767194773182842284081

sshift=s1-s2
# rshift=r1-r2
r=r1
zshift=z1-z2
def keydecrypt():
    sdiff_inv = inverse_mod(((sshift)%n),n)
    k = ( ((zshift)%n) * sdiff_inv) % n
    r_inv = inverse_mod(r,n)
    da = (((((s1*k) %n) -z1) %n) * r_inv) % n
    recovered_private_key_ec = ecdsa.SigningKey.from_secret_exponent(da)    
    return recovered_private_key_ec.to_pem()

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def inverse_mod(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

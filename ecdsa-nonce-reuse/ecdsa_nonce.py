import hashlib
import pdb


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


def hex_hash(msg, hashfunc):
    if hashfunc == 'sha256':
        return hashlib.sha256(str(msg)).hexdigest()
    elif hashfunc == 'sha384':
        return hashlib.sha384(str(msg)).hexdigest()
    elif hashfunc == 'sha512':
        return hashlib.sha512(str(msg)).hexdigest()
    elif hashfunc == 'sha1':
        return hashlib.sha1(str(msg)).hexdigest()
    elif hashfunc == 'sha224':
        return hashlib.sha224(str(msg)).hexdigest()
    elif hashfunc == 'md5':
        return hashlib.md5(str(msg)).hexdigest()
    else:
        print('fuuuuuck')


def get_n_leftmost_bits(number, bitlen):
    # take n leftmost bits of each hash, where n 
    # is the bit length of the group order
    binary_no = bin(number).lstrip('0b')
    return binary_no[0:bitlen]


def recover_key(z_1, z_2, s_1, s_2, n):
    # initially i thought that one needed to actually 
    # compute these... one does not. 
    # h_1 = int(hex_hash(z_1, 'sha256'), 16)
    # h_2 = int(hex_hash(z_2, 'sha256'), 16)

    # bitlen_group_ord = len(bin(n).lstrip('0b'))
    # e_1 = get_n_leftmost_bits(h_1, bitlen_group_ord)
    # e_2 = get_n_leftmost_bits(h_2, bitlen_group_ord)

    # hmsg_diff = int(e_1, 2) - int(e_2, 2)
    hmsg_diff = z_1 - z_2

    sigdiff_inv = modinv(s_1 - s_2, n)
    ephemeral_key = (hmsg_diff * sigdiff_inv) % n
    return ephemeral_key


def main():
    z1 = 78963682628359021178354263774457319969002651313568557216154777320971976772376
    s1 = 5416854926380100427833180746305766840425542218870878667299
    r1 = 5568285309948811794296918647045908208072077338037998537885

    z2 = 62159883521253885305257821420764054581335542629545274203255594975380151338879
    s2 = 1063435989394679868923901244364688588218477569545628548100
    r2 = 5568285309948811794296918647045908208072077338037998537885

    n = 6277101735386680763835789423176059013767194773182842284081

    solution = recover_key(z1, z2, s1, s2, n)
    print('The solution is: {}'.format(hex(solution)))


if __name__=='__main__':
    main()

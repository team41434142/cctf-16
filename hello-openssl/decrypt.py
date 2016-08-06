#!/usr/bin/python3

import binascii
import subprocess

test_vectors = [
    '71b71b4f55ba6c921c33fbe91f51bf888bba9761134c2ac6456e02f3802b1b69',
    '842129370f36e80ca715b4cd97570d7a664f8def2c22f580866b04aeaa87fef2',
    'c6128c44895959192315ffc715ef2dd9feaddd25b297696da01d5c3dbfc9cb4b',
    '432beb994a0aef57e61822b1e89c2afa41663ddf9928922ae932894329a1e208',
    'bed8d61a863a430b7c11bb71220db0ed9f605bdfca5c86b202e0b5b021272eb5',
    '03c67f8d506f637b8d447a4f4568e1d0eb27de62db3ff3ea9b93011c35b1e387',
    'c1ade6db41c134eb2cf649366368286dc768462aefad58b17018cad5b65de4',
    '6d2b3c8cf668777e981b9f6690c16a3b0aee07e16aed8a0ab59883671925d855',
    '5e711cd1cdfd3a09429ca06ed16217b8951552c467329d9cebd936f792503329',
    '7fa80734ec297b4f5dd50a14a0981d2ebcf8f19561f43878b49a9774fea00965',
    '6794893f3c47247262e95fbed846e1a623fc67b1dd96e13c7f9fc3b880642e42',
]

for vector in test_vectors:
    cmd = subprocess.run(
        ['openssl', 'rsautl', '-inkey', 'key.pem', '-decrypt', '-raw'],
        input=binascii.unhexlify(vector),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    print(binascii.hexlify(cmd.stdout))

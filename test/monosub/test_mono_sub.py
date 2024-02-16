from ciphers.analysis import strip
from ciphers.monosub.mono_sub import (
    atbash,
    decipher_mono_sub,
    encipher_mono_sub,
    invert_key,
)
from ciphers.test.analysis import get_tests

if __name__ == "__main__":
    testing = "0000"
    testing = [int(i) for i in testing]

    tests = get_tests("testMonoSub.txt")
    plaintext = strip(tests[0])

    if testing[0]:
        print(invert_key(tests[1]))

    if testing[1]:
        print(encipher_mono_sub(plaintext, tests[2]))

    if testing[2]:
        print(decipher_mono_sub(*tests[3].split()))

    if testing[3]:
        print(atbash(plaintext))
        print(atbash(atbash(plaintext)))

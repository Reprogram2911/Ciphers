from ciphers.analysis import strip
from ciphers.monosub.mono_sub import (
    invert_key,
    encipher_mono_sub,
    decipher_mono_sub,
    atbash,
)

if __name__ == "__main__":
    testing = "0000"
    testing = [int(i) for i in testing]

    with open("testMonoSub.txt", "r") as f:
        tests = f.read().split("\n\n")

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

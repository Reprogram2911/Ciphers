from ciphers.analysis import clean
from ciphers.polysub.porta import (
    brute_force_porta,
    decipher_bellaso,
    decipher_porta,
    dictionary_porta,
    encipher_porta,
    hill_climbing_bellaso,
    hill_climbing_porta,
    matching_word,
    periodic_attack_porta,
)
from ciphers.test.utils import get_tests

if __name__ == "__main__":
    testing = "0000000001"
    testing = [int(i) for i in testing]

    tests = get_tests("testPorta.txt")
    tests = [clean(test).replace(" ", "") for test in tests]

    if testing[0]:
        print(encipher_porta(tests[0], "PORTA", 1))
        print(encipher_porta(tests[0], "PORTA", 2))
        print(encipher_porta(tests[1], "PLAGIA", 3))
        print(encipher_porta(tests[2], "KEYWORD", 1))

    if testing[1]:
        print(decipher_porta(tests[3], "CIPHER", 2))

    if testing[2]:
        brute_force_porta(tests[4])
        # IM, v2

    if testing[3]:
        print(matching_word("SECQES"))
        # SECRET

    if testing[4]:
        dictionary_porta(tests[5])
        # INSIDE, v1

    if testing[5]:
        for _ in range(5):
            hill_climbing_porta(tests[6], 6)
        # CKOSES, v2
        # YQMIWI, v1
        print(matching_word("CKOSES"))  # CLOSES
        print(matching_word("YQMIWI"))  # fails

    if testing[6]:
        for _ in range(5):
            hill_climbing_porta(tests[7], 7)  # UAIWEAC v1, GASEWAY v2
        print(matching_word("UAIWEAC"))
        print(matching_word("GASEWAY"))  # GATEWAY

    if testing[7]:
        periodic_attack_porta(tests[7], 7)  # ...

    if testing[8]:
        print(decipher_bellaso(tests[8], "PLAGIARIZE"))

    if testing[9]:
        # period too long for brute force
        # dictionary attack fails
        hill_climbing_bellaso(tests[9], 7)
        # COPYCAT

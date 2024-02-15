from ciphers.analysis.randomness import entropy, ioc, find_block_size
from ciphers.test.analysis.test_fitness import test_function, average_corpus


def find_block_size2(text):
    length = len(text)
    for n in range(2, 7):
        actual = ioc(text, n)
        expected = average_corpus(length, ioc, n)
        print(f"IoC {n}:")
        print(f"\tActual: {actual}")
        print(f"\tExpected: {expected}")


if __name__ == "__main__":
    testing = "00000"
    testing = [int(i) for i in testing]

    with open("testFindBlockSize.txt", "r") as f:
        tests = f.read()
    tests = tests.split("\n\n")
    tests = [test.replace(" ", "").replace("\n", "") for test in tests]

    if testing[0]:
        test_function("Entropy", entropy, False)  # 0.88
        test_function("Entropy", entropy, True)  # 1

    if testing[1]:
        test_function("Index of coincidence", ioc, False)  # 1.73
        test_function("Index of coincidence", ioc, True)  # 1

    if testing[2]:
        for n in range(2, 6):
            test_function("Index of coincidence", ioc, False, n)
        # 1.33, 3.45, 16, 130

    if testing[3]:
        for test in tests:
            find_block_size(test)
        # 6, 4, x, x, x, 5, 4

    if testing[4]:
        for test in tests:
            find_block_size2(test)
        # x, 4, 3, 2/3, x, x, x

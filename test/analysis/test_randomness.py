from ciphers.analysis.randomness import entropy, find_block_size, ioc
from ciphers.test.analysis.test_fitness import average_corpus, test_function


def get_tests(fp):
    with open(fp, "r") as f:
        return f.read().split("\n\n")


def percentage_error(value, expected):
    return abs((value - expected) / expected) * 100


def find_block_size_2(text):
    length = len(text)
    for n in range(2, 7):
        actual = ioc(text, n)
        expected = average_corpus(length, ioc, n)
        print(f"IoC {n}: {percentage_error(actual, expected):.2f}")


if __name__ == "__main__":
    testing = "00000"
    testing = [int(i) for i in testing]

    tests = get_tests("testFindBlockSize.txt")
    tests = [test.replace(" ", "").replace("\n", "") for test in tests]

    if testing[0]:
        test_function("Entropy", entropy, False)  # 0.88
        test_function("Entropy", entropy, True)  # 0.99

    if testing[1]:
        test_function("Index of coincidence", ioc, False)  # 1.73
        test_function("Index of coincidence", ioc, True)  # 1.00

    if testing[2]:
        for n in range(2, 7):
            test_function("Index of coincidence", ioc, False, n)
        # 1.33, 3.4, 16, 130, 1200

    if testing[3]:
        for test in tests:
            find_block_size(test)
        # 6, 4, x, x, x, 5, 4

    if testing[4]:
        for test in tests:
            find_block_size_2(test)  # not as reliable as other function
            print()

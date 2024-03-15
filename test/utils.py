def get_tests(fp):
    with open(fp, "r") as f:
        return f.read().split("\n\n")

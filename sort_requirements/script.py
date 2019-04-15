#!/usr/bin/env python
import os
import sys


from . import sort_requirements


def main():
    files = [os.path.abspath(f) for f in sys.argv[1:]]
    for path in files:
        with open(path, "r") as f:
            data = sort_requirements(f.read())
        with open(path, "w") as f:
            f.write(data)


if __name__ == "__main__":
    main()

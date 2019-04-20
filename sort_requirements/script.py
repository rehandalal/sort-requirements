#!/usr/bin/env python
import argparse
import os
import sys


from . import sort_requirements


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help=(
            "Don't write the files back, just return a list of files that would change. Return "
            "code 0 means nothing would change. Return code 1 means some files would be changed."
        ),
    )

    args = parser.parse_args()

    failed = []

    files = [os.path.abspath(f) for f in args.files]
    for path in files:
        with open(path, "r") as f:
            original = f.read()
            modified = sort_requirements(original)

        if args.check:
            if original != modified:
                failed.append(path)
        else:
            with open(path, "w") as f:
                f.write(modified)

    if args.check and failed:
        print("Some files need sorting:")
        for f in failed:
            print("- {}".format(os.path.relpath(f)))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

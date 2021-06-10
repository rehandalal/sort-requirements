#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import difflib
import os
import sys


from . import sort_requirements


def end(code, args, changed, total):
    """Print results and return code."""
    if not args.quiet:
        if code:
            write = sys.stderr.write
        else:
            write = sys.stdout.write

        write("All done! 🎉\n")

        if changed:
            write(
                "{} file(s) changed, {} file(s) unchanged.\n".format(
                    changed, total - changed
                )
            )
        else:
            write("{} file(s) unchanged.\n".format(total))

    return code


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
    parser.add_argument(
        "-d",
        "--diff",
        action="store_true",
        help="Don't write the files back, just output a diff for each file on stdout.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help=(
            "Don't output any non-error messages. Errors are still output, silence those with "
            "2>/dev/null."
        ),
    )

    args = parser.parse_args()

    changed = 0
    failed = []

    files = [os.path.abspath(f) for f in args.files]
    for path in files:
        with open(path, "r") as f:
            original = f.read()
            modified = sort_requirements(original)
            modified = "\n".join(set(modified.split("\n")))

        if original != modified:
            changed += 1

            if args.diff:
                sys.stderr.writelines(
                    difflib.unified_diff(
                        original.splitlines(True),
                        modified.splitlines(True),
                        fromfile=os.path.relpath(path),
                        tofile=os.path.relpath(path),
                    )
                )
                sys.stderr.write("\n")

            if args.check or args.diff:
                failed.append(path)
            else:
                with open(path, "w") as f:
                    f.write(modified)

    if failed:
        if args.check and not args.quiet:
            sys.stderr.write("Some files need sorting:\n")
            for f in failed:
                sys.stderr.write("- {}\n".format(os.path.relpath(f)))
            sys.stderr.write("\n")

        return end(1, args, changed, len(files))

    return end(0, args, changed, len(files))


if __name__ == "__main__":
    sys.exit(main())

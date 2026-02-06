import os
import sys
import re

from setuptools import find_packages, setup
from setuptools.command.install import install


ROOT = os.path.abspath(os.path.dirname(__file__))

# Read version from __init__.py
version_file = os.path.join(ROOT, "sort_requirements", "__init__.py")
with open(version_file, "r") as f:
    version_match = re.search(r"^VERSION = \((.+?)\)", f.read(), re.MULTILINE)
    if version_match:
        version_tuple = tuple(map(int, version_match.group(1).split(", ")))
        version = ".".join(str(v) for v in version_tuple)
    else:
        raise RuntimeError("Unable to find version string")

with open("README.md", "r") as f:
    long_description = f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != "v{}".format(version):
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, version
            )
            sys.exit(info)


setup(
    name="sort_requirements",
    version=version,
    url="https://github.com/rehandalal/sort-requirements",
    license="Mozilla Public License Version 2.0",
    author="Rehan Dalal",
    author_email="rehan@meet-rehan.com",
    description="A simple script to sort python dependencies in requirement text files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[],
    entry_points={
        "console_scripts": ["sort-requirements = sort_requirements.script:main"]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Build Tools",
    ],
    cmdclass={"verify": VerifyVersionCommand},
)

import os
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install


ROOT = os.path.abspath(os.path.dirname(__file__))

version = __import__("sort_requirements").__version__

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
    py_modules=["sort_requirements"],
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
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Build Tools",
    ],
    cmdclass={"verify": VerifyVersionCommand},
)

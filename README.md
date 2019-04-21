sort-requirements
=================

A simple script to sort python dependencies in requirement text files.

[![PyPI](https://img.shields.io/pypi/v/sort-requirements.svg)](https://pypi.org/project/sort-requirements/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sort-requirements.svg)](https://pypi.org/project/sort-requirements/)

[![CircleCI](https://img.shields.io/circleci/project/github/rehandalal/sort-requirements.svg)](https://circleci.com/gh/rehandalal/sort-requirements)


#### Installation

Installing this tool is easily done using [pip](https://github.com/pypa/pip). 
Assuming `pip` is installed just run the following from the command line:

```
$ pip install sort_requirements
```

This command will download the latest version from the
[Python Package Index](https://pypi.org/project/sort-requirements/)
and install it to your system. More information about `pip` and pypi can be
found here:

* [install pip](https://pip.pypa.io/en/latest/installing.html)
* [pypi](https://pypi.python.org/pypi)

Alternatively you can install from the distribution using the `setup.py`
script:

```
$ python setup.py install
```

You could also install the 
[development version](https://github.com/rehandalal/sort-requirements/tarball/master#egg=sort-requirements-dev)
by running the following:

```
$ pip install therapist==dev
```

Or simple install from a clone of the 
[git repo](https://github.com/rehandalal/therapist/):

```
$ git clone https://github.com/rehandalal/sort-requirements.git
$ mkvirtualenv sort-requirements
$ pip install --editable .
```


#### Usage

To use this tool simply run the following from the command line:

```
$ sort-requirements my-requirements-file.txt
```

Please make sure to replace `my-requirements-file.txt` with the path to your
requirements file(s).

If you only want to get a list of files that need sorting, without actually
writing any changes to the files, use the `--check` flag:

```
$ sort-requirements --check my-requirements-file.txt another-file.txt
```

For even more options use the `--help` flag:

```
$ sort-requirements --help
```

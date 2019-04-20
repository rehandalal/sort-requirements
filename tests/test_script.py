import os
import re
import shutil
import subprocess

import pytest

from . import FIXTURES_DIR


class CLIResult(object):
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


@pytest.fixture()
def cli():
    """A fixture that allows running the CLI"""

    def run_cli(*args, **kwargs):
        options = ["sort-requirements"]

        for a in args:
            options.append(a)

        for kw in kwargs:
            if len(kw) == 1:
                options.append("-{}".format(kw))
            else:
                options.append("--{}".format(kw))
            if not isinstance(kwargs[kw], bool):
                options.append(kwargs[kw])

        popen = subprocess.Popen(
            options, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output = popen.communicate()
        return CLIResult(popen.returncode, output[0], output[1])

    return run_cli


class TestScript(object):
    def test_no_options(self, cli):
        cmd = cli()
        assert cmd.returncode > 0
        assert "the following arguments are required: files" in cmd.stderr.decode()

    def test_single_file(self, cli, tmp_path):
        tfp = os.path.join(tmp_path, "simple.txt")
        shutil.copy(os.path.join(FIXTURES_DIR, "simple.txt"), tfp)

        cli(tfp)

        with open(tfp, "r") as f:
            result = f.read()

        with open(os.path.join(FIXTURES_DIR, "simple-sorted.txt"), "r") as f:
            expected = f.read()

        assert result == expected

    def test_multiple_files(self, cli, tmp_path):
        tfp1 = os.path.join(tmp_path, "simple.txt")
        tfp2 = os.path.join(tmp_path, "complex.txt")
        shutil.copy(os.path.join(FIXTURES_DIR, "simple.txt"), tfp1)
        shutil.copy(os.path.join(FIXTURES_DIR, "complex.txt"), tfp2)

        cli(tfp1, tfp2)

        with open(tfp1, "r") as f:
            result = f.read()

        with open(os.path.join(FIXTURES_DIR, "simple-sorted.txt"), "r") as f:
            expected = f.read()

        assert result == expected

        with open(tfp2, "r") as f:
            result = f.read()

        with open(os.path.join(FIXTURES_DIR, "complex-sorted.txt"), "r") as f:
            expected = f.read()

        assert result == expected

    def test_check_no_issues(self, cli, tmp_path):
        tfp = os.path.join(tmp_path, "simple.txt")
        shutil.copy(os.path.join(FIXTURES_DIR, "simple-sorted.txt"), tfp)

        cmd = cli(tfp, check=True)

        assert cmd.returncode == 0
        assert cmd.stdout.decode() == ""

    def test_check_single_file(self, cli, tmp_path):
        tfp = os.path.join(tmp_path, "simple.txt")
        shutil.copy(os.path.join(FIXTURES_DIR, "simple.txt"), tfp)

        cmd = cli(tfp, check=True)

        pattern = r"Some files need sorting:\n- .+?simple\.txt\n$"

        assert cmd.returncode == 1
        assert re.match(pattern, cmd.stdout.decode()) is not None

    def test_check_multiple_files(self, cli, tmp_path):
        tfp1 = os.path.join(tmp_path, "simple.txt")
        tfp2 = os.path.join(tmp_path, "complex.txt")
        shutil.copy(os.path.join(FIXTURES_DIR, "simple.txt"), tfp1)
        shutil.copy(os.path.join(FIXTURES_DIR, "complex.txt"), tfp2)

        cmd = cli(tfp1, tfp2, check=True)

        pattern = r"Some files need sorting:\n- .+?simple\.txt\n- .+?complex\.txt\n$"

        assert cmd.returncode == 1
        assert re.match(pattern, cmd.stdout.decode()) is not None

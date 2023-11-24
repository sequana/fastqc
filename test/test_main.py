import os
import tempfile
import subprocess
import sys


from sequana_pipelines.fastqc.main import main

from click.testing import CliRunner


from . import test_dir

sharedir = f"{test_dir}/data"


# 
def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = "sequana_fastqc --input-directory {} "
    cmd += "--working-directory {}  --force"
    cmd = cmd.format(sharedir, directory.name)
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()

    runner = CliRunner()
    results = runner.invoke(main, ["--input-directory", sharedir, "--working-directory",
        directory.name, "--force"])
    assert results.exit_code == 0



def test_full_fastqc():

    with tempfile.TemporaryDirectory() as directory:
        wk = directory

        cmd = "sequana_fastqc --input-directory {} "
        cmd += "--working-directory {} --force"
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())


        cmd = "snakemake -s fastqc.rules --wrapper-prefix https://raw.githubusercontent.com/sequana/sequana-wrappers/  -p --cores 2 "

        stat = subprocess.call(cmd.split(), cwd=wk)

        assert os.path.exists(wk + "/summary.html")
        assert os.path.exists(wk + "/tree.html")
        assert os.path.exists(wk + "/multiqc/multiqc_report.html")


def test_version():
    cmd = "sequana_fastqc --version"
    subprocess.call(cmd.split())


def test_help():
    cmd = "sequana_fastqc --help"
    subprocess.call(cmd.split())


def test_help_click():
    runner = CliRunner()
    results = runner.invoke(main, ["--help"])
    assert results.exit_code == 0


def test_full_falco():

    with tempfile.TemporaryDirectory() as directory:
        wk = directory

        cmd = "sequana_fastqc --input-directory {} "
        cmd += "--working-directory {}  --force --method falco"
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())


        cmd = "snakemake -s fastqc.rules --wrapper-prefix https://raw.githubusercontent.com/sequana/sequana-wrappers/  -p --cores 2 "

        stat = subprocess.call(cmd.split(), cwd=wk)

        assert os.path.exists(wk + "/summary.html")
        assert os.path.exists(wk + "/tree.html")
        assert os.path.exists(wk + "/multiqc/multiqc_report.html")


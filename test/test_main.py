import easydev
import os
import tempfile
import subprocess
import sys

from . import test_dir

sharedir = f"{test_dir}/data"


# 
def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = "sequana_fastqc --input-directory {} "
    cmd += "--working-directory {} --run-mode local --force"
    cmd = cmd.format(sharedir, directory.name)
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()
    import sequana_pipelines.fastqc.main as m
    sys.argv = ["test", "--input-directory", sharedir, "--working-directory",
        directory.name, "--run-mode", "local", "--force"]
    m.main()


def test_full_fastqc():

    with tempfile.TemporaryDirectory() as directory:
        wk = directory

        cmd = "sequana_fastqc --input-directory {} "
        cmd += "--working-directory {} --run-mode local --force"
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

def test_full_falco():

    with tempfile.TemporaryDirectory() as directory:
        wk = directory

        cmd = "sequana_fastqc --input-directory {} "
        cmd += "--working-directory {} --run-mode local --force --method falco"
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())


        cmd = "snakemake -s fastqc.rules --wrapper-prefix https://raw.githubusercontent.com/sequana/sequana-wrappers/  -p --cores 2 "

        stat = subprocess.call(cmd.split(), cwd=wk)

        assert os.path.exists(wk + "/summary.html")
        assert os.path.exists(wk + "/tree.html")
        assert os.path.exists(wk + "/multiqc/multiqc_report.html")


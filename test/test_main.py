import easydev
import os
import tempfile
import subprocess
import sys


sequana_path = easydev.get_package_location('sequana_fastqc')
sharedir = os.sep.join([sequana_path , "sequana_pipelines", 'fastqc', 'data'])


# 
def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = "sequana_pipelines_fastqc --input-directory {} "
    cmd += "--working-directory {} --run-mode local --force"
    cmd = cmd.format(sharedir, directory.name)
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()
    import sequana_pipelines.fastqc.main as m
    sys.argv = ["test", "--input-directory", sharedir, "--working-directory",
        directory.name, "--run-mode", "local", "--force"]
    m.main()


def test_full():

    with tempfile.TemporaryDirectory() as directory:
        print(directory)
        wk = directory

        cmd = "sequana_pipelines_fastqc --input-directory {} "
        cmd += "--working-directory {} --run-mode local --force"
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())

        stat = subprocess.call("sh fastqc.sh".split(), cwd=wk)

        assert os.path.exists(wk + "/summary.html")
        assert os.path.exists(wk + "/tree.html")
        assert os.path.exists(wk + "/multiqc/multiqc_report.html")

def test_version():
    cmd = "sequana_pipelines_fastqc --version"
    subprocess.call(cmd.split())

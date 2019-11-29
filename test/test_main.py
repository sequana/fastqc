import easydev
import os
import tempfile
import subprocess
import sys


sequana_path = easydev.get_package_location('sequana_fastqc')
sharedir = os.sep.join([sequana_path , "sequana", 'data'])


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

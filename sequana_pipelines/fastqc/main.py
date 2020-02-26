import sys
import os
import argparse

from sequana.pipelines_common import *
from sequana.snaketools import Module
from sequana import logger
logger.level = "INFO"

col = Colors()

NAME = "fastqc"
m = Module(NAME)
m.is_executable()


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME):
        usage = col.purple(
            """This script prepares the sequana pipeline fastqc layout to
            include the Snakemake pipeline and its configuration file ready to
            use.

            In practice, it copies the config file and the pipeline into a
            directory (fastqc) together with an executable script

            For a local run, use :

                sequana_pipelines_fastqc --input-directory PATH_TO_DATA --run-mode local

            For a run on a SLURM cluster:

                sequana_pipelines_fastqc --input-directory PATH_TO_DATA --run-mode slurm

        """
        )
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        so = InputOptions()
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)


def main(args=None):
    if args is None:
        args = sys.argv

    if "--version" in sys.argv:
        print_version(NAME)
        sys.exit(0)

    options = Options(NAME).parse_args(args[1:])

    manager = PipelineManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    cfg = manager.config.config
    cfg.input_pattern = options.input_pattern
    cfg.input_readtag = options.input_readtag
    cfg.input_directory = os.path.abspath(options.input_directory)

    manager.exists(cfg.input_directory)

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()

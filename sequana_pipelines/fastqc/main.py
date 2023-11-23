#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os

import rich_click as click
import click_completion

click_completion.init()


from sequana_pipetools.options import *
from sequana_pipetools import SequanaManager


NAME = "fastqc"

help = init_click(NAME, groups={
    "Pipeline Specific": [
        "--method", "--skip-multiqc"],
        }
)



@click.command(context_settings=help)
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickInputOptions, add_input_readtag=False)
@include_options_from(ClickGeneralOptions)
@click.option(
    "--method",
    "method",
    default="fastqc",
    type=click.Choice(["fastqc", "falco"]),
    show_default=True,
    help="""Software to be used to perform QC of input data set,
            Standard tool is fastqc (default), but one can use falco, which is 3-4 faster
            and produces same plots""",
)
@click.option(
    "--skip-multiqc",
    is_flag=False,
    help="""It may happen that multiqc requires lots of memory.
        For local run, you may want to switch if off with this flag""",
)
def main(**options):


    # the real stuff is here
    manager = SequanaManager(options, NAME)
    options = manager.options

    # creates the working directory
    manager.setup()

    # Fill the config file with data and specific options
    cfg = manager.config.config
    cfg.input_pattern = options.input_pattern
    cfg.input_directory = os.path.abspath(options.input_directory)
    cfg.multiqc.do = not options.skip_multiqc
    cfg.general.method_choice = options.method

    manager.exists(cfg.input_directory)

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()

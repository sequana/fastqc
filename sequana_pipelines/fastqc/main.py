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
import sys
import os
import argparse
import subprocess

from sequana_pipetools.options import *
from sequana_pipetools.options import before_pipeline
from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog
from sequana_pipetools import SequanaManager

col = Colors()

NAME = "fastqc"


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        so = InputOptions(add_input_readtag=False)
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)


        pipeline_group = self.add_argument_group("sequana_fastqc")
        pipeline_group.add_argument("--method", dest="method",
            default="fastqc", choices=['fastqc', 'falco'], 
            help="""Software to be used to perform QC of input data set,
                Standard tool is fastqc (default), but one can use falco, which is 3-4 faster
                and produces same plots""")
        pipeline_group.add_argument("--skip-multiqc", default=False, action="store_true",
            help="""It may happen that multiqc requires lots of memory. For local
run, you may want to swithc multiqc off with this option""")
        #pipeline_group.add_argument("--data-type", dest="data_type",
        #    default="illumina", choices=['illumina', 'nanopore', 'pacbio', 'mgi', 'others'], 
        #    help="""nanopore, others and pacbio are not paired. The --input-readtag then be ignored""")

        self.add_argument("--run", default=False, action="store_true",
            help="execute the pipeline directly")

    def parse_args(self, *args):
        args_list = list(*args)
        if "--from-project" in args_list:
            if len(args_list)>2:
                msg = "WARNING [sequana]: With --from-project option, " + \
                        "pipeline and data-related options will be ignored."
                print(col.error(msg))
            for action in self._actions:
                if action.required is True:
                    action.required = False
        options = super(Options, self).parse_args(*args)
        return options


def main(args=None):

    if args is None:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])

    # the real stuff is here
    manager = SequanaManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    if options.from_project is None:
        cfg = manager.config.config
        cfg.input_pattern = options.input_pattern
        cfg.input_directory = os.path.abspath(options.input_directory)
        cfg.multiqc.do = not options.skip_multiqc

        cfg.general.method_choice = options.method

        manager.exists(cfg.input_directory)
    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()

    if options.run:
        subprocess.Popen(["sh", '{}.sh'.format(NAME)], cwd=options.workdir)

if __name__ == "__main__":
    main()

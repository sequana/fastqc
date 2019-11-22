import sys
import os
import argparse
import shutil

from sequana.misc import Colors
from sequana.snaketools import SequanaConfig
from sequana import Module

col = Colors()

m = Module("fastqc")
assert m.is_pipeline()
config = SequanaConfig(m.config)


class Options(argparse.ArgumentParser):
    def __init__(self, prog="fastqc"):
        usage = col.purple(
            """This script prepares the sequana pipeline fastqc layout to
            include the Snakemake pipeline and its configuration file ready to
            use.

            In practice, it copies the config file and the pipeline into a
            directory (fastqc) together with an executable script

            For a local run, use :

                sequana_pipelines_fastqc --fastq-directory PATH_TO_DATA --run-mode local

            For a run on a SLURM cluster:

                sequana_pipelines_fastqc --fastq-directory PATH_TO_DATA --run-mode slurm

        """
        )
        super(Options, self).__init__(usage=usage, prog=prog, description="")

        self.add_argument(
            "--jobs",
            dest="jobs",
            default=40,
            help="number of jobs to run at the same time"
        )

        self.add_argument(
            "--slurm-cores-per-job",
            dest="slurm_cores_per_job",
            default=4,
            help="SLURM queue to be used (biomics)",
        )

        self.add_argument(
            "--slurm-queue",
            dest="slurm_queue",
            default="biomics",
            help="SLURM queue to be used (biomics)",
        )
        self.add_argument(
            "--output-directory",
            dest="outdir",
            default="fastqc",
            help="Where to save the FASTQC results (default fastqc/ )",
        )
        self.add_argument(
            "--fastq-directory",
            dest="fastq_directory",
            default=".",
            required=True,
            help="Where to find the FastQ files (default current directory . ) ",
        )
        self.add_argument(
            "--input-pattern",
            dest="input_pattern",
            default="*fastq.gz",
            help="pattern for the input FastQ files (default  *fastq.gz)",
        )
        self.add_argument(
            "--slurm-memory",
            dest="slurm_memory",
            default=4000,
            help="memory in Mb (default 4000)"
        )

        self.add_argument(
            "--run-mode",
            dest="run_mode",
            required=True,
            choices=['local', 'slurm'],
            help="""run_mode can be either 'local' or 'slurm'. Use local to run
                the pipeline locally, otherwise use 'slurm' to run on a cluster 
                with SLURM scheduler"""
        )

        self.add_argument(
            "--force",
            action="store_true",
            help="force the creation of the output directory"
            )



def main(args=None):
    options = Options(prog="fastqc")
    if args is None:
        args = sys.argv

    options = options.parse_args(args[1:])

    jobs = options.jobs
    outdir = options.outdir

    runme = "#!/bin/bash\nsnakemake -s fastqc.rules"

    if options.run_mode == "slurm":
        slurm_queue = "-A {} --qos {} -p {}".format(
            options.slurm_queue,
            options.slurm_queue,
            options.slurm_queue)

        runme += " --cluster sbatch --mem {} -c {} {} ".format(
            options.slurm_memory, 
            options.slurm_cores_per_job, 
            options.slurm_queue)

    runme += " --jobs {}".format(options.jobs)

    if os.path.exists(outdir) is True and options.force is False:
        print(col.failed("Output path {} exists already".format(outdir)))
        sys.exit()
    elif os.path.exists(outdir) is True and options.force is True:
        print(col.warning("Path {} exists already but you set --force to overwrite it".format(outdir)))
    else:
        os.mkdir(outdir)

    # fill the config file with input parameters
    config.config.input_pattern = options.input_pattern
    config.config.input_directory = os.path.abspath(options.fastq_directory)
    config._update_yaml()
    config.save("{}/config.yaml".format(outdir))

    with open("{}/fastqc.sh".format(outdir), "w") as fout:
        fout.write(runme)


    shutil.copy(
        m.snakefile,
        "{}".format(outdir),
    )

    msg = "Check the script in {}/fastq.sh as well as the configuration file in {}/config.yaml.\n"
    print(col.purple(msg.format(outdir, outdir)))

    msg = "Once ready, execute the script fastqc.sh using \n\n\t"
    if options.run_mode == "slurm":
        msg += "cd {}; sbatch fastqc.sh\n\n"
    else:
        msg += "cd {}; sh fastqc.sh\n\n"
    print(col.purple(msg.format(outdir)))



if __name__ == "__main__":
    main()

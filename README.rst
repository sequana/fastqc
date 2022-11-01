
.. image:: https://badge.fury.io/py/sequana-fastqc.svg
     :target: https://pypi.python.org/pypi/sequana_fastqc

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: http://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI

.. image:: https://github.com/sequana/fastqc/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/fastqc/actions/workflows/main.yml



This is is the **fastqc** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet

:Overview: Runs fastqc and multiqc on a set of Sequencing data to produce control quality reports
:Input: A set of FastQ files (paired or single-end) compressed or not
:Output: an HTML file summary.html (individual fastqc reports, mutli-samples report)
:Status: production
:Wiki: https://github.com/sequana/fastqc/wiki
:Documentation: This README file, the Wiki from the github repository (link above) and https://sequana.readthedocs.io
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

sequana_fastqc is based on Python3, just install the package as follows::

    pip install sequana_fastqc --upgrade

You will need third-party software such as fastqc. Please see below for details.

Usage
~~~~~

This command will scan all files ending in .fastq.gz found in the local
directory, create a directory called fastqc/ where a snakemake pipeline is
launched automatically. Depending on the number of files and their sizes, the
process may be long::

    sequana_fastqc --run

To know more about the options (e.g., add a different pattern to restrict the
execution to a subset of the input files, change the output/working directory,
etc)::

    sequana_fastqc --help
    sequana_fastqc --input-directory DATAPATH

This creates a directory **fastqc**. You just need to execute the pipeline::

    cd fastqc
    sh fastqc.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can retrieve the fastqc.rules and config.yaml files and then execute the pipeline yourself with specific parameters::

    snakemake -s fastqc.rules --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Please see the `Wiki <https://github.com/sequana/fastqc/wiki>`_ for more examples and features.

Tutorial
~~~~~~~~

You can retrieve test data from sequana_fastqc (https://github.com/sequana/fastqc) or type::

    wget https://raw.githubusercontent.com/sequana/fastqc/master/sequana_pipelines/fastqc/data/data_R1_001.fastq.gz
    wget https://raw.githubusercontent.com/sequana/fastqc/master/sequana_pipelines/fastqc/data/data_R2_001.fastq.gz

then, prepare the pipeline::

    sequana_fastqc --input-directory .
    cd fastqc
    sh fastq.sh

    # once done, remove temporary files (snakemake and others)
    make clean

Just open the HTML entry called summary.html. A multiqc report is also available. 
You will get expected images such as the following one:

.. image:: https://github.com/sequana/fastqc/blob/main/doc/summary.png?raw=true

Please see the `Wiki <https://github.com/sequana/fastqc/wiki>`_ for more examples and features.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- fastqc
- falco (optional)


For Linux users, we provide singularity images available through within the **damona** project (https://damona.readthedocs.io). 

To mak use of them, initiliase the pipeline with the --use-singularity option and everything should be downloaded
automatically for you, which also guarantees reproducibility::

    sequana_fastqc --input-directory data --use-singularity


.. image:: https://raw.githubusercontent.com/sequana/fastqc/main/sequana_pipelines/fastqc/dag.png


Details
~~~~~~~~~

This pipeline runs fastqc in parallel on the input fastq files (paired or not)
and then execute multiqc. A brief sequana summary report is also produced.
s
You may use falco instead of fastqc. This is experimental but seem to work for
Illumina/FastQ files.

This pipeline has been tested on several hundreds of MiSeq, NextSeq, MiniSeq,
ISeq100, Pacbio runs.

It produces a md5sum of your data. It copes with empty samples. Produces
ready-to-use HTML reports, etc


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/fastqc/main/sequana_pipelines/fastqc/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 

Changelog
~~~~~~~~~
========= ====================================================================
Version   Description
========= ====================================================================
1.6.1     * pin sequana version to 1.4.4 to force usage of new fastqc module
            to fix falco. Updated config documentation.
1.6.0     * Fixed falco output error and use singularity containers
1.5.0     * removed modules completely.
1.4.2     * simplified pipeline (suppress setup and use existing wrapper)
1.4.1     * simplified pipeline with wrappers/rules
1.4.0     * This version uses sequana 0.12.0 and new sequana-wrappers 
            mechanism. Functionalities is unchanged. Also based on
            sequana_pipetools 0.6.X
1.3.0     * add option --skip-multiqc (in case of memory trouble)
          * Fix typo in the link towards fastqc reports in the summary.html
            table
          * Fix number of samples in the paired case (divide by 2)
1.2.0     * compatibility with Sequanix
          * Fix pipeline to cope with new snakemake API
1.1.0     * add new rule to allow users to choose falco software instead of
            fastqc. Note that fastqc is 4 times faster but still a work in
            progress (version 0.1 as of Nov 2020).
          * allows the pipeline to process pacbio files (in fact any files
            accepted by fastqc i.e. SAM and BAM files
          * More doc, test and info on the wiki
1.0.1     * add md5sum of input files as md5.txt file
1.0.0     * a stable version. Added a wiki on github as well and a 
            singularity recipes
0.9.15    * For the HTML reports, takes into account samples with zero reads
0.9.14    * round up some statistics in the main table 
0.9.13    * improve the summary HTML report
0.9.12    * implemented new --from-project option
0.9.11    * now depends on sequana_pipetools instead of sequana.pipelines to 
            speed up --help calls
          * new summary.html report created with pipeline summary
          * new rule (plotting)
0.9.10    * simplify the onsuccess section
0.9.9     * add missing png and pipeline (regression bug)
0.9.8     * add missing multi_config file
0.9.7     * check existence of input directory in main.py
          * add a logo 
          * fix schema
          * add multiqc_config
          * add sequana + sequana_fastqc version
0.9.6     add the readtag option
========= ====================================================================


Contribute & Code of Conduct
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To contribute to this project, please take a look at the 
`Contributing Guidelines <https://github.com/sequana/sequana/blob/master/CONTRIBUTING.rst>`_ first. Please note that this project is released with a 
`Code of Conduct <https://github.com/sequana/sequana/blob/master/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.


This is is the **fastqc** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet

:Overview: Runs fastqc and multiqc on a set of Sequencing data to produce control quality reports
:Input: A set of FastQ files (paired or single-end) compressed or not
:Output: an HTML file summary.html (individual fastqc reports, mutli-samples report)
:Status: production
:Wiki: https://github.com/sequana/sequana_fastqc/wiki
:Documentation: This README file, the Wiki from the github repository (link above) and https://sequana.readthedocs.io
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

You must install Sequana first (use --upgrade to get the latest version installed)::

    pip install sequana --upgrade

Then, just install this package::

    pip install sequana_fastqc --upgrade

Usage
~~~~~

::

    sequana_pipelines_fastqc --help
    sequana_pipelines_fastqc --input-directory DATAPATH

This creates a directory **fastq**. You just need to execute the pipeline::

    cd fastqc
    sh fastqc.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can retrieve the fastqc.rules and config.yaml files and then execute the pipeline yourself with specific parameters::

    snakemake -s fastqc.rules --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Please see the `Wiki <https://github.com/sequana/sequana_fastqc/wiki>`_ for more examples and features.

Tutorial
~~~~~~~~

You can retrieve test data from sequana_fastqc (https://github.com/sequana/sequana_fastqc) or type::

    wget https://raw.githubusercontent.com/sequana/sequana_fastqc/master/sequana_pipelines/fastqc/data/data_R1_001.fastq.gz
    wget https://raw.githubusercontent.com/sequana/sequana_fastqc/master/sequana_pipelines/fastqc/data/data_R2_001.fastq.gz

then, prepare the pipeline::

    sequana_fastqc --input-directory .
    cd fastqc
    sh fastq.sh

    # once done, remove temporary files (snakemake and others)
    make clean

Just open the HTML entry called summary.html. A multiqc report is also available. 
You will get expected images such as the following one:

.. image:: https://github.com/sequana/sequana_fastqc/blob/master/doc/summary.png?raw=true

Please see the `Wiki <https://github.com/sequana/sequana_fastqc/wiki>`_ for more examples and features.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- fastqc

For Linux users, we provide a singularity image available through damona::

    pip install damona
    damona install fastqc
    # and add the ~/.config/damona/bin path to your binary PATH 

.. image:: https://raw.githubusercontent.com/sequana/sequana_fastqc/master/sequana_pipelines/fastqc/dag.png


Details
~~~~~~~~~

This pipeline runs fastqc in parallel on the input fastq files (paired or not)
and then execute multiqc. A brief sequana summary report is also produced.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_fastqc/master/sequana_pipelines/fastqc/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 

Changelog
~~~~~~~~~
========= ====================================================================
Version   Description
========= ====================================================================
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


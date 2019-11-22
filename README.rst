:Overview: fastqc + multiqc 
:Input: A set of FastQ files (paired or single-end) compressed or not
:Output: an HTML file index.html (multiqc) and tree.html (individual fastqc report)

Usage
~~~~~

::

    sequana_pipelines_fastqc --help
    sequana_pipelines_fastqc --fastq-directory DATAPATH --run-mode local
    sequana_pipelines_fastqc --fastq-directory DATAPATH --run-mode slurm

This creates a directory **fastq**. You just need to execute the pipeline::

    cd fastqc
    sh fastqc.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can retrieve the fastqc.rules and config.yaml files and then execute the pipeline yourself with specific parameters::

    snakemake -s fastqc.rules --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipelines requires:

- fastqc
- multiqc
- snakemake

.. include:: requirements.txt

.. image:: https://raw.githubusercontent.com/sequana/sequana_fastqc/master/sequana_pipelines/fastqc/dag.png


Details
~~~~~~~~~

This pipeline runs fastqc in parallel on the input fastq files (paired or not)
and then execute multiqc. A brief sequana summary report is also produced.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is a documented configuration file :download:`../sequana/pipelines/fastqc/config.yaml` to be used with the pipeline. Each rule used in the pipeline may have a section in the
configuration file. 


FastQC
^^^^^^^^^^^
.. snakemakerule:: fastqc_dynamic

mutliqc
^^^^^^^^^^^^^^^
.. snakemakerule:: multiqc2


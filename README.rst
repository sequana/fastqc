
.. image:: https://badge.fury.io/py/sequana-fastqc.svg
     :target: https://pypi.python.org/pypi/sequana_fastqc

.. image:: https://github.com/sequana/fastqc/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/fastqc/actions/workflows/main.yml

.. image:: https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg
    :target: https://pypi.python.org/pypi/sequana
    :alt: Python 3.11 | 3.12

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: http://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI

This is the **fastqc** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet

:Overview: Runs fastqc (or falco) and multiqc on a set of sequencing data to produce quality control reports
:Input: A set of FastQ files (paired or single-end), compressed or not
:Output: An HTML summary report with individual FastQC reports and a multi-sample MultiQC report
:Status: Production
:Documentation: This README file and https://sequana.readthedocs.io
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

If you already have all requirements, you can install the package using pip::

    pip install sequana_fastqc --upgrade

You will need third-party software such as fastqc or falco. Please see below for details.

Usage
~~~~~

Scan FastQ files in a directory and set up the pipeline (replace ``DATAPATH`` with your input directory)::

    sequana_fastqc --input-directory DATAPATH

To use falco instead of fastqc::

    sequana_fastqc --input-directory DATAPATH --method falco

To skip the MultiQC report (useful when memory is limited)::

    sequana_fastqc --input-directory DATAPATH --skip-multiqc

This creates a ``fastqc/`` directory with the pipeline and configuration file. Execute the pipeline locally::

    cd fastqc
    sh fastqc.sh

If you are familiar with Snakemake, you can also run the pipeline directly::

    snakemake -s fastqc.rules --cores 4 --stats stats.txt

See ``.sequana/profile/config.yaml`` to tune Snakemake behaviour (cores, cluster settings, etc.).

Usage with apptainer
~~~~~~~~~~~~~~~~~~~~~

With apptainer, initiate the working directory as follows::

    sequana_fastqc --input-directory DATAPATH --use-apptainer

Images are downloaded in the working directory but you can store them in a shared location::

    sequana_fastqc --input-directory DATAPATH --use-apptainer --apptainer-prefix ~/.sequana/apptainers

and then::

    cd fastqc
    sh fastqc.sh


Requirements
~~~~~~~~~~~~

This pipeline requires the following executables (install via bioconda/conda):

- **fastqc** — quality control tool for sequencing data (default)
- **falco** — faster drop-in replacement for fastqc (optional, ``--method falco``)
- **multiqc** — aggregated HTML report across samples


Install all dependencies at once::

    mamba env create -f environment.yml

.. image:: https://raw.githubusercontent.com/sequana/fastqc/main/sequana_pipelines/fastqc/dag.png


Details
~~~~~~~~~

This pipeline runs fastqc (or falco) in parallel on the input FastQ files, then aggregates results
with MultiQC. A sequana summary report is also produced with per-sample statistics and quality plots.

**QC method** (``--method``):

- ``fastqc`` (default) — standard FastQC; handles FastQ, BAM, and SAM inputs
- ``falco`` — faster alternative; FastQ inputs only

**Optional outputs**:

- MultiQC report (``multiqc/multiqc_report.html``) — enabled by default, disable with ``--skip-multiqc``
- MD5 checksums of all input files (``md5.txt``)
- Tree browser of individual FastQC HTML reports (``tree.html``)

This pipeline has been tested on several hundreds of MiSeq, NextSeq, MiniSeq, ISeq100, and PacBio runs.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/fastqc/main/sequana_pipelines/fastqc/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file.

Changelog
~~~~~~~~~
========= ====================================================================
Version   Description
========= ====================================================================
1.10.0    * Fix --skip-multiqc flag (was is_flag=False, now is_flag=True)
          * Add multiqc_config rule so read_count_multiplier is written
            before multiqc runs (ordering fix)
          * Restore config_file support in multiqc shell command
          * Fix summary image link when multiqc is disabled
          * Fix plotting_and_stats to use its own resources section
          * Fix plotting_and_stats input (log files → declared outputs)
          * Replace assert with raise ValueError in plotting_and_stats
          * Use context manager for open() in onsuccess
          * Extend localrules to dot2svg, md5sum, plotting_and_stats,
            multiqc_config
          * Fix typo: detailled → detailed in HTML report
          * Fix column label: duplicated (%) → unique (%)
          * Remove stale sequana_wrappers version field from config.yaml
          * Fix falco config comment (was copy-pasted from fastqc section)
          * Remove redundant exclude_pattern assignment in main.py
            (SequanaManager handles it automatically)
1.9.0     * Replace wrappers with shell commands via manager.get_shell()
            for falco, fastqc, multiqc, and dot2svg rules
          * rulegraph rule uses manager.get_run() instead of wrapper
1.8.2     * Fix the onerror typo in the pipeline, fix CI.
1.8.1     * update __init__ (version)
1.8.0     * uses pyproject instead of setuptools
          * uses click instead of argparse and newest sequana_pipetools
            (0.16.0)
1.7.1     * Set wrapper version in the config based on new sequana_pipetools
            feature
1.7.0     * Use new rulegraph wrapper and new graphviz apptainer
1.6.2     * slight refactorisation to use rulegraph wrapper
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
`Contributing Guidelines <https://github.com/sequana/sequana/blob/main/CONTRIBUTING.rst>`_ first. Please note that this project is released with a
`Code of Conduct <https://github.com/sequana/sequana/blob/main/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.

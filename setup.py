from setuptools import setup, find_namespace_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess

_MAJOR               = 1
_MINOR               = 6
_MICRO               = 0
version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {"main": ("thomas cokelaer", "thomas.cokelaer@pasteur.fr")},
    'version': version,
    'license' : 'new BSD',
    'url' : "https://github.com/sequana/",
    'description': "A fastqc pipeline from sequana project." ,
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : ['fastqc', 'NGS', 'snakemake', 'multiqc', 'sequana'],
    'classifiers' : [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics']
    }

NAME = "fastqc"

class Install(install):
    def run(self):
        cmd = "sequana_completion --name {} --force ".format(NAME)
        try: subprocess.run(cmd.split())
        except:pass
        install.run(self)

class Develop(develop):
    def run(self):
        cmd = "sequana_completion --name {} --force ".format(NAME)
        try:subprocess.run(cmd.split())
        except:pass
        develop.run(self)

setup(
    name             = "sequana_{}".format(NAME),
    version          = version,
    maintainer       = metainfo['authors']['main'][0],
    maintainer_email = metainfo['authors']['main'][1],
    author           = metainfo['authors']['main'][0],
    author_email     = metainfo['authors']['main'][1],
    long_description = open("README.rst").read(),
    keywords         = metainfo['keywords'],
    description      = metainfo['description'],
    license          = metainfo['license'],
    platforms        = metainfo['platforms'],
    url              = metainfo['url'],
    classifiers      = metainfo['classifiers'],

    # package installation
    packages = ["sequana_pipelines.fastqc"],

    install_requires = open("requirements.txt").read(),

    # This is recursive include of data files
    exclude_package_data = {"": ["__pycache__"]},
    package_data = {
        '': ['*.yaml', "*.rules", "*.json", "requirements.txt", "*png", "*yml", "*smk"]
        },

    zip_safe=False,

    entry_points = {'console_scripts':[
        'sequana_fastqc=sequana_pipelines.fastqc.main:main']
    }

)

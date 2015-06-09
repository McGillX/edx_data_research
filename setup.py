import os

from setuptools import setup, find_packages

import edx_data_research

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Topic :: Software Development :: Libraries :: Python Modules"
]

setup(name = 'McGillX',
      version = edx_data_research.__version__,
      author = edx_data_research.__author__,
      author_email = edx_data_research.__email__,
      description = ("This is a public repository for the tools developed and used by the McGillX research team to package, analyse, and manipulate the data that is collected                         through McGill's online courses offered via the edX platform."),
      license = edx_data_research.__license__,
      packages=find_packages(),
      url = 'https://github.com/McGillX/edx_data_research',
      long_description = read('README.md'),
      keywords = "mcgillx edx analytics mooc data python",
      classifiers = classifiers,
      entry_points = {
        'console_scripts' : ['moocx=edx_data_research.cli.cli:main'],
      },
)

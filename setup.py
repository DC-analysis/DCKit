from os.path import dirname, realpath, exists
from setuptools import setup, find_packages
import sys


author = u"Paul Müller"
authors = [author]
description = 'Graphical toolkit for RT-DC data management'
name = 'dckit'
year = "2019"

sys.path.insert(0, realpath(dirname(__file__))+"/"+name)
from _version import version

setup(
    name=name,
    author=author,
    author_email='dev@craban.de',
    url='https://github.com/ZELLMECHANIK-DRESDEN/DCKit',
    version=version,
    packages=find_packages(),
    package_dir={name: name},
    include_package_data=True,
    license="GPL v3",
    description=description,
    long_description=open('README.rst').read() if exists('README.rst') else '',
    install_requires=["dclab==0.28.0",  # pinned for triaging
                      "h5py>=2.8.0",
                      "imageio[ffmpeg]>=2.8.0",
                      "nptdms>=0.27.0",
                      "numpy",
                      "pyqt5",
                      ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-qt"],
    python_requires='>=3.6, <4',
    entry_points={"gui_scripts" : ['dckit = dckit.__main__:main']},
    keywords=["RT-DC", "deformability", "cytometry", "zellmechanik"],
    classifiers= ['Operating System :: OS Independent',
                  'Programming Language :: Python :: 3',
                  'Intended Audience :: Science/Research',
                  ],
    platforms=['ALL']
    )

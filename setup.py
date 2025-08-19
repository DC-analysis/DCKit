from os.path import dirname, realpath, exists
from setuptools import setup, find_packages
import sys


author = u"Paul Müller"
authors = [author]
description = 'Graphical toolkit for RT-DC data management'
name = 'dckit'
year = "2019"

sys.path.insert(0, realpath(dirname(__file__))+"/"+name)
from _version import version  # noqa: E402

setup(
    name=name,
    author=author,
    author_email='dev@craban.de',
    url='https://github.com/DC-analysis/DCKit',
    version=version,
    packages=find_packages(),
    package_dir={name: name},
    include_package_data=True,
    license="GPL-3.0-or-later",
    description=description,
    long_description=open('README.rst').read() if exists('README.rst') else '',
    install_requires=["dclab[tdms]>=0.67.0",
                      "h5py>=3.9.0",
                      "imageio[ffmpeg]",
                      "nptdms>=0.27.0",
                      "numpy>=1.21",
                      "pyqt5",
                      ],
    python_requires='>=3.10, <4',
    entry_points={"gui_scripts": ['dckit = dckit.__main__:main']},
    keywords=["RT-DC", "deformability", "cytometry", "zellmechanik"],
    classifiers=['Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 'Intended Audience :: Science/Research',
                 ],
    platforms=['ALL']
)

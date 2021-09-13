#!/usr/bin/env python3
# -*- coding: latin-1 -*-
import re
import os
import io
from setuptools import setup


def open_local(paths, mode="r", encoding="utf8"):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), *paths)
    return io.open(path, mode, encoding=encoding)


with open_local(["owlrl", "__init__.py"], encoding="utf-8") as fp:
    try:
        version = re.findall(r'^__version__ = "([^"]+)"\r?$', fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

with open_local(["README.rst"]) as readme:
    long_description = readme.read()

with open_local(["requirements.txt"]) as req:
    found_requirements = req.read().split("\n")
    dependency_links = []
    requirements = []
    for f in found_requirements:
        if "git+" in f:
            pkg = f.split("#")[-1]
            dependency_links.append(f.strip() + "-9876543210")
            requirements.append(pkg.replace("egg=", "").rstrip())
        else:
            requirements.append(f.strip())

setup(
    name="owlrl",
    packages=["owlrl"],
    scripts=["scripts/owlrl", "scripts/RDFConvertService"],
    package_dir={"owlrl": "./owlrl"},
    version=version,
    description="OWL-RL and RDFS based RDF Closure inferencing for Python",
    author="Ivan Herman",
    author_email="ivan@ivan-herman.net",
    maintainer="Nicholas Car",
    maintainer_email="nicholas.car@csiro.au",
    url="https://github.com/RDFLib/OWL-RL/",
    download_url="https://github.com/RDFLib/OWL-RL/"
    "archive/v{:s}.tar.gz".format(version),
    license="LICENSE.txt",
    keywords=[
        "Linked Data",
        "Semantic Web",
        "Python",
        "triples",
        "inferencing",
        "RDF",
        "OWL",
        "OWL-RL",
        "owlrl",
        "RDFS",
    ],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: W3C License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    tests_require=["pytest"] + requirements,
    dependency_links=dependency_links,
)

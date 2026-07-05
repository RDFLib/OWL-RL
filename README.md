[![Original Author DOI](https://zenodo.org/badge/9385/RDFLib/OWL-RL.svg)](http://dx.doi.org/10.5281/zenodo.14543)
[![PyPI badge](https://badge.fury.io/py/owlrl.svg)](https://badge.fury.io/py/owlrl)

[![OWL-RL Logo](https://raw.githubusercontent.com/RDFLib/OWL-RL/master/OWL-RL.png)](http://owl-rl.readthedocs.io/)

# OWL-RL

* [Installation](#installation)
* [Use](#use)
* [License](#license)
* [Support & Contacts](#support--contacts)
* [Development](#development)

A simple implementation of the OWL2 RL Profile, as well as a basic RDFS inference, on top of [RDFLib](https://github.com/RDFLib/rdflib), based on forward-chaining.

## Installation

This package requires RDFLib 7.6.0 or newer. It can be installed from the Python Package Index in the usual way:

```sh
pip install owlrl
```

or

```sh
poetry add owlrl
```

Optional: run the closure against an [Oxigraph](https://pyoxigraph.readthedocs.io/) in-memory store by installing the extra:

```sh
pip install "owlrl[oxigraph]"
```

## Use

This package can run inference according to RDFS and/or OWL-RL.

For details on RDFS, see the [RDF Semantics Specification](http://www.w3.org/TR/rdf11-mt/); for OWL 2 RL, see the [OWL 2 Profile specification](http://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules).

View the **OWL-RL documentation** online:

<http://owl-rl.readthedocs.io/>

### Scripts

This Python package contains a couple of Command Line scripts:

- `scripts/RDFConvertService`: a CGI script to invoke the library
    - It may have to be adapted to the local server setup.

- `scripts/owlrl`: a script that can be run locally to transform a file into RDF (on the standard output)
    - Run the script with `-h` to get the available flags.

### Oxigraph store (optional)

After installing the `oxigraph` extra (see **Installation** above), you may pass a [PyOxigraph](https://pyoxigraph.readthedocs.io/) `Store` into `owlrl.DeductiveClosure(...).expand(...)` and related closure entry points wherever you would normally pass an RDFLib `Graph` or `Dataset`. Inferred triples can still be written to a separate named graph on that store via the `destination` argument, as with RDFLib.

This integration is provided for **compatibility** (for example, keeping the rest of an application on Oxigraph) rather than for speed. Converting terms to and from RDFLib objects removes most of the performance benefit of Oxigraph, and this project still uses RDFLib types and logic internally for all inference steps.

## License

This software is released under the W3C© SOFTWARE NOTICE AND LICENSE. See [LICENSE.txt](LICENSE.txt).

## Support & Contacts

Please follow the instructions for Support and Contact as given for the RDFLib package:

* <https://github.com/RDFLib/rdflib#support--contacts>

## Development

### Changes

To view the changelog for this software package, see [CHANGELOG.rst](CHANGELOG.rst).

### Release Procedure

- ensure all tests pass: `pytest`
- update all the version numbers
  - `pyproject.toml`
  - `README.rst`
- remove the current `dist/` directory
- build the new distribution
- test the metadata rendering
- test pushing it to PyPI
- actually push it to PyPI

```sh
pytest
rm -vf dist/*
poetry build
bsdtar -xvf dist/owlrl-*.whl -O '*/METADATA' | view -
bsdtar -xvf dist/owlrl-*.tar.gz -O '*/PKG-INFO' | view -

poetry publish --dry-run
poetry publish -u __token__ -p <OWL-RL PyPI Token>
```

- commit the version update
- tag it
- push the commits and tag to GitHub
- make a GitHub release
  - reuse the CHANGELOG entry for the release
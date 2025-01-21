|Original Author DOI| |PyPI badge|

|OWL-RL Logo|

.. |Original Author DOI| image:: https://zenodo.org/badge/9385/RDFLib/OWL-RL.svg
    :target: http://dx.doi.org/10.5281/zenodo.14543

.. |PyPI badge| image:: https://badge.fury.io/py/owlrl.svg
    :target: https://badge.fury.io/py/owlrl

.. |OWL-RL Logo| image:: https://raw.githubusercontent.com/RDFLib/OWL-RL/master/OWL-RL.png
    :width: 250
    :target: http://owl-rl.readthedocs.io/


OWL-RL
======

A simple implementation of the OWL2 RL Profile, as well as a basic RDFS inference, on top of RDFLib, based on forward chaining.

This package is a Python library that also contains a couple of scripts:

* `scripts/RDFConvertService`: a CGI script to invoke the library. It may have to be adapted to the local server setup.

* `scripts/owlrl`: a script that can be run locally on to transform a file into RDF (on the standard output). Run the script with `-h` to get the available flags.

Installation
------------

This package requires RDFLib 7.1.3 as its only dependency and it can be installed from the Python Package index in the usual way:

::

    pip install owlrl


or

::

    poetry add owlrl


Use
---

This package can run inference according to RDFS and/or OWL-RL.

For details on RDFS, see the `RDF Semantics Specification`_; for OWL 2 RL, see the `OWL 2 Profile specification`_.

.. _RDF Semantics Specification: http://www.w3.org/TR/rdf11-mt/
.. _OWL 2 Profile specification: http://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules

View the **OWL-RL documentation** online: http://owl-rl.readthedocs.io/


License
-------
This software is released under the W3C© SOFTWARE NOTICE AND LICENSE. See `LICENSE.txt <LICENSE.txt>`_.


Support & Contacts
------------------

For general "how do I..." queries, please use https://stackoverflow.com and tag your question with ``rdflib``. Existing questions:

* https://stackoverflow.com/questions/tagged/rdflib

If you want to contact the rdflib maintainers, please do so via:

* the rdflib-dev mailing list: https://groups.google.com/group/rdflib-dev
* the chat, which is available at `gitter <https://gitter.im/RDFLib/rdflib>`_ or via matrix `#RDFLib_rdflib:gitter.im <https://matrix.to/#/#RDFLib_rdflib:gitter.im>`_


Development
-----------

Changes
~~~~~~~

To view the changelog for this software library, see `CHANGELOG.rst <CHANGELOG.rst>`_.

Release Procedure
~~~~~~~~~~~~~~~~~

* update all the version numbers

    * pyproject.toml
    * README.rst

* remove the current ``dist/`` dir
* build the new distribution
* test the metadata rendering
* test push it to PyPI
* actually push it to PyPI

::

    rm -vf dist/*
    poetry build
    bsdtar -xvf dist/owlrl-*.whl -O '*/METADATA' | view -
    bsdtar -xvf dist/owlrl-*.tar.gz -O '*/PKG-INFO' | view -

    poetry publish --dry-run
    poetry publish -u __token__ -p <OWL-RL PyPI Token>

* commit the version update
* tag it
* push the commits & tag to GitHub
* make a GitHub release

    * reuse the CHANGELOG entry for the release

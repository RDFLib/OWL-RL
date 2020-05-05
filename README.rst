|Original Author DOI| |PyPI badge|

|OWL-RL Logo|

.. |Original Author DOI| image:: https://zenodo.org/badge/9385/RDFLib/OWL-RL.svg
    :target: http://dx.doi.org/10.5281/zenodo.14543

.. |PyPI badge| image:: https://badge.fury.io/py/owlrl.svg
    :target: https://badge.fury.io/py/owlrl

.. |OWL-RL Logo| image:: OWL-RL-250.png
    :target: http://owl-rl.readthedocs.io/


OWL-RL
======

A simple implementation of the OWL2 RL Profile, as well as a basic RDFS inference, on top of RDFLib. Based mechanical forward chaining. The distribution contains:

**OWL-RL**: the Python library. You should copy the directory somewhere into your :code:`PYTHONPATH`. Alternatively, you can also run the :code:`python setup.py install` script in the directory.

* :code:`scripts/RDFConvertService`: can be used as a CGI script to invoke the library. It may have to be adapted to the local server setup.

* :code:`scripts/owlrl`: script that can be run locally on to transform a file into RDF (on the standard output). Run the script with :code:`-h` to get the available flags.

The package requires Python version 3.5 or higher; it depends on `RDFLib`_; version 4.2.2 or higher is required. If you need the python 2.7.x compatible version, see the @/py2 branch in this repository.

.. _RDFLib: https://github.com/RDFLib

For the details on RDFS, see the `RDF Semantics Specification`_; for OWL 2 RL, see the `OWL 2 Profile specification`_.

.. _RDF Semantics Specification: http://www.w3.org/TR/rdf11-mt/
.. _OWL 2 Profile specification: http://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules

View the **OWL-RL documentation** online: http://owl-rl.readthedocs.io/

To view the changelog for this software library, see `CHANGELOG.rst <CHANGELOG.rst>`_.

This software is released under the W3C© SOFTWARE NOTICE AND LICENSE. See `LICENSE.txt <LICENSE.txt>`_.

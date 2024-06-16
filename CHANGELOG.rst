Changelog
---------

v.6.0.2 - October, 2021
~~~~~~~~~~~~~~~~~~~~~~~
Changes:

* works with rdflib >= 6.2.0
* replaces owl namespace element lists with those of rdflib (OWL, RDF, RDFS, XSD)

v5.2.3
~~~~~~

Changes:

* fix README image display
* fix version acquisition in setup.py

v5.2.2
~~~~~~

Changes:

* Depend on RDFLib v5.0+

* Removed rdflib_jsonld as a requirement. It is included in rdflib 6.0

* Detect if rdflib 6.0 is in use, and do not import the jsonld module


v5.2.1
~~~~~~

Changes:

* Added stdeb.cfg file, and notes in requirements-dev.txt for building a debian package

* Removed the .py extension from the files in the scripts directory

* Same change as above but for the RDFConvertService script

* Fix Qualified Max Cardinality 0 Bug

* Fix output printing of owlrl commandline script


v5.2.0
~~~~~~

Changes:

* Dropped LiteralProxies finally. Processing of literals is no longer done through a LiteralProxy class (thanks :code:`@wrobell`)

  * As a consequence:

  * The change improves performance of the library by about 14%.

  * Related blocks of code, which swallow exceptions are removed.

* Unit tests for the following OWL 2 RL rules are implemented
    cax-dw,
    cls-avf,
    cls-maxc1,
    cls-maxc2,
    cls-maxqc1,
    cls-maxqc2,
    cls-maxqc3,
    cls-maxqc4

* Unit tests for RDFS closure implemented
    adding datatype axioms,
    one time rules

* Unit tests for OWL 2 RL extras closure implemented
    one time rules


v5.1.1
~~~~~~

Changes:

* Renamed script: :code:`closure.py` to :code:`owlrl.py`

* Fixed a deployment bug which caused the shebang to be rewritten incorrectly in the owlrl.py script.


v5.1.0
~~~~~~

Changes:

* Rename module from RDFClosure to owlrl

* Published on PyPI!

* Fixed bugs caused by python3 automatic conversion (like :code:`range` being a variabe, not a function)

* Added some basic tests (more tests coming!)

* Started foundational work to remove :code:`LiteralProxies` in the future (thanks :code:`@wrobell`)

* Simplified some sections of the code (thanks :code:`@wrobell`)



Version 5.0.0
~~~~~~~~~~~~~

Changes:

* Port to Python3. Minimum recommended version is now Python v3.5.

* Fixed a bug where the inferencing process would crash if the engine encountered a literal node that has a datatype for which it does not have a hardcoded converter.



Version 4/5
~~~~~~~~~~~

This is a major release: the package has been updated to Python 2.7 and RDFLib 4 (and to Python 3.5 in v5.0.0).

Some important changes:

* The local parser and serializer implementations have been removed; the package relies fully on RDFLib.

* If the extra JSON-LD parser and serializer is available, that format may also be used both for input and output.

* RDFa as a possible input format has been added.

* The datatype part has been reworked to adapt itself to the way RDFLib handles datatypes.

* The :code:`Literal` class has been adapted to the latest versions of RDFLib's :code:`Literal` (there is no :code:`cmp_value` any more, only value)

* Python 2.7 includes an implementation for rational numbers (under the name :code:`Fraction`), so the separate module became moot.

* The :code:`script` directory has been moved to the top level of the distribution.

* The RDF1.1 specific datatypes (:code:`LangString` and :code:`HTML`) have been added, although the :code:`HTML`  is simply treated as a text (a reliance on the HTML5 Library may be too much for what this is worth…)

* The :code:`closure` script has now an extra flag (:code:`-m`) to use the "maximal" entailment, i.e., extended OWLRL+RDF with extra trimmings.


Version 4.2.1
~~~~~~~~~~~~~

Changes:

* Per error report of Michael Schneider: if a class name is a blank node, the XML serialization went wrong. In case of exception, the fall back is to use the pure xml rather than the pretty xml; that works. There was also a 'trimming' argument missing in case of a pure format conversion that led to an exception, that is handled, too.

Version 4.2
~~~~~~~~~~~

Changes:

* I exchanged rdflib Graph usage to rdflib ConjunctiveGraph. It avoids issues around deprecation and is also a possible entry point for named graphs.

* Added an extra check in the allValuesFrom handling for datatype restrictions. This does not affect pure OWLRL but is used by the extras that implement facets.

* The RestrictedDatatype class has now a 'Core' superclass; this can be used by other restricted datatypes that are not necessarily defined in OWL 2

Version 4.1
~~~~~~~~~~~

Changes:

* On advise from Dominique, the error message in the CGI script uses cgi.escape on the text input before displaying it.

* 'Trimming' has been added to the command line options

* Adaptation to rdflib 2.4.2 (or even 2.4.1?): the :code:`Literal._PythonToXSD` changed its structure from a dictionary to a list of tuples; :code:`DatatypeHandling.use_Alt_lexical_conversions()` had to change.

Version 4.0
~~~~~~~~~~~

Changes:

* The top level :code:`__init__` file has been reorganized, so that the package can be used as a module for applications in RDFLib. There is a top level class (:code:`DeductiveClosure`) that can be invoked from an RDFLib application and the old entry point (:code:`convert_graph`) relies on that.

* New class have been added to cover a combined RDFS + OWL 2 RL closure (Michael Schneider's idea).

* An extension mechanism has been built in from bottom up; user can define his/her own rules via an extension class that is given as a parameter to the core closure class.

* Using the extension mechanism a separate OWLRLExtras module has been added to implement, eg, self restriction, rational datatype.

* In the closure class the array of temporarily stored tuples has been exchanged against a set; in other words, checking whether the tuple is to be stored already is now done by the built-in set operation. It became much faster...

* The input argument has changed from 'source' to 'sources'; ie, several input files can be given to the service at the same time (eg, a separate URI for the data and the ontology, respectively).

* Added the implementation of owl:imports.

* Added an implemenatation for the datatype restrictions.

* Bugs:
    * there was an optimization in the datatype handling of OWLRL that excluded subsumptions for 'implicit' literals, ie, literals that are given datatypes via the ^^ formalism (and not via sameAs and explicit datatype definitions). But this excluded proper inferences for existential restrictions...:-(

* handler for the :code:`xsd:normalizedString` datatype was missing.

Version 3.2
~~~~~~~~~~~

Note: this version passes the full batch of official OWL Full/RL tests uploaded by Michael Schneider to the OWL Working Group site. The difference, in this respect, between this version and version 3.1 is the handling of datatypes (which was only rudimentary in 3.1)

* Bugs:
    * the rules on dt-diff/dt-eq were missing in the implementation. (My mistake: I did not realize that ( owl:sameAs "adfa") was a possible setups whereby those rules do come in even in practice, so I did not implement them thinking that the results would not appear in the final code anyway due to a literal appearing in a subject position. Clearly an error in judgement.)

    * :code:`PlainLiteral` was in a wrong namespace in the OWLRL file:-(

    * Added an explicit handling for virtually all data types, to check the lexical values. (This is, in fact, a RDFLib deficiency for most cases, except those that came in via OWL, like PlainLiteral...)

    * Added a note referring to a Turtle parser bug...

Version 3.1
~~~~~~~~~~~

Note: this version passes the first, basic batch of official OWL Full/RL tests uploaded by Michael Schneider to the OWL Working Group site.

* Bugs:
    * if the URI of a predicate did not correspond to a defined namespace, the extra namespace declaration did not appear in the pretty xml output. Typical situation: the user defines a namespace without trailing '#' or '/', but uses the prefix nevertheless; this ends up in a URI for, say, a predicate or a type that cannot be represented in XML. The proper approach is then to add a new prefix with 'http://' and use that in the output.

    The original XML serialization of RDFLib does that; the PrettyXMLSerialization did not. The pretty XML serialization is based on the one of RDFLib, and has therefore inherited this bug.

    * the axiomatic expression for (byte subclass short) was misspelled to (byte subclass byte)

    * the axiomatic triples added automatically should say (Thing type :code:`owl:Class`) (and not :code:`rdfs:Class` as before). Also, (Nothing type :code:`owl:Class`) was missing there.

    * :code:`rdf:text` changed to :code:`rdf:PlainLiteral` (in the axiomatic triples), as a result of the OWL WG on changing the name.

    * missing subclass relationship for dateTimeStamp vs dateTime.

    * there was an optimization that added Datatype triples only for those datatypes that appeared as part of a literal in the input graph. However, the rule set requires those triples to be added no matter what. At the moment, this is pending (there are discussions in the group on this).

    * the set of triples declaring annotation properties were missing

    * error message for asymmetric properties was bogus (has :code:`%p` instead of :code:`%s` in the text).

    * there was a leftover error message via exceptions for :code:`owl:Nothing` check.

    * rule :code:`scm-eqc2` was missing :-(

* New Features:
    * added some support to booleans; essentially introducing a stronger check (according to XSD the :code:`"111"^xsd:boolean` is not a valid boolean values, though RDFLib accepts it as such...).

    * triples with a bnode predicate were systematically filtered out when added to a graph. However, incoming ontologies may include statements like '[ owl:inverseOf P]', and processing those through the rule set requires to allow such triples during deduction. Lucklily RDFLib is relaxed on that. So such 'generalized' triples are now allowed during the forward chaining and are filtered out only once, right before serialization.

    * some improvements on the datatype handling:
        * adding type relationships to super(data)types. For example, if the original graph includes (:code:`<B> rdf:type xsd:short`), then the triple (:code:`<B> rdf:type xsd:integer`), etc, is also added. As an optimization the (:code:`xsd:short rdfs:subClassOf xsd:integer`) triples are not added, but the direct datatyping is done instead.
        * adding disjointness information on datatypes on top of the hierarchy. This means that inconsistencies of the sort :code:`<B> ex:prop 123 . <B> ex:prop "1"^^xsd:boolean`. will be detected (integers and booleans must be disjoing per XSD; the explicit type relationships and the disjointness of some data types will trigger the necessary rules).

    Note that, mainly the first rule, is really useful when generic nodes are used as datatypes, as opposed to explicit literals.

    * added the possibility to set the input format explicitly, and changed the RDFConvert script accordingly (the service is not yet changed...).

    * added the possibility to consume standard input.

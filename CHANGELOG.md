# Changelog

## v7.6.1 — July 2026

- moved to Markdown documentation
- updates some small aspects of the README

## v7.6.0 — July 2026

### Changes

- Support for Oxigraph as a store
- Increased RDFLib dependency to 7.6.0+

## v7.1.4 — July 2025

### Changes

- Dependency updates to support RDFLib 7.1.4
- Python 3.9+ only, matching RDFLib 7.1.4
- Updated and tested development dependencies

## v7.1.3 — January 2025

### Changes

- Dependency updates for RDFLib 7.1.3
- Development dependencies updated for Python 3.8.1+
- Updated README with contact information and installation instructions

## v7.1.2 — October 2024

### Changes

- Changed Python requirement to >3.8 (instead of >3.10) for compatibility with other RDFLib packages

## v7.1.1 — October 2024

### Changes

- Works with RDFLib >= 7.1.1

This version updates the RDFLib dependency to reduce upstream dependency constraints. It also includes several major functional improvements:

- [Better handling of detecting identical literals for RDFS `sameAs` rules](https://github.com/RDFLib/OWL-RL/pull/68)
- [Allow OWL-RL closures to run on RDFLib `Dataset` instances](https://github.com/RDFLib/OWL-RL/pull/69)
- [Add inferred triples to a separate named graph](https://github.com/RDFLib/OWL-RL/pull/70)

The primary outcome of these changes is that OWL-RL can now be run on a `Graph` within a `Dataset`, while storing inferred triples in a separate graph. This allows asserted and inferred data to coexist cleanly while being managed independently.

This update is particularly important for tools such as [pySHACL](https://github.com/RDFLib/pySHACL).

---

## v6.0.2 — October 2021

### Changes

- Works with RDFLib >= 6.2.0
- Replaced local OWL namespace element lists with those provided by RDFLib (`OWL`, `RDF`, `RDFS`, `XSD`)

## v5.2.3

### Changes

- Fixed README image display
- Fixed version acquisition in `setup.py`

## v5.2.2

### Changes

- Require RDFLib 5.0+
- Removed `rdflib_jsonld` as a dependency (included in RDFLib 6.0)
- Detect RDFLib 6.0 and avoid importing the `jsonld` module

## v5.2.1

### Changes

- Added `stdeb.cfg` and Debian packaging notes to `requirements-dev.txt`
- Removed the `.py` extension from files in the `scripts` directory
- Applied the same change to `RDFConvertService`
- Fixed qualified maximum cardinality 0 bug
- Fixed output printing in the `owlrl` command-line script

## v5.2.0

### Changes

- Removed `LiteralProxies` (thanks `@wrobell`)
  - Improved library performance by approximately 14%
  - Removed related exception-swallowing code
- Added unit tests for the following OWL 2 RL rules:
  - `cax-dw`
  - `cls-avf`
  - `cls-maxc1`
  - `cls-maxc2`
  - `cls-maxqc1`
  - `cls-maxqc2`
  - `cls-maxqc3`
  - `cls-maxqc4`
- Added unit tests for the RDFS closure:
  - Datatype axioms
  - One-time rules
- Added unit tests for the OWL 2 RL Extras closure:
  - One-time rules

## v5.1.1

### Changes

- Renamed `closure.py` to `owlrl.py`
- Fixed a deployment bug that caused the shebang in `owlrl.py` to be rewritten incorrectly

## v5.1.0

### Changes

- Renamed the module from `RDFClosure` to `owlrl`
- Published on PyPI
- Fixed Python 3 conversion issues (such as `range`)
- Added initial test suite
- Began work to remove `LiteralProxies` (thanks `@wrobell`)
- Simplified several parts of the codebase (thanks `@wrobell`)

## v5.0.0

### Changes

- Ported to Python 3 (minimum recommended version: Python 3.5)
- Fixed a crash when inferencing encountered literals with unsupported datatypes

## v4/5

This major release updated the package to Python 2.7 and RDFLib 4 (and Python 3.5 in v5.0.0).

### Highlights

- Removed bundled parsers and serializers in favor of RDFLib
- Added JSON-LD support when the optional parser/serializer is installed
- Added RDFa input support
- Reworked datatype handling to match RDFLib
- Updated the `Literal` implementation for newer RDFLib versions
- Removed the standalone rational number module in favor of Python's `Fraction`
- Moved the `script` directory to the top level
- Added RDF 1.1 datatypes (`LangString` and `HTML`)
- Added the `-m` flag to the `closure` script for maximal entailment

## v4.2.1

### Changes

- Fixed XML serialization when class names are blank nodes
- Added fallback to plain XML serialization
- Fixed missing `trimming` argument during format conversion

## v4.2

### Changes

- Replaced `Graph` with `ConjunctiveGraph`
- Improved `allValuesFrom` handling for datatype restrictions
- Introduced a `Core` superclass for `RestrictedDatatype`

## v4.1

### Changes

- Escaped CGI error output using `cgi.escape`
- Added `trimming` command-line option
- Updated datatype handling for RDFLib 2.4.x changes

## v4.0

### Changes

- Reorganized the package API around `DeductiveClosure`
- Added combined RDFS + OWL 2 RL closure support
- Added extension mechanism for custom rule sets
- Added the `OWLRLExtras` module
- Replaced temporary tuple arrays with sets for improved performance
- Changed `source` to `sources` to allow multiple inputs
- Added support for `owl:imports`
- Added datatype restriction support

### Bug Fixes

- Fixed datatype subsumption handling for implicitly typed literals
- Added missing handler for `xsd:normalizedString`

## v3.2

This version passes the complete official OWL Full/RL test suite contributed by Michael Schneider.

### Bug Fixes

- Implemented missing `dt-diff` and `dt-eq` rules
- Corrected the namespace for `PlainLiteral`
- Added lexical validation for nearly all datatypes
- Added a note about a Turtle parser bug

## v3.1

This version passes the initial official OWL Full/RL test suite.

### Bug Fixes

- Fixed namespace declarations in Pretty XML serialization
- Corrected `byte subclass short` axiom
- Corrected axiomatic triples for `owl:Thing` and `owl:Nothing`
- Updated `rdf:text` to `rdf:PlainLiteral`
- Added missing subclass relationship for `dateTimeStamp`
- Fixed datatype axiom generation
- Added missing annotation property declarations
- Corrected asymmetric property error message
- Removed leftover `owl:Nothing` exception
- Added missing `scm-eqc2` rule

### New Features

- Improved boolean datatype validation
- Allowed generalized triples with blank-node predicates during reasoning
- Improved datatype reasoning by:
  - Adding inferred super-datatype relationships
  - Adding datatype disjointness information
- Added explicit input format selection
- Added support for reading from standard input
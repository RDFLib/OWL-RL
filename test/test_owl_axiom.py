#!/usr/bin/env python3

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

"""
This file tests behaviors of owl:Axioms.

The OWL-RDF mapping [2], Table 7 row 7, would match the introduction
pattern pertaining to EX.NamedAxiom with a Class Declaration, EXCEPT the
axiom's identifier is an IRI instead of a blank node.  The document only
defines behaviors for `owl:Axiom`s identifying as blank nodes.  Given
this pattern non-match, the RDF graph will contain these triples after
the mapping process of [2] Section 3 should have emptied the RDF graph.

The requirement at the end of [2] Section 3, "At the end of this
process, the graph G MUST be empty." fails, meaning [1] Section 2.1's
requirement "conformant OWL 2 tools that take ontology documents as
input(s) MUST accept ontology documents using the RDF/XML serialization"
fails, placing the graph into OWL 2 FULL and providing no behaviors for
or against constructing a class declaration.

[1] https://www.w3.org/TR/2012/REC-owl2-conformance-20121211/
[2] https://www.w3.org/TR/2012/REC-owl2-mapping-to-rdf-20121211/
"""

import logging
from pathlib import Path

import owlrl
import pytest
from rdflib import BNode, Graph, Namespace
from rdflib.namespace import OWL, RDF

EX = Namespace("http://example.org/")
RELS = Namespace("http://example.org/relatives#")

def _test_owl_axiom(include_named_axiom: bool) -> None:
    """
    Test whether an axiom written only as an owl:Axiom is an asserted axiom.
    """
    g = Graph()
    relatives_ttl_path = Path(__file__).parent / "relatives.ttl"
    g.parse(str(relatives_ttl_path), format="turtle")

    # Define three individuals - "Max", but in three ways.

    # First, Max, directly asserted.
    g.add((EX.MaxByAssertion, RDF.type, RELS.Person))

    # Second, Max, not directly asserted, but would be asserted if this blank-node axiom were not reified.
    # NOTE - [2] Table 7 row 7 matches this pattern with a Class Declaration.
    ax = BNode()
    g.add((ax, RDF.type, OWL.Axiom))
    g.add((ax, OWL.annotatedSource, EX.MaxByBlankAxiom))
    g.add((ax, OWL.annotatedProperty, RDF.type))
    g.add((ax, OWL.annotatedTarget, RELS.Person))

    if include_named_axiom:
        # Third, Max, not directly asserted, but would be asserted if this named axiom were not reified.
        # NOTE - [2] Table 7 row 7 does not match this pattern with a Class Declaration.
        g.add((EX.NamedAxiom, RDF.type, OWL.Axiom))
        g.add((EX.NamedAxiom, OWL.annotatedSource, EX.MaxByNamedAxiom))
        g.add((EX.NamedAxiom, OWL.annotatedProperty, RDF.type))
        g.add((EX.NamedAxiom, OWL.annotatedTarget, RELS.Person))

    # Before defining and expanding closure, confirm the direct and both reified Maxes are, are not, and are not in the graph, respectively.
    assert (EX.MaxByAssertion, RDF.type, RELS.Person) in g
    assert not (EX.MaxByBlankAxiom, RDF.type, RELS.Person) in g
    assert not (EX.MaxByNamedAxiom, RDF.type, RELS.Person) in g

    try:
        owlrl.DeductiveClosure(owlrl.OWLRL_Extension).expand(g)
    except:
        if include_named_axiom:
            pytest.xfail("The OWL 2 RL closure correctly rejected an IRI-identified owl:Axiom.")
        else:
            raise

    if include_named_axiom:
        assert False, "The OWL 2 RL closure should have rejected an IRI-identified owl:Axiom."

    # After defining and expanding closure, confirm the direct and reified Maxes are in the graph according to [2].
    assert (EX.MaxByAssertion, RDF.type, RELS.Person) in g
    assert (EX.MaxByBlankAxiom, RDF.type, RELS.Person) in g


def test_owl_axiom_blank() -> None:
    _test_owl_axiom(False)


def test_owl_axiom_iri() -> None:
    _test_owl_axiom(True)

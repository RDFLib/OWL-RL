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

from pathlib import Path

import owlrl
from rdflib import BNode, Graph, Namespace
from rdflib.namespace import OWL, RDF

EX = Namespace("http://example.org/")
RELS = Namespace("http://example.org/relatives#")

def test_owl_axiom() -> None:
    """
    Test whether an axiom written only as an owl:Axiom is an asserted axiom.

    https://www.w3.org/TR/2012/REC-owl2-mapping-to-rdf-20121211/
    Table: 7, row 7
    """
    g = Graph()
    relatives_ttl_path = Path(__file__).parent / "relatives.ttl"
    g.parse(str(relatives_ttl_path), format="turtle")

    # Define three individuals - "Max", but in three ways.

    # First, Max, directly asserted.
    g.add((EX.MaxByAssertion, RDF.type, RELS.Person))

    # Second, Max, not directly asserted, but would be asserted if this blank-node axiom were not reified.
    # NOTE - The OWL-RDF mapping, Table 7 row 7, matches this pattern with a Class Declaration.
    ax = BNode()
    g.add((ax, RDF.type, OWL.Axiom))
    g.add((ax, OWL.annotatedSource, EX.MaxByBlankAxiom))
    g.add((ax, OWL.annotatedProperty, RDF.type))
    g.add((ax, OWL.annotatedTarget, RELS.Person))

    # Third, Max, not directly asserted, but would be asserted if this named axiom were not reified.
    # NOTE - The OWL-RDF mapping, Table 7 row 7, matches this pattern with a Class Declaration, EXCEPT the node is an IRI instead of a blank node.  This may be undefined behavior.
    g.add((EX.NamedAxiom, RDF.type, OWL.Axiom))
    g.add((EX.NamedAxiom, OWL.annotatedSource, EX.MaxByNamedAxiom))
    g.add((EX.NamedAxiom, OWL.annotatedProperty, RDF.type))
    g.add((EX.NamedAxiom, OWL.annotatedTarget, RELS.Person))

    # Before defining and expanding closure, confirm the direct and both reified Maxes are, are not, and are not in the graph, respectively.
    assert (EX.MaxByAssertion, RDF.type, RELS.Person) in g
    assert not (EX.MaxByBlankAxiom, RDF.type, RELS.Person) in g
    assert not (EX.MaxByNamedAxiom, RDF.type, RELS.Person) in g

    owlrl.DeductiveClosure(owlrl.OWLRL_Extension).expand(g)

    # After defining and expanding closure, confirm the direct and reified Maxes are in the graph according to OWL-RDF mapping specification.
    assert (EX.MaxByAssertion, RDF.type, RELS.Person) in g
    assert (EX.MaxByBlankAxiom, RDF.type, RELS.Person) in g
    # TODO - This last behavior might be undefined.
    assert not (EX.MaxByNamedAxiom, RDF.type, RELS.Person) in g

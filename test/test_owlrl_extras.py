"""
Unit tests for OWL RL extras closure.
"""

from rdflib import Graph, Literal, RDF, XSD
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import owlrl
from owlrl.Namespaces import T


def test_one_time_rules():
    """
    Test OWL 2 RL extras closure one time rules.
    """
    data = """
    @prefix : <http://test.org/> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    :t a rdfs:Datatype ;
        owl:onDatatype xsd:integer;
        owl:withRestrictions (
          [xsd:minInclusive "1"^^xsd:integer]
          [xsd:maxInclusive "6"^^xsd:integer]
      ).
    """

    g = Graph()
    g.parse(data=data, format="n3")

    lt = Literal(2, datatype=XSD.integer)
    g.add((lt, RDF.type, XSD.integer))
    g.add((T.a, T.p, lt))

    owlrl.DeductiveClosure(owlrl.OWLRL_Extension).expand(g)

    assert (lt, RDF.type, T.t) in g

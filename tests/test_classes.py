"""
Test for OWL 2 RL/RDF rules from

    Table 6. The Semantics of Classes

https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules
"""

from rdflib import Graph, BNode, Literal, Namespace, RDF, XSD, RDFS, OWL

import RDFClosure

DAML = Namespace('http://www.daml.org/2002/03/agents/agent-ont#')
T = Namespace('http://test.org/')

def test_cls_maxqc1():
    """
    Test cls-maxqc1 rule for OWL 2 RL.

    If::

        T(?x, owl:maxQualifiedCardinality, "0"^^xsd:nonNegativeInteger)
        T(?x, owl:onProperty, ?p)
        T(?x, owl:onClass, ?c)
        T(?u, rdf:type, ?x)
        T(?u, ?p, ?y)
        T(?y, rdf:type, ?c)

    then::

        false
    """
    g = Graph()

    x = T.x
    p = T.p
    c = T.C
    u = T.u
    y = T.y

    g.add((x, OWL.maxQualifiedCardinality, Literal(0)))
    g.add((x, OWL.onProperty, p))
    g.add((x, OWL.onClass, c))
    g.add((u, p, y))
    g.add((y, RDF.type, c))

    RDFClosure.DeductiveClosure(RDFClosure.OWLRL_Semantics).expand(g)

    result = next(g.objects(predicate=DAML.error))
    expected = Literal(
        'Erroneous usage of maximum qualified cardinality with'
        + ' http://test.org/x, http://test.org/C and http://test.org/y'
    )
    assert expected == result

def test_cls_maxqc2():
    """
    Test cls-maxqc2 rule for OWL 2 RL.

    If::

        T(?x, owl:maxQualifiedCardinality, "0"^^xsd:nonNegativeInteger)
        T(?x, owl:onProperty, ?p)
        T(?x, owl:onClass, owl:Thing)
        T(?u, rdf:type, ?x)
        T(?u, ?p, ?y)

    then::

        false
    """
    g = Graph()

    x = T.x
    p = T.p
    u = T.u
    y = T.y

    g.add((x, OWL.maxQualifiedCardinality, Literal(0)))
    g.add((x, OWL.onProperty, p))
    g.add((x, OWL.onClass, OWL.Thing))
    g.add((u, RDF.type, x))
    g.add((u, p, y))

    RDFClosure.DeductiveClosure(RDFClosure.OWLRL_Semantics).expand(g)

    result = next(g.objects(predicate=DAML.error))
    expected = Literal(
        'Erroneous usage of maximum qualified cardinality with'
        + ' http://test.org/x, http://www.w3.org/2002/07/owl#Thing and'
        + ' http://test.org/y'

    )
    assert expected == result

def test_cls_maxqc3():
    """
    Test cls-maxqc3 rule for OWL 2 RL.

    If::

        T(?x, owl:maxQualifiedCardinality, "1"^^xsd:nonNegativeInteger)
        T(?x, owl:onProperty, ?p)
        T(?x, owl:onClass, ?c)
        T(?u, rdf:type, ?x)
        T(?u, ?p, ?y1)
        T(?y1, rdf:type, ?c)
        T(?u, ?p, ?y2)
        T(?y2, rdf:type, ?c)

    then::

        T(?y1, owl:sameAs, ?y2)
    """
    g = Graph()

    x = T.x
    p = T.p
    c = T.C
    u = T.u
    y1 = T.y1
    y2 = T.y2

    g.add((x, OWL.maxQualifiedCardinality, Literal(1)))
    g.add((x, OWL.onProperty, p))
    g.add((x, OWL.onClass, c))
    g.add((u, RDF.type, x))
    g.add((u, p, y1))
    g.add((y1, RDF.type, c))
    g.add((u, p, y2))
    g.add((y2, RDF.type, c))

    RDFClosure.DeductiveClosure(RDFClosure.OWLRL_Semantics).expand(g)

    assert (y1, OWL.sameAs, y2) in g

def test_cls_maxqc4():
    """
    Test cls-maxqc4 rule for OWL 2 RL.

    If::

        T(?x, owl:maxQualifiedCardinality, "1"^^xsd:nonNegativeInteger)
        T(?x, owl:onProperty, ?p)
        T(?x, owl:onClass, owl:Thing)
        T(?u, rdf:type, ?x)
        T(?u, ?p, ?y1)
        T(?u, ?p, ?y2)

    then::

        T(?y1, owl:sameAs, ?y2)
    """
    g = Graph()

    x = T.x
    p = T.p
    u = T.u
    y1 = T.y1
    y2 = T.y2

    g.add((x, OWL.maxQualifiedCardinality, Literal(1)))
    g.add((x, OWL.onProperty, p))
    g.add((x, OWL.onClass, OWL.Thing))
    g.add((u, RDF.type, x))
    g.add((u, p, y1))
    g.add((u, p, y2))

    RDFClosure.DeductiveClosure(RDFClosure.OWLRL_Semantics).expand(g)

    assert (y1, OWL.sameAs, y2) in g


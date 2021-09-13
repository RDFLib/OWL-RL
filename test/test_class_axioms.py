"""
Test for OWL 2 RL/RDF rules from

    Table 7. The Semantics of Class Axioms

https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules
"""

from rdflib import Graph, Literal, Namespace, RDF, OWL

import owlrl

DAML = Namespace("http://www.daml.org/2002/03/agents/agent-ont#")
T = Namespace("http://test.org/")


def test_cax_dw():
    """
    Test cax-dw rule for OWL 2 RL.

    If::

        T(?c1, owl:disjointWith, ?c2)
        T(?x, rdf:type, ?c1)
        T(?x, rdf:type, ?c2)

    then::

        false
    """
    g = Graph()

    x = T.x
    c1 = T.c1
    c2 = T.c2

    g.add((c1, OWL.disjointWith, c2))
    g.add((x, RDF.type, c1))
    g.add((x, RDF.type, c2))

    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)

    result = next(g.objects(predicate=DAML.error))
    expected = Literal(
        "Disjoint classes http://test.org/c1 and http://test.org/c2"
        " have a common individual http://test.org/x"
    )
    assert expected == result

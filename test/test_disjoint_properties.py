"""
Test for OWL 2 RL/RDF rule prp-adp from

    Table 5. The Semantics of Axioms about Properties

https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules
"""

from itertools import combinations

import pytest
from rdflib import BNode, Graph, OWL, RDF
from rdflib.collection import Collection

import owlrl
from owlrl.Namespaces import ERRNS, T


def _all_disjoint_properties_graph(member_count):
    graph = Graph()
    properties = [T[f"p{i}"] for i in range(member_count)]
    statement = BNode()
    member_list = Collection(graph, BNode(), properties)
    graph.add((statement, RDF.type, OWL.AllDisjointProperties))
    graph.add((statement, OWL.members, member_list.uri))
    for prop in properties:
        graph.add((prop, RDF.type, OWL.ObjectProperty))
    return graph, properties


@pytest.mark.parametrize(
    "member_count,first,second",
    [
        (member_count, first, second)
        for member_count in (2, 3, 5)
        for first, second in combinations(range(member_count), 2)
    ],
)
def test_prp_adp_rejects_shared_pair(member_count, first, second):
    """Every pair of members must be checked, including the last member (#90)."""
    graph, properties = _all_disjoint_properties_graph(member_count)
    graph.add((T.x, properties[first], T.y))
    graph.add((T.x, properties[second], T.y))

    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

    errors = [str(e) for e in graph.objects(predicate=ERRNS.error)]
    assert any("AllDisjointProperties" in e for e in errors)


@pytest.mark.parametrize("member_count", [0, 1, 2, 3, 5])
def test_prp_adp_without_shared_pair(member_count):
    """Members that never link the same pair of individuals do not produce errors."""
    graph, properties = _all_disjoint_properties_graph(member_count)
    for i, prop in enumerate(properties):
        graph.add((T.x, prop, T[f"y{i}"]))

    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

    assert not list(graph.objects(predicate=ERRNS.error))

"""
Test for OWL 2 RL/RDF rule prp-key from

    Table 5. The Semantics of Axioms about Properties

https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules
"""

import pytest
from rdflib import BNode, Graph, Literal, OWL, RDF
from rdflib.collection import Collection

import owlrl
from owlrl.Namespaces import T


def _has_key_graph(key_size):
    graph = Graph()
    properties = [T[f"key{i}"] for i in range(key_size)]
    key_list = Collection(graph, BNode(), properties)
    graph.add((T.C, OWL.hasKey, key_list.uri))
    for prop in properties:
        graph.add((prop, RDF.type, OWL.DatatypeProperty))
    graph.add((T.x, RDF.type, T.C))
    graph.add((T.y, RDF.type, T.C))
    return graph, properties


def _same_as(graph):
    return (T.x, OWL.sameAs, T.y) in graph or (T.y, OWL.sameAs, T.x) in graph


@pytest.mark.parametrize("key_size", [1, 2, 3])
def test_prp_key_same_values_merge(key_size):
    """Instances that agree on every key property are the same individual."""
    graph, properties = _has_key_graph(key_size)
    for prop in properties:
        graph.add((T.x, prop, Literal("same")))
        graph.add((T.y, prop, Literal("same")))

    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

    assert _same_as(graph)


@pytest.mark.parametrize(
    "key_size,differing",
    [(key_size, i) for key_size in (1, 2, 3) for i in range(key_size)],
)
def test_prp_key_different_value_does_not_merge(key_size, differing):
    """A different value for any key property, including the last, prevents owl:sameAs (#89)."""
    graph, properties = _has_key_graph(key_size)
    for i, prop in enumerate(properties):
        graph.add((T.x, prop, Literal("x" if i == differing else "same")))
        graph.add((T.y, prop, Literal("y" if i == differing else "same")))

    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

    assert not _same_as(graph)

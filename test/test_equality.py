"""
Test for OWL 2 RL/RDF rules from

    Table 4. The Semantics of Equality

https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules
"""

from itertools import combinations

import pytest
from rdflib import BNode, Graph, Literal, OWL, RDF
from rdflib.collection import Collection

import owlrl
from owlrl.Namespaces import ERRNS, T


def test_eq_diff1():
    """
    Test eq-diff1 rule for OWL 2 RL.

    If::

        T(?x, owl:sameAs, ?y)
        T(?x, owl:differentFrom, ?y)

    then::

        false
    """
    g = Graph()

    x = T.x
    y = T.y

    g.add((x, OWL.sameAs, y))
    g.add((x, OWL.differentFrom, y))

    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)

    result = g.objects(predicate=ERRNS.error)
    expected = Literal(
        "'sameAs' and 'differentFrom' cannot be used on the same"
        + " subject-object pair:"
    )

    # expect multiple error messages for pairs (x, y), (x, x) and (y, y)
    # due to contradiction:
    #
    #    x == y and x != y => x != x and y != y and x == x and y == y
    assert all(r.startswith(expected) for r in result)


def _all_different_graph(member_count, list_predicate):
    graph = Graph()
    members = [T[f"member{i}"] for i in range(member_count)]
    statement = BNode()
    member_list = Collection(graph, BNode(), members)
    graph.add((statement, RDF.type, OWL.AllDifferent))
    graph.add((statement, list_predicate, member_list.uri))
    return graph, members


@pytest.mark.parametrize("list_predicate", [OWL.members, OWL.distinctMembers])
@pytest.mark.parametrize(
    "member_count,first,second",
    [
        (member_count, first, second)
        for member_count in (2, 3, 5)
        for first, second in combinations(range(member_count), 2)
    ],
)
@pytest.mark.parametrize("reverse", [False, True])
def test_all_different_rejects_same_as_pair(
    list_predicate, member_count, first, second, reverse
):
    """Every AllDifferent pair must conflict with sameAs, including the last member."""
    graph, members = _all_different_graph(member_count, list_predicate)
    left, right = members[first], members[second]
    graph.add((right, OWL.sameAs, left) if reverse else (left, OWL.sameAs, right))

    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

    expected = Literal(
        "'sameAs' and 'AllDifferent' cannot be used on the same subject-object "
        f"pair: ({left}, {right})"
    )
    assert expected in set(graph.objects(predicate=ERRNS.error))


@pytest.mark.parametrize("list_predicate", [OWL.members, OWL.distinctMembers])
@pytest.mark.parametrize("member_count", [0, 1, 2, 3, 5])
def test_all_different_without_conflicting_pair(list_predicate, member_count):
    """Distinct members and unrelated sameAs statements do not produce errors."""
    graph, _ = _all_different_graph(member_count, list_predicate)
    graph.add((T.outside_left, OWL.sameAs, T.outside_right))

    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

    assert not list(graph.objects(predicate=ERRNS.error))

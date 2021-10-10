from rdflib import Graph, Namespace
from rdflib.namespace import RDF
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import owlrl
RELS = Namespace("http://example.org/relatives#")


def test_basic():
    # create an RDF graph, load a simple OWL ontology and data
    g = Graph()
    try:
        g.parse("relatives.ttl", format="turtle")
    except FileNotFoundError:
        # This test might be run from the parent directory root
        g.parse("test/relatives.ttl", format="turtle")

    # count no. rels:Person class instances, no inferencing, should find 14 results (one Child)
    cnt = 0
    for _ in g.subjects(predicate=RDF.type, object=RELS.Person):
        cnt += 1

    assert cnt == 14

    # count no. of hasGrandparent predicates, no inferencing, should find 0 results
    cnt = 0
    for _ in g.subject_objects(predicate=RELS.hasGrandparent):
        cnt += 1
    assert cnt == 0

    # expand the graph with OWL-RL semantics
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)

    # count no. rels:Person class instances, after inferencing, should find 15 results
    cnt = 0
    for _ in g.subjects(predicate=RDF.type, object=RELS.Person):
        cnt += 1

    assert cnt == 15

    # count no. of hasGrandparent predicates, after inferencing, should find 7 results
    cnt = 0
    for _ in g.subject_objects(predicate=RELS.hasGrandparent):
        cnt += 1
    assert cnt == 7

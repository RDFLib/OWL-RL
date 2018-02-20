import rdflib
import sys
import os
# add path for the RDFClosure module
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
import RDFClosure


def test_basic():
    # create an RDF graph, load a simple OWL ontology and data
    g = rdflib.Graph()
    g.parse('relatives.ttl', format='turtle')

    # run a simple SPARQL query against it, no inferencing, should find 15 results
    q = '''
        PREFIX : <http://example.org/relatives#>
        SELECT (COUNT(?s) AS ?cnt)
        WHERE {
            ?s a :Person .
        }
        '''
    for r in g.query(q):
        cnt = int(r[0])
    assert cnt == 15

    # run a SELECT query for grandParents, no inferencing, should find 0 results
    q = '''
        PREFIX : <http://example.org/relatives#>
        SELECT (COUNT(?gc) AS ?cnt)
        WHERE {
            ?gc :hasGrandparent ?gp .
        }
        '''
    for r in g.query(q):
        cnt = int(r[0])
    assert cnt == 0

    # expand the graph with OWL-RL semantics
    RDFClosure.DeductiveClosure(RDFClosure.OWLRL_Semantics).expand(g)

    # run a SELECT query for grandParents, should find 7 results
    q = '''
        PREFIX : <http://example.org/relatives#>
        SELECT (COUNT(?gc) AS ?cnt)
        WHERE {
            ?gc :hasGrandparent ?gp .
        }
        '''
    for r in g.query(q):
        cnt = int(r[0])
    assert cnt == 7

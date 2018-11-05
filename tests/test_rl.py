# these tests are taken from http://owl.semanticweb.org/page/Test:RL.html
# RDF mapping from https://www.w3.org/2007/OWL/wiki/Mapping_to_RDF_Graphs


# Approved and Extra Credit tests


# Chain2trans
# A role chain can be a synonym for transitivity
def test_chain2trans():
    premis_ttl = '''
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix : <http://example.org/> .
        
        :p a owl:ObjectProperty ;
            owl:propertyChainAxiom ( :p :p ) .
    '''

    conclusion_ttl = '''
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix : <http://example.org/> ..
        
        :p a owl:TransitiveProperty .
    '''


# DisjointClasses-001
# Demonstrates a binary disjoint classes axiom based on example in the Structural Specification and Functional-Style
# Syntax document
def test_disjointclasses_001():
    premis = '''
        Prefix( : = <http://example.org/> )
        
        Ontology(
            Declaration( Class( :Boy ) )
            Declaration( Class( :Girl ) )
        
            DisjointClasses( :Boy :Girl )                
            ClassAssertion( :Boy :Stewie )
            ClassAssertion( :Girl :Stewie )
        )
    '''

    premis_ttl = '''
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix : <http://example.org/> .

        :Boy a owl:Class .
        :Girl a owl:Class .
        
        :Boy owl:disjointWith :Girl .
        
        :Stewie a :Boy .
        :Stewie a :Girl .
    '''


# DisjointClasses-002
# Demonstrates a binary disjoint classes axiom and class assertions causing an inconsistency based on example in the
# Structural Specification and Functional-Style Syntax document
def test_disjointclasses_002():
    premis = '''
        Prefix( : = <http://example.org/> )
        
        Ontology(
            Declaration( Class( :Boy ) )
            Declaration( Class( :Girl ) )
            Declaration( Class( :Dog ) )
            
            DisjointClasses( :Boy :Girl :Dog )
            ClassAssertion( :Boy :Stewie )
        )    
    '''

    premis_ttl = '''
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix : <http://example.org/> .

        :Boy a owl:Class .
        :Girl a owl:Class .
        :Dog a owl:Class .
        
        :Boy owl:disjointWith :Girl .
        
        [ ]
            a owl:AllDisjointClasses ;
            owl:members ( :Boy :Girl :Dog ) . 
        
        :Stewie a :Boy .
    '''


# DisjointClasses-003
# A modification of test DisjointClasses-001 to demonstrate a ternary disjoint classes axiom
def test_disjointclasses_003():
    premis = '''
        Prefix( : = <http://example.org/> )
        
        Ontology(
            Declaration( Class( :Boy ) )
            Declaration( Class( :Girl ) )
            Declaration( Class( :Dog ) )
            
            DisjointClasses( :Boy :Girl :Dog )
            ClassAssertion( :Boy :Stewie )
        )    
    '''

    premis_ttl = '''
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix : <http://example.org/> .

        :Boy a owl:Class .
        :Girl a owl:Class .
        :Dog a owl:Class .
        
        :Boy owl:disjointWith :Girl .
        
        [] a owl:AllDisjointClasses ;
            owl:members ( :Boy :Girl :Dog ) . 
        
        :Stewie a :Boy .  
    '''

    conclusion = '''
        Prefix( : = <http://example.org/> )
        
        Ontology(
            Declaration( Class( :Girl ) )
            Declaration( Class( :Dog ) )
            
            ClassAssertion( ObjectComplementOf( :Girl ) :Stewie )
            ClassAssertion( ObjectComplementOf( :Dog ) :Stewie )
        )    
    '''

    conclusion_ttl = '''
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix : <http://example.org/> .
        
        :Girl a owl:Class .
        :Dog a owl:Class .
            
        :Stewie a owl:Class ;
            owl:complementOf :Girl .

        :Stewie a owl:Class ;
            owl:complementOf :Girl .            
    '''


# FS2RDF-different-individuals-2-ar
# Functional syntax to RDFXML translation of ontology consisting of a 2 argument DifferentIndividuals
def test_fs2rdf_different_individuals_2_ar():
    premis = '''
        Prefix(: = <http://example.org/>)
        Ontology(
            DifferentIndividuals( :a :b )
        )
    '''

    premis_ttl = '''
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix : <http://example.org/> .   
        
        :a owl:differentFrom :b .  
    '''


# FS2RDF-different-individuals-3-ar
# Functional syntax to RDFXML translation of ontology consisting of a 3 argument DifferentIndividuals
def test_fs2rdf_different_individuals_3_ar():
    premis = '''
        Prefix(: = <http://example.org/>)
        Ontology(
            DifferentIndividuals( :a :b :c )
        )
    '''

    premis_ttl = '''
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix : <http://example.org/> .   

        [] a owl:AllDifferent ;
            owl:distinctMembers ( :a :b :c ) .
    '''


# FS2RDF-no-builtin-prefixes-ar
# Functional syntax to RDFXML checking that there aren't builtin prefixes for xsd, rdf, rdfs, owl
def test_fs2rdf_no_builtin_prefixes_ar():
    premis = '''
        Prefix(: = <http://example.org/>)
        Prefix(xsd: = <http://example.org/>)
        Prefix(rdf: = <http://example.org/>)
        Prefix(rdfs: = <http://example.org/>)
        Prefix(owl: = <http://example.org/>)
        Ontology(
            SameIndividual(:a xsd:b rdf:c rdfs:d owl:e)
        )    
    '''

    prefix_ttl = '''
        @prefix : <http://example.org/> .  
        @prefix xsd: <http://example.org/> . 
        @prefix rdfs: <http://example.org/> . 
        @prefix rdf: <http://example.org/> . 
        @prefix owl: <http://example.org/> . 
        
        :a = xsd:b .
        :a = rdf:c .
        :a = rdfs:d .
        :a = owl:e .
    '''


# FS2RDF-same-individual-2-ar
# Functional syntax to RDFXML translation of ontology consisting of a 2 argument SameIndividual
def test_fs2rdf_same_individual_2_ar():
    premis = '''
    Prefix(: = <http://example.org/>)
    Ontology(
        SameIndividual( :a :b )
    )    
    '''

    premis_ttl = '''
    @prefix : <http://example.org/> .
    
    :a = :b .
    '''


# Functionality-clash
# The property hasAge is functional, but the individual a has two distinct hasAge fillers
def test_functionality_clash():
    premis = '''
        Prefix(:=<http://example.org/>)
        Prefix(xsd:=<http://www.w3.org/2001/XMLSchema#>)
        Ontology(
            Declaration(NamedIndividual(:a))
            Declaration(DataProperty(:hasAge))
            FunctionalDataProperty(:hasAge) 
            ClassAssertion(DataHasValue(:hasAge "18"^^xsd:integer) :a) 
            ClassAssertion(DataHasValue(:hasAge "19"^^xsd:integer) :a)
        )    
    '''

    premis_ttl = '''
        @prefix : <http://example.org/> . 
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        
        :a a owlNamedIndividual ;
            :hasAge "18"^^xsd:integer , "19"^^xsd:integer .        
        
        :hasAge a owl:DatatypeProperty , owl:FunctionalProperty .    
    '''


# New-Feature-AnnotationAnnotations-001
# Demonstrates annotation of an annotation. Adapted from an example in the Mapping to RDF Graphs document
def test_new_feature_annotationannotations_001():
    premis = '''
        Prefix( rdfs: = <http://www.w3.org/2000/01/rdf-schema#> )
        Prefix( : = <http://example.org/> )
        
        Ontology(<http://example.org/>
            Annotation(
                Annotation( :author "Mike Smith" )
                rdfs:label "An example ontology"
            )
            
            Declaration( AnnotationProperty( :author ) )
            Declaration( NamedIndividual( :i ) )
        )    
    '''

    premis_ttl = '''
        @prefix : <http://example.org/> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .

        :i a owl:NamedIndividual .
        
        : a owl:Ontology ;
            rdfs:label "An example ontology" .
        
        [] a owl:Annotation ;
            :author "Mike Smith" ;
            owl:annotatedProperty rdfs:label ;
            owl:annotatedSource : ;
            owl:annotatedTarget "An example ontology" .
    '''


# New and proposed tests


# Datatype-Float-Discrete-002
# The value space of owl:real is continuous, in contrast with xsd:float
def test_datatype_float_discrete_002():
    premis = '''
        Prefix( owl: = <http://www.w3.org/2002/07/owl#> )
        Prefix( xsd: = <http://www.w3.org/2001/XMLSchema#> )
        Prefix( : = <http://example.org/ontology/> )
        
        Ontology(        
            Declaration( DataProperty( :dp ) )
            
            ClassAssertion(
                DataSomeValuesFrom( :dp
                    DatatypeRestriction( owl:real
                        xsd:minExclusive "0.0"^^xsd:float
                        xsd:maxExclusive "1.401298464324817e-45"^^xsd:float
                    )
                )
                :a
            )
        )    
    '''

    premis_ttl = '''    
        @prefix owl: <http://www.w3.org/2002/07/owl#> .        
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        @prefix : <http://example.org/> .
        
        : a owl:Ontology ;
        
        :dp a owl:DatatypeProperty ;
            owl:someValuesFrom [
            owl:real ( 
                [ xsd:minInclusive "0.0"^^xsd:float ; ] 
                [ xsd:maxInclusive  "1.401298464324817e-45"^^xsd:float ; ] 
            )
        ] .
    
    
    
    '''


# New-Feature-ObjectPropertyChain-BJP-002
# A transitivity axiom should entail a property chain
def test_new_feature_bbjectpropertychain_bjp_002():
    premis = '''

    '''

    premis_ttl = '''

    '''


# WebOnt-I4.6-003
# owl:sameAs is stronger than owl:equivalentClass
def test_webont_i4_6_003():
    premis = '''

    '''

    premis_ttl = '''

    '''


# WebOnt-I4.6-005
# owl:equivalentClass is not related to annotations on classes
def test_webont_i4_6_005():
    premis = '''

    '''

    premis_ttl = '''

    '''


# WebOnt-equivalentClass-008
# Annotation properties refer to a class instance. equivalentClass refers to the class extension
def test_webont_equivalentclass_008():
    premis = '''

    '''

    premis_ttl = '''

    '''

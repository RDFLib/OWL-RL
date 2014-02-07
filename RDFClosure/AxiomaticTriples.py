#!/d/Bin/Python/python.exe
# -*- coding: utf-8 -*-
#
"""
Axiomatic triples to be (possibly) added to the final graph.

@requires: U{RDFLib<https://github.com/RDFLib/rdflib>}, 4.0.0 and higher
@license: This software is available for use under the U{W3C Software License<http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231>}
@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}

"""

__author__  = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = u'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

import rdflib
from RDFClosure.RDFS import Seq, Bag, Alt, Statement, Property, XMLLiteral, List
from RDFClosure.RDFS import RDFNS as ns_rdf
from RDFClosure.RDFS import subject, predicate, object, type, value, first, rest, nil
from RDFClosure.RDFS import Resource, Class, subClassOf, subPropertyOf, comment, label, domain, range
from RDFClosure.RDFS import seeAlso, isDefinedBy, Literal, Container, ContainerMembershipProperty, member, Datatype

from rdflib.namespace 	import XSD as ns_xsd
from OWL import *

#: Simple RDF axiomatic triples (typing of subject, predicate, first, rest, etc)
_Simple_RDF_axiomatic_triples = [
	(type, type, Property),
	(subject, type, Property),
	(predicate, type, Property),
	(object, type, Property),
	(first, type, Property),
	(rest, type, Property),
	(value, type, Property),
	(nil, type, List),
]

#: RDFS axiomatic triples (domain and range, as well as class setting for a number of RDFS symbols)
_RDFS_axiomatic_triples = [
	(type, domain, Resource),
	(domain, domain, Property),
	(range, domain, Property),
	(subPropertyOf, domain, Property),
	(subClassOf, domain, Class),
	(subject, domain, Statement),
	(predicate, domain, Statement),
	(object, domain, Statement),
	(member, domain, Resource),
	(first, domain, List),
	(rest, domain, List),
	(seeAlso, domain, Resource),
	(isDefinedBy, domain, Resource),
	(comment, domain, Resource),
	(label, domain, Resource),
	(value, domain, Resource),
	(Property, type, Class),

	(type, range, Class),
	(domain, range, Class),
	(range, range, Class),
	(subPropertyOf, range, Property),
	(subClassOf, range, Class),
	(subject, range, Resource),
	(predicate, range, Resource),
	(object, range, Resource),
	(member, range, Resource),
	(first, range, Resource),
	(rest, range, List),
	(seeAlso, range, Resource),
	(isDefinedBy, range, Resource),
	(comment, range, Literal),
	(label, range, Literal),
	(value, range, Resource),

	(Alt, subClassOf, Container),
	(Bag, subClassOf, Container),
	(Seq, subClassOf, Container),
	(ContainerMembershipProperty, subClassOf, Property),

	(isDefinedBy, subPropertyOf, seeAlso),

	(XMLLiteral, type, Datatype),
	(XMLLiteral, subClassOf, Literal),
	(Datatype, subClassOf, Class),

	# rdfs valid triples; these would be inferred by the RDFS expansion, but it may make things
	# a bit faster to add these upfront
	(Resource, type, Class),
	(Class, type, Class),
	(Literal, type, Class),
	(XMLLiteral, type, Class),
	(Datatype, type, Class),
	(Seq, type, Class),
	(Bag, type, Class),
	(Alt, type, Class),
	(Container, type, Class),
	(List, type, Class),
	(ContainerMembershipProperty, type, Class),
	(Property, type, Class),
	(Statement, type, Class),

	(domain, type, Property),
	(range, type, Property),
	(subPropertyOf, type, Property),
	(subClassOf, type, Property),
	(member, type, Property),
	(seeAlso, type, Property),
	(isDefinedBy, type, Property),
	(comment, type, Property),
	(label, type, Property)
]

#: RDFS Axiomatic Triples all together
RDFS_Axiomatic_Triples    = _Simple_RDF_axiomatic_triples + _RDFS_axiomatic_triples

#: RDFS D-entailement triples, ie, possible subclassing of various datatypes
RDFS_D_Axiomatic_Triples_subclasses = [
	# See http://www.w3.org/TR/2004/REC-xmlschema-2-20041028/#built-in-datatypes
	(ns_xsd['decimal'], subClassOf, Literal),

	(ns_xsd['integer'], subClassOf, ns_xsd['decimal']),

	(ns_xsd['long'], subClassOf, ns_xsd['integer']),
	(ns_xsd['int'], subClassOf, ns_xsd['long']),
	(ns_xsd['short'], subClassOf, ns_xsd['int']),
	(ns_xsd['byte'], subClassOf, ns_xsd['short']),

	(ns_xsd['nonNegativeInteger'], subClassOf, ns_xsd['integer']),
	(ns_xsd['positiveInteger'], subClassOf, ns_xsd['nonNegativeInteger']),
	(ns_xsd['unsignedLong'], subClassOf, ns_xsd['nonNegativeInteger']),
	(ns_xsd['unsignedInt'], subClassOf, ns_xsd['unsignedLong']),
	(ns_xsd['unsignedShort'], subClassOf, ns_xsd['unsignedInt']),
	(ns_xsd['unsignedByte'], subClassOf, ns_xsd['unsignedShort']),

	(ns_xsd['nonPositiveInteger'], subClassOf, ns_xsd['integer']),
	(ns_xsd['negativeInteger'], subClassOf, ns_xsd['nonPositiveInteger']),

	(ns_xsd['normalizedString'], subClassOf, ns_xsd['string']),
	(ns_xsd['token'], subClassOf, ns_xsd['normalizedString']),
	(ns_xsd['language'], subClassOf, ns_xsd['token']),
	(ns_xsd['Name'], subClassOf, ns_xsd['token']),
	(ns_xsd['NMTOKEN'], subClassOf, ns_xsd['token']),

	(ns_xsd['NCName'], subClassOf, ns_xsd['Name']),

	(ns_xsd['dateTimeStamp'], subClassOf, ns_xsd['dateTime']),
]

RDFS_D_Axiomatic_Triples_types = [
	(ns_xsd['integer'], type, Datatype),
	(ns_xsd['decimal'], type, Datatype),
	(ns_xsd['nonPositiveInteger'], type, Datatype),
	(ns_xsd['nonPositiveInteger'], type, Datatype),
	(ns_xsd['positiveInteger'], type, Datatype),
	(ns_xsd['positiveInteger'], type, Datatype),
	(ns_xsd['long'], type, Datatype),
	(ns_xsd['int'], type, Datatype),
	(ns_xsd['short'], type, Datatype),
	(ns_xsd['byte'], type, Datatype),
	(ns_xsd['unsignedLong'], type, Datatype),
	(ns_xsd['unsignedInt'], type, Datatype),
	(ns_xsd['unsignedShort'], type, Datatype),
	(ns_xsd['unsignedByte'], type, Datatype),
	(ns_xsd['float'], type, Datatype),
	(ns_xsd['double'], type, Datatype),
	(ns_xsd['string'], type, Datatype),
	(ns_xsd['normalizedString'], type, Datatype),
	(ns_xsd['token'], type, Datatype),
	(ns_xsd['language'], type, Datatype),
	(ns_xsd['Name'], type, Datatype),
	(ns_xsd['NCName'], type, Datatype),
	(ns_xsd['NMTOKEN'], type, Datatype),
	(ns_xsd['boolean'], type, Datatype),
	(ns_xsd['hexBinary'], type, Datatype),
	(ns_xsd['base64Binary'], type, Datatype),
	(ns_xsd['anyURI'], type, Datatype),
	(ns_xsd['dateTimeStamp'], type, Datatype),
	(ns_xsd['dateTime'], type, Datatype),
	(Literal, type, Datatype),
	(XMLLiteral, type, Datatype),
]

RDFS_D_Axiomatic_Triples = RDFS_D_Axiomatic_Triples_types + RDFS_D_Axiomatic_Triples_subclasses

#: OWL Class axiomatic triples: definition of special classes
_OWL_axiomatic_triples_Classes = [
	(AllDifferent, type, Class),
	(AllDifferent, subClassOf, Resource),

	(AllDisjointClasses, type, Class),
	(AllDisjointClasses, subClassOf, Resource),

	(AllDisjointProperties, type, Class),
	(AllDisjointProperties, subClassOf, Resource),

	(Annotation, type, Class),
	(Annotation, subClassOf, Resource),

	(AnnotationProperty, type, Class),
	(AnnotationProperty, subClassOf, Property),

	(AsymmetricProperty, type, Class),
	(AsymmetricProperty, subClassOf, Property),

	(OWLClass, type, Class),
	(OWLClass, equivalentClass, Class),

#	(DataRange, type, Class),
#	(DataRange, equivalentClass, Datatype),

	(Datatype, type, Class),

	(DatatypeProperty, type, Class),
	(DatatypeProperty, subClassOf, Property),

	(DeprecatedClass, type, Class),
	(DeprecatedClass, subClassOf, Class),

	(DeprecatedProperty, type, Class),
	(DeprecatedProperty, subClassOf, Property),

	(FunctionalProperty, type, Class),
	(FunctionalProperty, subClassOf, Property),

	(InverseFunctionalProperty, type, Class),
	(InverseFunctionalProperty, subClassOf, Property),

	(IrreflexiveProperty, type, Class),
	(IrreflexiveProperty, subClassOf, Property),

	(Literal, type, Datatype),

#	(NamedIndividual, type, Class),
#	(NamedIndividual, equivalentClass, Resource),

	(NegativePropertyAssertion, type, Class),
	(NegativePropertyAssertion, subClassOf, Resource),

	(Nothing, type, Class),
	(Nothing, subClassOf, Thing ),

	(ObjectProperty, type, Class),
	(ObjectProperty, equivalentClass, Property),

	(Ontology, type, Class),
	(Ontology, subClassOf, Resource),

	(OntologyProperty, type, Class),
	(OntologyProperty, subClassOf, Property),

	(Property, type, Class),

	(ReflexiveProperty, type, Class),
	(ReflexiveProperty, subClassOf, Property),

	(Restriction, type, Class),
	(Restriction, subClassOf, Class),


	(SymmetricProperty, type, Class),
	(SymmetricProperty, subClassOf, Property),

	(Thing, type, Class),
	(Thing, subClassOf, Resource),

	(TransitiveProperty, type, Class),
	(TransitiveProperty, subClassOf, Property),

	# OWL valid triples; some of these would be inferred by the OWL RL expansion, but it may make things
	# a bit faster to add these upfront
	(AllDisjointProperties, type, OWLClass),
	(AllDisjointClasses, type, OWLClass),
	(AllDisjointProperties, type, OWLClass),
	(Annotation, type, OWLClass),
	(AsymmetricProperty, type, OWLClass),
	(Axiom, type, OWLClass),
	(DataRange, type, OWLClass),
	(Datatype, type, OWLClass),
	(DatatypeProperty, type, OWLClass),
	(DeprecatedClass, type, OWLClass),
	(DeprecatedClass, subClassOf, OWLClass),
	(DeprecatedProperty, type, OWLClass),
	(FunctionalProperty, type, OWLClass),
	(InverseFunctionalProperty, type, OWLClass),
	(IrreflexiveProperty, type, OWLClass),
	(NamedIndividual, type, OWLClass),
	(NegativePropertyAssertion, type, OWLClass),
	(Nothing, type, OWLClass),
	(ObjectProperty, type, OWLClass),
	(Ontology, type, OWLClass),
	(OntologyProperty, type, OWLClass),
	(Property, type, OWLClass),
	(ReflexiveProperty, type, OWLClass),
	(Restriction, type, OWLClass),
	(Restriction, subClassOf, OWLClass),
#	(SelfRestriction, type, OWLClass),
	(SymmetricProperty, type, OWLClass),
	(Thing, type, OWLClass),
	(TransitiveProperty, type, OWLClass),
]

#: OWL Property axiomatic triples: definition of domains and ranges
_OWL_axiomatic_triples_Properties = [
	(allValuesFrom, type, Property),
	(allValuesFrom, domain, Restriction),
	(allValuesFrom, range, Class),

	(assertionProperty, type, Property),
	(assertionProperty, domain, NegativePropertyAssertion),
	(assertionProperty, range, Property),

	(backwardCompatibleWith, type, OntologyProperty),
	(backwardCompatibleWith, type, AnnotationProperty),
	(backwardCompatibleWith, domain, Ontology),
	(backwardCompatibleWith, range, Ontology),

#	(bottomDataProperty, type, DatatypeProperty),
#
#	(bottomObjectProperty, type, ObjectProperty),

#	(cardinality, type, Property),
#	(cardinality, domain, Restriction),
#	(cardinality, range, ns_xsd["nonNegativeInteger"]),

	(comment, type, AnnotationProperty),
	(comment, domain, Resource),
	(comment, range, Literal),

	(complementOf, type, Property),
	(complementOf, domain, Class),
	(complementOf, range, Class),

#
#	(datatypeComplementOf, type, Property),
#	(datatypeComplementOf, domain, Datatype),
#	(datatypeComplementOf, range, Datatype),

	(deprecated, type, AnnotationProperty),
	(deprecated, domain, Resource),
	(deprecated, range, Resource),

	(differentFrom, type, Property),
	(differentFrom, domain, Resource),
	(differentFrom, range, Resource),

#	(disjointUnionOf, type, Property),
#	(disjointUnionOf, domain, Class),
#	(disjointUnionOf, range, List),

	(disjointWith, type, Property),
	(disjointWith, domain, Class),
	(disjointWith, range, Class),

	(distinctMembers, type, Property),
	(distinctMembers, domain, AllDifferent),
	(distinctMembers, range, List),

	(equivalentClass, type, Property),
	(equivalentClass, domain, Class),
	(equivalentClass, range, Class),

	(equivalentProperty, type, Property),
	(equivalentProperty, domain, Property),
	(equivalentProperty, range, Property),

	(hasKey, type, Property),
	(hasKey, domain, Class),
	(hasKey, range, List),

	(hasValue, type, Property),
	(hasValue, domain, Restriction),
	(hasValue, range, Resource),

	(imports, type, OntologyProperty),
	(imports, domain, Ontology),
	(imports, range, Ontology),

	(incompatibleWith, type, OntologyProperty),
	(incompatibleWith, type, AnnotationProperty),
	(incompatibleWith, domain, Ontology),
	(incompatibleWith, range, Ontology),

	(intersectionOf, type, Property),
	(intersectionOf, domain, Class),
	(intersectionOf, range, List),

	(inverseOf, type, Property),
	(inverseOf, domain, Property),
	(inverseOf, range, Property),

	(isDefinedBy, type, AnnotationProperty),
	(isDefinedBy, domain, Resource),
	(isDefinedBy, range, Resource),

	(label, type, AnnotationProperty),
	(label, domain, Resource),
	(label, range, Literal),

	(maxCardinality, type, Property),
	(maxCardinality, domain, Restriction),
	(maxCardinality, range, ns_xsd["nonNegativeInteger"]),

	(maxQualifiedCardinality, type, Property),
	(maxQualifiedCardinality, domain, Restriction),
	(maxQualifiedCardinality, range, ns_xsd["nonNegativeInteger"]),

	(members, type, Property),
	(members, domain, Resource),
	(members, range, List),

#	(minCardinality, type, Property),
#	(minCardinality, domain, Restriction),
#	(minCardinality, range, ns_xsd["nonNegativeInteger"]),

#	(minQualifiedCardinality, type, Property),
#	(minQualifiedCardinality, domain, Restriction),
#	(minQualifiedCardinality, range, ns_xsd["nonNegativeInteger"]),

#	(annotatedTarget, type, Property),
#	(annotatedTarget, domain, Resource),
#	(annotatedTarget, range, Resource),

	(onClass, type, Property),
	(onClass, domain, Restriction),
	(onClass, range, Class),

#	(onDataRange, type, Property),
#	(onDataRange, domain, Restriction),
#	(onDataRange, range, Datatype),

	(onDatatype, type, Property),
	(onDatatype, domain, Datatype),
	(onDatatype, range, Datatype),

	(oneOf, type, Property),
	(oneOf, domain, Class),
	(oneOf, range, List),

	(onProperty, type, Property),
	(onProperty, domain, Restriction),
	(onProperty, range, Property),

#	(onProperties, type, Property),
#	(onProperties, domain, Restriction),
#	(onProperties, range, List),

#	(annotatedProperty, type, Property),
#	(annotatedProperty, domain, Resource),
#	(annotatedProperty, range, Property),

	(priorVersion, type, OntologyProperty),
	(priorVersion, type, AnnotationProperty),
	(priorVersion, domain, Ontology),
	(priorVersion, range, Ontology),

	(propertyChainAxiom, type, Property),
	(propertyChainAxiom, domain, Property),
	(propertyChainAxiom, range, List),

#	(propertyDisjointWith, type, Property),
#	(propertyDisjointWith, domain, Property),
#	(propertyDisjointWith, range, Property),
#
#	(qualifiedCardinality, type, Property),
#	(qualifiedCardinality, domain, Restriction),
#	(qualifiedCardinality, range, ns_xsd["nonNegativeInteger"]),

	(sameAs, type, Property),
	(sameAs, domain, Resource),
	(sameAs, range, Resource),

	(seeAlso, type, AnnotationProperty),
	(seeAlso, domain, Resource),
	(seeAlso, range, Resource),

	(someValuesFrom, type, Property),
	(someValuesFrom, domain, Restriction),
	(someValuesFrom, range, Class),

	(sourceIndividual, type, Property),
	(sourceIndividual, domain, NegativePropertyAssertion),
	(sourceIndividual, range, Resource),
#
#	(annotatedSource, type, Property),
#	(annotatedSource, domain, Resource),
#	(annotatedSource, range, Resource),
#
	(targetIndividual, type, Property),
	(targetIndividual, domain, NegativePropertyAssertion),
	(targetIndividual, range, Resource),

	(targetValue, type, Property),
	(targetValue, domain, NegativePropertyAssertion),
	(targetValue, range, Literal),

#	(topDataProperty, type, DatatypeProperty),
#	(topDataProperty, domain, Resource),
#	(topDataProperty, range, Literal),
#
#	(topObjectProperty, type, ObjectProperty),
#	(topObjectProperty, domain, Resource),
#	(topObjectProperty, range, Resource),

	(unionOf, type, Property),
	(unionOf, domain, Class),
	(unionOf, range, List),

	(versionInfo, type, AnnotationProperty),
	(versionInfo, domain, Resource),
	(versionInfo, range, Resource),

	(versionIRI, type, AnnotationProperty),
	(versionIRI, domain, Resource),
	(versionIRI, range, Resource),

	(withRestrictions, type, Property),
	(withRestrictions, domain, Datatype),
	(withRestrictions, range, List),

	# some OWL valid triples; these would be inferred by the OWL RL expansion, but it may make things
	# a bit faster to add these upfront
	(allValuesFrom, range, OWLClass),
	(complementOf, domain, OWLClass),
	(complementOf, range, OWLClass),

#	(datatypeComplementOf, domain, DataRange),
#	(datatypeComplementOf, range, DataRange),
	(disjointUnionOf, domain, OWLClass),
	(disjointWith, domain, OWLClass),
	(disjointWith, range, OWLClass),
	(equivalentClass, domain, OWLClass),
	(equivalentClass, range, OWLClass),
	(hasKey, domain, OWLClass),
	(intersectionOf, domain, OWLClass),
	(onClass, range, OWLClass),
#	(onDataRange, range, DataRange),
	(onDatatype, domain, DataRange),
	(onDatatype, range, DataRange),
	(oneOf, domain, OWLClass),
	(someValuesFrom, range, OWLClass),
	(unionOf, range, OWLClass),
#	(withRestrictions, domain, DataRange)
]

#: OWL RL axiomatic triples: combination of the RDFS triples plus the OWL specific ones
OWLRL_Axiomatic_Triples   = _OWL_axiomatic_triples_Classes   + _OWL_axiomatic_triples_Properties

# Note that this is not used anywhere. But I encoded it once and I did not want to remove it...:-)
_OWL_axiomatic_triples_Facets = [
	# langPattern
	(ns_xsd['length'],type,Property),
	(ns_xsd['maxExclusive'],type,Property),
	(ns_xsd['maxInclusive'],type,Property),
	(ns_xsd['maxLength'],type,Property),
	(ns_xsd['minExclusive'],type,Property),
	(ns_xsd['minInclusive'],type,Property),
	(ns_xsd['minLength'],type,Property),
	(ns_xsd['pattern'],type,Property),

	(ns_xsd['length'],domain,Resource),
	(ns_xsd['maxExclusive'],domain,Resource),
	(ns_xsd['maxInclusive'],domain,Resource),
	(ns_xsd['maxLength'],domain,Resource),
	(ns_xsd['minExclusive'],domain,Resource),
	(ns_xsd['minInclusive'],domain,Resource),
	(ns_xsd['minLength'],domain,Resource),
	(ns_xsd['pattern'],domain,Resource),
	(ns_xsd['length'],domain,Resource),

	(ns_xsd['maxExclusive'],range,Literal),
	(ns_xsd['maxInclusive'],range,Literal),
	(ns_xsd['maxLength'],range,Literal),
	(ns_xsd['minExclusive'],range,Literal),
	(ns_xsd['minInclusive'],range,Literal),
	(ns_xsd['minLength'],range,Literal),
	(ns_xsd['pattern'],range,Literal),
]

#: OWL D-entailment triples (additionally to the RDFS ones), ie, possible subclassing of various extra datatypes
_OWL_D_Axiomatic_Triples_types = [
	(ns_rdf['PlainLiteral'], type, Datatype)
]

OWL_D_Axiomatic_Triples_subclasses = [
	(ns_xsd['string'], subClassOf, ns_rdf['PlainLiteral']),
	(ns_xsd['normalizedString'], subClassOf, ns_rdf['PlainLiteral']),
	(ns_xsd['token'], subClassOf, ns_rdf['PlainLiteral']),
	(ns_xsd['Name'], subClassOf, ns_rdf['PlainLiteral']),
	(ns_xsd['NCName'], subClassOf, ns_rdf['PlainLiteral']),
	(ns_xsd['NMTOKEN'], subClassOf, ns_rdf['PlainLiteral'])
]

OWLRL_Datatypes_Disjointness = [
	(ns_xsd["anyURI"], disjointWith, ns_xsd['base64Binary']),
	(ns_xsd["anyURI"], disjointWith, ns_xsd['boolean']),
	(ns_xsd["anyURI"], disjointWith, ns_xsd['dateTime']),
	(ns_xsd["anyURI"], disjointWith, ns_xsd['decimal']),
	(ns_xsd["anyURI"], disjointWith, ns_xsd['double']),
	(ns_xsd["anyURI"], disjointWith, ns_xsd['float']),
	(ns_xsd["anyURI"], disjointWith, ns_xsd['hexBinary']),
	(ns_xsd["anyURI"], disjointWith, ns_xsd['string']),
	(ns_xsd["anyURI"], disjointWith, ns_rdf['PlainLiteral']),
	(ns_xsd["anyURI"], disjointWith, XMLLiteral),

	(ns_xsd["base64Binary"], disjointWith, ns_xsd['boolean']),
	(ns_xsd["base64Binary"], disjointWith, ns_xsd['dateTime']),
	(ns_xsd["base64Binary"], disjointWith, ns_xsd['decimal']),
	(ns_xsd["base64Binary"], disjointWith, ns_xsd['double']),
	(ns_xsd["base64Binary"], disjointWith, ns_xsd['float']),
	(ns_xsd["base64Binary"], disjointWith, ns_xsd['hexBinary']),
	(ns_xsd["base64Binary"], disjointWith, ns_xsd['string']),
	(ns_xsd["base64Binary"], disjointWith, ns_rdf['PlainLiteral']),
	(ns_xsd["base64Binary"], disjointWith, XMLLiteral),

	(ns_xsd["boolean"], disjointWith, ns_xsd['dateTime']),
	(ns_xsd["boolean"], disjointWith, ns_xsd['decimal']),
	(ns_xsd["boolean"], disjointWith, ns_xsd['double']),
	(ns_xsd["boolean"], disjointWith, ns_xsd['float']),
	(ns_xsd["boolean"], disjointWith, ns_xsd['hexBinary']),
	(ns_xsd["boolean"], disjointWith, ns_xsd['string']),
	(ns_xsd["boolean"], disjointWith, ns_rdf['PlainLiteral']),
	(ns_xsd["boolean"], disjointWith, XMLLiteral),

	(ns_xsd["dateTime"], disjointWith, ns_xsd['decimal']),
	(ns_xsd["dateTime"], disjointWith, ns_xsd['double']),
	(ns_xsd["dateTime"], disjointWith, ns_xsd['float']),
	(ns_xsd["dateTime"], disjointWith, ns_xsd['hexBinary']),
	(ns_xsd["dateTime"], disjointWith, ns_xsd['string']),
	(ns_xsd["dateTime"], disjointWith, ns_rdf['PlainLiteral']),
	(ns_xsd["dateTime"], disjointWith, XMLLiteral),

	(ns_xsd["decimal"], disjointWith, ns_xsd['double']),
	(ns_xsd["decimal"], disjointWith, ns_xsd['float']),
	(ns_xsd["decimal"], disjointWith, ns_xsd['hexBinary']),
	(ns_xsd["decimal"], disjointWith, ns_xsd['string']),
	(ns_xsd["decimal"], disjointWith, ns_rdf['PlainLiteral']),
	(ns_xsd["decimal"], disjointWith, XMLLiteral),

	(ns_xsd["double"], disjointWith, ns_xsd['float']),
	(ns_xsd["double"], disjointWith, ns_xsd['hexBinary']),
	(ns_xsd["double"], disjointWith, ns_xsd['string']),
	(ns_xsd["double"], disjointWith, ns_rdf['PlainLiteral']),
	(ns_xsd["double"], disjointWith, XMLLiteral),

	(ns_xsd["float"], disjointWith, ns_xsd['hexBinary']),
	(ns_xsd["float"], disjointWith, ns_xsd['string']),
	(ns_xsd["float"], disjointWith, ns_rdf['PlainLiteral']),
	(ns_xsd["float"], disjointWith, XMLLiteral),

	(ns_xsd["hexBinary"], disjointWith, ns_xsd['string']),
	(ns_xsd["hexBinary"], disjointWith, ns_rdf['PlainLiteral']),
	(ns_xsd["hexBinary"], disjointWith, XMLLiteral),

	(ns_xsd["string"], disjointWith, XMLLiteral),
]

#: OWL RL D Axiomatic triples: combination of the RDFS ones, plus some extra statements on ranges and domains, plus some OWL specific datatypes
OWLRL_D_Axiomatic_Triples = RDFS_D_Axiomatic_Triples + _OWL_D_Axiomatic_Triples_types + OWL_D_Axiomatic_Triples_subclasses + OWLRL_Datatypes_Disjointness




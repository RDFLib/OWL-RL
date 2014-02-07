#!/d/Bin/Python/python.exe
# -*- coding: utf-8 -*-
#
"""

Extension to OWL 2 RL, ie, some additional rules added to the system from OWL 2 Full. It is implemented through
the L{OWLRL_Extension} class, whose reference has to be passed to the relevant semantic class (ie, either the OWL 2 RL or the combined
closure class) as an 'extension'.

The added rules and features are:

 - self restriction
 - owl:rational datatype
 - datatype restrictions via facets
 
In more details, the rules that are added:

 1. self restriction 1: C{?z owl:hasSelf ?x. ?x owl:onProperty ?p. ?y rdf:type ?z. => ?y ?p ?y.}
 2. self restriction 2: C{?z owl:hasSelf ?x. ?x owl:onProperty ?p. ?y ?p ?y. => ?y rdf:type ?z. }

@requires: U{RDFLib<https://github.com/RDFLib/rdflib>}, 4.0.0 and higher
@license: This software is available for use under the U{W3C Software License<http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231>}
@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}

"""

__author__  = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = u'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

import rdflib
# noinspection PyPep8Naming
from rdflib.namespace 	import XSD as ns_xsd

from .RDFS	import  Property
# noinspection PyPep8Naming
from .RDFS	import type as rdfType
from .RDFS 	import Resource, Class, subClassOf, subPropertyOf, domain
from .RDFS 	import Datatype

from fractions import Fraction as Rational

from .DatatypeHandling import AltXSDToPYTHON

from .OWL import *
# noinspection PyPep8Naming
from .OWL import OWLNS as ns_owl
from .CombinedClosure import RDFS_OWLRL_Semantics
from .OWLRL import OWLRL_Annotation_properties

from .XsdDatatypes import OWL_RL_Datatypes, OWL_Datatype_Subsumptions

from RestrictedDatatype import extract_faceted_datatypes

###########################################################################################################################
# Rational datatype

# noinspection PyPep8Naming
def _strToRational(v):
	"""Converting a string to a rational.
	
	According to the OWL spec: numerator must be an integer, denominator a positive integer (ie, xsd['integer'] type), and the denominator
	should not have a '+' sign.
	
	@param v: the literal string defined as boolean
	@return corresponding Rational value
	@rtype: Rational
	@raise ValueError: invalid rational string literal
	"""
	try :
		r = v.split('/')
		if len(r) == 2:
			n_str = r[0]
			d_str = r[1]
		else:
			n_str = r[0]
			d_str = "1"
		if d_str.strip()[0] == '+':
			raise ValueError("Invalid Rational literal value %s" % v)
		else :
			return Rational(AltXSDToPYTHON[ns_xsd["integer"]](n_str), AltXSDToPYTHON[ns_xsd["positiveInteger"]](d_str))
	except:
		raise ValueError("Invalid Rational literal value %s" % v)

###########################################################################################################################


# noinspection PyPep8Naming,PyBroadException
class OWLRL_Extension(RDFS_OWLRL_Semantics) :
	"""
	Additional rules to OWL 2 RL. The initialization method also adds the C{owl:rational} datatype to the set of allowed 
	datatypes with the L{_strToRational} function as a conversion between the literal form and a Rational. The C{xsd:decimal} datatype
	is also set to be a subclass of C{owl:rational}. Furthermore, the restricted datatypes are extracted from the graph
	using a L{separate method in a different module<RestrictedDatatype.extract_faceted_datatypes>}, and all those datatypes are also
	added to the set of allowed datatypes. In the case of the restricted datatypes and extra subsumption relationship is set up
	between the restricted and the base datatypes.

	@cvar extra_axioms: additional axioms that have to be added to the deductive closure (in case the axiomatic triples are required)
	@ivar restricted_datatypes : list of the datatype restriction
	@type restricted_datatypes : array of L{restricted datatype<RestrictedDatatype.RestrictedDatatype>} instances
	"""
	extra_axioms = [
		(hasSelf, rdfType, Property),
		(hasSelf, domain, Property),
	]
	def __init__(self, graph, axioms, daxioms, rdfs=False):
		"""
		@param graph: the RDF graph to be extended
		@type graph: rdflib.Graph
		@param axioms: whether (non-datatype) axiomatic triples should be added or not
		@type axioms: Boolean
		@param daxioms: whether datatype axiomatic triples should be added or not
		@type daxioms: Boolean
		@param rdfs: whether RDFS extension is done 
		@type rdfs: boolean
		"""
		RDFS_OWLRL_Semantics.__init__(self, graph, axioms, daxioms, rdfs)
		self.rdfs = rdfs
		self.add_new_datatype(ns_owl["rational"], _strToRational, OWL_RL_Datatypes, 
						      subsumption_dict = OWL_Datatype_Subsumptions, 
						      subsumption_key  = ns_xsd["decimal"], 
						      subsumption_list = [ns_owl["rational"]])
		
		self.restricted_datatypes = extract_faceted_datatypes(self, graph)
		for dt in self.restricted_datatypes:
			self.add_new_datatype(dt.datatype, dt.toPython, OWL_RL_Datatypes,
								  subsumption_dict = OWL_Datatype_Subsumptions,
								  subsumption_key  = dt.datatype,
								  subsumption_list = [dt.base_type])

	# noinspection PyShadowingNames
	def _subsume_restricted_datatypes(self):
		"""
		A one-time-rule: all the literals are checked whether they are (a) of type restricted by a
		faceted (restricted) datatype and (b) whether
		the corresponding value abides to the restrictions. If true, then the literal gets an extra
		tag as being of type of the restricted datatype, too.
		"""
		for rt in self.restricted_datatypes:
			# This is a recorded restriction. The base type is:
			base_type = rt.base_type
			# Look through all the literals; more precisely, through the
			# proxy bnodes:
			for bn in self.literal_proxies.bnode_to_lit:
				# check if the type of that proxy matches. Note that this also takes
				# into account the subsumption datatypes, that have been taken
				# care of by the 'regular' OWL RL process
				if (bn, rdfType, base_type) in self.graph:
					# yep, that is a good candidate!
					lt = self.literal_proxies.bnode_to_lit[bn]
					try :
						# the conversion or the check may go wrong and raise an exception; then simply move on
						value = lt.lit.toPython()
						if rt.checkValue(value):
							# yep, this is also of type 'rt'
							self.store_triple((bn, rdfType, rt.datatype))
					except:
						continue

	def restriction_typing_check(self, v, t):
		"""Helping method to check whether a type statement is in line with a possible
		restriction. This method is invoked by rule "cls-avf" before setting a type
		on an allValuesFrom restriction.
		
		The method is a placeholder at this level. It is typically implemented by subclasses for
		extra checks, eg, for datatype facet checks.
		@param v: the resource that is to be 'typed'
		@param t: the targeted type (ie, Class)
		@return: boolean
		"""
		# Look through the restricted datatypes to see if 't' corresponds to one of those...
		# There are a bunch of possible exceptions here with datatypes, but they can all
		# be ignored...
		try :
			for rt in self.restricted_datatypes:
				if rt.datatype == t:
					# bingo
					if v in self.literal_proxies.bnode_to_lit:
						return rt.checkValue(self.literal_proxies.bnode_to_lit[v].lit.toPython())
					else :
						return True
			# if we got here, no restriction applies
			return True
		except :
			return True

	def one_time_rules(self):
		"""
		This method is invoked only once at the beginning, and prior of, the forward chaining process.

		At present, only the L{subsumption} of restricted datatypes<_subsume_restricted_datatypes>} is performed.
		"""
		RDFS_OWLRL_Semantics.one_time_rules(self)
		# it is important to flush the triples at this point, because
		# the handling of the restriction datatypes rely on the datatype
		# subsumption triples added by the superclass
		self.flush_stored_triples()
		self._subsume_restricted_datatypes()

	def add_axioms(self):
		"""
		Add the L{extra axioms<OWLRL_Extension.extra_axioms>}, related to the self restrictions.
		"""
		RDFS_OWLRL_Semantics.add_axioms(self)
		for t in self.extra_axioms : self.graph.add(t)

	def rules(self, t, cycle_num):
		"""
		Go through the additional rules implemented by this module.
		@param t: a triple (in the form of a tuple)
		@param cycle_num: which cycle are we in, starting with 1. This value is forwarded to all local rules; it is also used
		locally to collect the bnodes in the graph.
		"""
		RDFS_OWLRL_Semantics.rules(self, t, cycle_num)
		z, q, x = t
		if q == hasSelf:
			for p in self.graph.objects(z, onProperty):
				for y in self.graph.subjects(rdfType, z):
					self.store_triple((y, p, y))
				for y1, y2 in self.graph.subject_objects(p):
					if y1 == y2 :
						self.store_triple((y1, rdfType, z))


# noinspection PyPep8Naming
class OWLRL_Extension_Trimming(OWLRL_Extension):
	"""
	This Class adds only one feature to L{OWLRL_Extension}: to initialize with a trimming flag set to C{True} by default. 
	
	This is pretty experimental and probably contentious: this class I{removes} a number of triples from the Graph at the very end of the processing steps.
	These triples are either the by-products of the deductive closure calculation or are axiom like triples that are added following the rules of OWL 2 RL.
	While these triples I{are necessary} for the correct inference of really 'useful' triples, they may not be of interest for the application
	for the end result. The triples that are removed are of the form (following a SPARQL-like notation):
	
	 - C{?x owl:sameAs ?x}, C{?x rdfs:subClassOf ?x}, C{?x rdfs:subPropertyOf ?x}, C{?x owl:equivalentClass ?x} type triples
	 - C{?x rdfs:subClassOf rdf:Resource}, C{?x rdfs:subClassOf owl:Thing}, C{?x rdf:type rdf:Resource}, C{owl:Nothing rdfs:subClassOf ?x} type triples
	 - For a datatype that does I{not} appear explicitly in a type assignments (ie, in a C{?x rdf:type dt}) the corresponding C{dt rdf:type owl:Datatype} and C{dt rdf:type owl:DataRange} triples, as well as the disjointness statements with other datatypes
	 - annotation property axioms
	 - a number of axiomatic triples on C{owl:Thing}, C{owl:Nothing} and C{rdf:Resource} (eg, C{owl:Nothing rdf:type owl:Class}, C{owl:Thing owl:equivalentClass rdf:Resource}, etc.)
	
	Trimming is the only feature of this class, done in the L{post_process} step. If users extend L{OWLRL_Extension}, this class can be safely mixed in via multiple
	inheritance.
	"""
	def __init__(self, graph, axioms, daxioms, rdfs=False):
		"""
		@param graph: the RDF graph to be extended
		@type graph: rdflib.Graph
		@param axioms: whether (non-datatype) axiomatic triples should be added or not
		@type axioms: Boolean
		@param daxioms: whether datatype axiomatic triples should be added or not
		@type daxioms: Boolean
		@param rdfs: whether RDFS extension is done 
		@type rdfs: boolean
		"""
		OWLRL_Extension.__init__(self, graph, axioms, daxioms, rdfs=False)

	def post_process(self) :
		"""
		Do some post-processing step performing the trimming of the graph. See the L{class description<OWLRL_Extension_Trimming>} for further details.
		
		"""
		OWLRL_Extension.post_process(self)
		self.flush_stored_triples()
		
		to_be_removed = set()
		for t in self.graph:
			s, p, o = t
			if s == o :
				if p == sameAs or p == equivalentClass or p == subClassOf or p == subPropertyOf:
					to_be_removed.add(t)
			if (p == subClassOf and (o == Thing or o == Resource)) or (p == rdfType and o == Resource) or (s == Nothing and p == subClassOf):
				to_be_removed.add(t)
		
		for dt in OWL_RL_Datatypes :
			# see if this datatype appears explicitly in the graph as the type of a symbol
			if len([s for s in self.graph.subjects(rdfType, dt)]) == 0:
				to_be_removed.add((dt, rdfType, Datatype))
				to_be_removed.add((dt, rdfType, DataRange))
				
				for t in self.graph.triples((dt, disjointWith, None)):
					to_be_removed.add(t)
				for t in self.graph.triples((None, disjointWith, dt)):
					to_be_removed.add(t)

		for an in OWLRL_Annotation_properties:
			self.graph.remove((an, rdfType, AnnotationProperty))

		to_be_removed.add((Nothing, rdfType, OWLClass))
		to_be_removed.add((Nothing, rdfType, Class))
		to_be_removed.add((Thing, rdfType, OWLClass))
		to_be_removed.add((Thing, rdfType, Class))
		to_be_removed.add((Thing, equivalentClass, Resource))
		to_be_removed.add((Resource, equivalentClass, Thing))
		to_be_removed.add((OWLClass, equivalentClass, Class))
		to_be_removed.add((OWLClass, subClassOf, Class))
		to_be_removed.add((Class, equivalentClass, OWLClass))
		to_be_removed.add((Class, subClassOf, OWLClass))
		to_be_removed.add((Datatype, subClassOf, DataRange))
		to_be_removed.add((Datatype, equivalentClass, DataRange))
		to_be_removed.add((DataRange, subClassOf, Datatype))
		to_be_removed.add((DataRange, equivalentClass, Datatype))

		for t in to_be_removed:
			self.graph.remove(t)



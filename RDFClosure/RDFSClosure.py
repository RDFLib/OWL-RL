#!/d/Bin/Python/python.exe
# -*- coding: utf-8 -*-
#
"""
This module is brute force implementation of the RDFS semantics on the top of RDFLib (with some caveats, see in the introductory text).


@requires: U{RDFLib<https://github.com/RDFLib/rdflib>}, 4.0.0 and higher
@license: This software is available for use under the U{W3C Software License<http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231>}
@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}

"""

__author__  = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = 'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

from RDFClosure.RDFS 	import Property, type
from RDFClosure.RDFS 	import Resource, Class, subClassOf, subPropertyOf, domain, range
from RDFClosure.RDFS 	import Literal, ContainerMembershipProperty, member, Datatype
# noinspection PyPep8Naming
from RDFClosure.RDFS 	import RDFNS as ns_rdf

from RDFClosure.Closure          import Core
from RDFClosure.AxiomaticTriples import RDFS_Axiomatic_Triples, RDFS_D_Axiomatic_Triples


######################################################################################################

## RDFS Semantics class
# noinspection PyPep8Naming
class RDFS_Semantics(Core):
	"""RDFS Semantics class, ie, implementation of the RDFS closure graph.

	Note that the module does I{not} implement the so called Datatype entailment rules, simply because the underlying RDFLib does
	not implement the datatypes (ie, RDFLib will not make the literal "1.00" and "1.00000" identical, although
	even with all the ambiguities on datatypes, this I{should} be made equal...). Also, the so-called extensional entailment rules
	(Section 7.3.1 in the RDF Semantics document) have not been implemented either.

	The comments and references to the various rule follow the names as used in the U{RDF Semantics document<http://www.w3.org/TR/rdf-mt/>}.
	"""
	def __init__(self, graph, axioms, daxioms, rdfs):
		"""
		@param graph: the RDF graph to be extended
		@type graph: rdflib.Graph
		@param axioms: whether (non-datatype) axiomatic triples should be added or not
		@type axioms: bool
		@param daxioms: whether datatype axiomatic triples should be added or not
		@type daxioms: bool
		@param rdfs: whether RDFS inference is also done (used in subclassed only)
		@type rdfs: boolean
		"""
		Core.__init__(self, graph, axioms, daxioms, rdfs)

	def add_axioms(self):
		"""Add axioms
		"""
		for t in RDFS_Axiomatic_Triples:
			self.graph.add(t)
		for i in range(1, self.IMaxNum + 1):
			ci = ns_rdf[("_%d" % i)]
			self.graph.add((ci, type, Property))
			self.graph.add((ci, domain, Resource))
			self.graph.add((ci, range, Resource))
			self.graph.add((ci, type, ContainerMembershipProperty))

	def add_d_axioms(self):
		"""This is not really complete, because it just uses the comparison possibilities that rdflib provides."""
		literals = list(self.literal_proxies.lit_to_bnode.keys())
		# #1
		for lt in literals:
			if lt.dt is not None:
				self.graph.add((self.literal_proxies.lit_to_bnode[lt], type, lt.dt))

		for t in RDFS_D_Axiomatic_Triples :
			self.graph.add(t)

	# noinspection PyBroadException
	def one_time_rules(self):
		"""Some of the rules in the rule set are axiomatic in nature, meaning that they really have to be added only
		once, there is no reason to add these in a cycle. These are performed by this method that is invoked only once
		at the beginning of the process.

		In this case this is related to a 'hidden' same as rules on literals with identical values (though different lexical values)
		"""
		# There is also a hidden sameAs rule in RDF Semantics: if a literal appears in a triple, and another one has the same value,
		# then the triple should be duplicated with the other value.
		for lt1 in list(self.literal_proxies.lit_to_bnode.keys()):
			for lt2 in list(self.literal_proxies.lit_to_bnode.keys()):
				if lt1 != lt2:
					try:
						lt1_d = lt1.lit.toPython()
						lt2_d = lt2.lit.toPython()
						if lt1_d == lt2_d :
							# In OWL, this line is simply stating a sameAs for the corresponding BNodes, and then let
							# the usual rules take effect. In RDFS this is not possible, so the sameAs rule is, essentially
							# replicated...
							bn1 = self.literal_proxies.lit_to_bnode[lt1]
							bn2 = self.literal_proxies.lit_to_bnode[lt2]
							for (s, p, o) in self.graph.triples((None, None, bn1)) :
								self.graph.add((s, p, bn2))
					except:
						# there may be a problem with one of the python conversions; the rule is imply ignored
						#raise e
						pass

	def rules(self,t,cycle_num):
		"""
			Go through the RDFS entailment rules rdf1, rdfs4-rdfs12, by extending the graph.
			@param t: a triple (in the form of a tuple)
			@param cycle_num: which cycle are we in, starting with 1. Can be used for some (though minor) optimization.
		"""
		s, p, o = t
		# rdf1
		self.store_triple((p, type, Property))
		# rdfs4a
		if cycle_num == 1:
			self.store_triple((s, type, Resource))
		# rdfs4b
		if cycle_num == 1:
			self.store_triple((o, type, Resource))
		if p == domain:
			# rdfs2
			for uuu, Y, yyy in self.graph.triples((None, s, None)):
				self.store_triple((uuu, type, o))
		if p == range:
			# rdfs3
			for uuu, Y, vvv in self.graph.triples((None, s, None)):
				self.store_triple((vvv, type, o))
		if p == subPropertyOf:
			# rdfs5
			for Z, Y, xxx in self.graph.triples((o, subPropertyOf, None)):
				self.store_triple((s, subPropertyOf, xxx))
			# rdfs7
			for zzz, Z, www in self.graph.triples((None, s, None)):
				self.store_triple((zzz, o, www))
		if p == type and o == Property:
			# rdfs6
			self.store_triple((s, subPropertyOf, s))
		if p == type and o == Class:
			# rdfs8
			self.store_triple((s, subClassOf, Resource))
			# rdfs10
			self.store_triple((s, subClassOf, s))
		if p == subClassOf:
			# rdfs9
			for vvv, Y, Z in self.graph.triples((None, type, s)):
				self.store_triple((vvv, type, o))
			# rdfs11
			for Z, Y, xxx in self.graph.triples((o, subClassOf, None)):
				self.store_triple((s, subClassOf, xxx))
		if p == type and o == ContainerMembershipProperty :
			# rdfs12
			self.store_triple((s, subPropertyOf, member))
		if p == type and o == Datatype:
			self.store_triple((s, subClassOf, Literal))



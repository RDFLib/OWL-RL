#!/d/Bin/Python/python.exe
# -*- coding: utf-8 -*-
#
"""
The combined closure: performing I{both} the OWL 2 RL and RDFS closures.
The two are very close but there are some rules in RDFS that are not in OWL 2 RL (eg, the axiomatic
triples concerning the container membership properties). Using this closure class the
OWL 2 RL implementation becomes a full extension of RDFS.

@requires: U{RDFLib<http://rdflib.net>}, 4.0.0 or higher
@license: This software is available for use under the U{W3C Software License<http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231>}
@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}

"""

__author__  = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = u'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

from RDFClosure.RDFS import Resource, Class, Datatype
from RDFClosure.OWL  import OWLClass, Thing, equivalentClass, DataRange

from RDFClosure.RDFSClosure import RDFS_Semantics
from RDFClosure.OWLRL       import OWLRL_Semantics

######################################################################################################


# noinspection PyPep8Naming
class RDFS_OWLRL_Semantics(RDFS_Semantics, OWLRL_Semantics):
	"""Common subclass of the RDFS and OWL 2 RL semantic classes. All methods simply call back
	to the functions in the superclasses. This may lead to some unnecessary duplication of terms
	and rules, but it it not so bad. Also, the additional identification defined for OWL Full,
	ie, Resource being the same as Thing and OWL and RDFS classes being identical are added to the
	triple store.
	
	Note that this class is also a possible user extension point: subclasses can be created that
	extend the standard functionality by extending this class. This class I{always} performs RDFS inferences.
	Subclasses have to set the C{self.rdfs} flag explicitly to the requested value if that is to be controlled.
	
	@ivar full_binding_triples: additional axiom type triples that are added to the combined semantics; these 'bind' the RDFS and the OWL worlds together
	@ivar rdfs: whether RDFS inference is to be performed or not. In this class instance the value is I{always} C{True}, subclasses may explicitly change it at initialization time.
	@type rdfs: boolean
	"""
	full_binding_triples = [
		(Thing, equivalentClass, Resource),
		(Class, equivalentClass, OWLClass),
		(DataRange, equivalentClass, Datatype)
	]

	def __init__(self, graph, axioms, daxioms, rdfs=True):
		"""
		@param graph: the RDF graph to be extended
		@type graph: rdflib.Graph
		@param axioms: whether (non-datatype) axiomatic triples should be added or not
		@type axioms: bool
		@param daxioms: whether datatype axiomatic triples should be added or not
		@type daxioms: bool
		@param rdfs: placeholder flag (used in subclassed only, it is always defaulted to True in this class)
		@type rdfs: boolean
		"""
		OWLRL_Semantics.__init__(self, graph, axioms, daxioms, rdfs)
		RDFS_Semantics.__init__(self, graph, axioms, daxioms, rdfs)
		self.rdfs = True

	# noinspection PyMethodMayBeStatic
	@staticmethod
	def add_new_datatype(uri, conversion_function, datatype_list, subsumption_dict=None, subsumption_key=None, subsumption_list=None):
		"""If an extension wants to add new datatypes, this method should be invoked at initialization time.
		
		@param uri : URI for the new datatypes, like owl_ns["Rational"]
		@param conversion_function : a function converting the lexical representation of the datatype to a Python value,
		possibly raising an exception in case of unsuitable lexical form
		@param datatype_list : list of datatypes already in use that has to be checked
		@param subsumption_dict : dictionary of subsumption hierarchies (indexed by the datatype URI-s)
		@param subsumption_key  : key in the dictionary, if None, the uri parameter is used
		@param subsumption_list : list of subsumptions associated to a subsumption key (ie, all datatypes that are superclasses of the new datatype)
		"""
		from DatatypeHandling import AltXSDToPYTHON, use_Alt_lexical_conversions
		
		if datatype_list:
			datatype_list.append(uri)
		
		if subsumption_dict and subsumption_list:
			if subsumption_key:
				subsumption_dict[subsumption_key] = subsumption_list
			else :
				subsumption_dict[uri] = subsumption_list
		
		AltXSDToPYTHON[uri] = conversion_function
		use_Alt_lexical_conversions()

	def post_process(self):
		"""Do some post-processing step. This method when all processing is done, but before handling possible
		errors (ie, the method can add its own error messages). By default, this method is empty, subclasses
		can add content to it by overriding it.
		"""
		OWLRL_Semantics.post_process(self)

	def rules(self, t, cycle_num):
		"""
		@param t: a triple (in the form of a tuple)
		@param cycle_num: which cycle are we in, starting with 1. This value is forwarded to all local rules; it is also used
		locally to collect the bnodes in the graph.
		"""
		OWLRL_Semantics.rules(self, t, cycle_num)
		if self.rdfs:
			RDFS_Semantics.rules(self, t, cycle_num)

	def add_axioms(self):
		if self.rdfs:
			RDFS_Semantics.add_axioms(self)
		OWLRL_Semantics.add_axioms(self)

	def add_d_axioms(self):
		if self.rdfs:
			RDFS_Semantics.add_d_axioms(self)
		OWLRL_Semantics.add_d_axioms(self)

	def one_time_rules(self):
		"""Adds some extra axioms and calls for the d_axiom part of the OWL Semantics."""
		for t in self.full_binding_triples:
			self.store_triple(t)

		# Note that the RL one time rules include the management of datatype which is a true superset
		# of the rules in RDFS. It is therefore unnecessary to add those even self.rdfs is True.
		OWLRL_Semantics.one_time_rules(self)


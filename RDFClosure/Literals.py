# -*- coding: utf-8 -*-
#
"""
Separate module to handle literals. 

The issue is that pure literals cannot appear in subject position according to the current rules on RDF. That means that
different types of conclusions cannot properly finish. The present trick is trying to get around the problem as follows:

 1. For all literals in the graph a bnode is created. The module does not do a full D entailment but just relies on RDFLib's ability to recognize identical literals
 2. All those bnodes get a type Literal
 3. All triples with literals are exchanged against a triple with the associated bnode

The inferences are then calculated with the modified Graph. At the end of the process, the above steps are done backwards: for all triples where 
a bnode representing a literal appear in object position, a triple is generated; however, all triples where the bnode appears in a
subject position are removed from the final graph.


@requires: U{RDFLib<https://github.com/RDFLib/rdflib>}, 4.0.0 and higher
@license: This software is available for use under the U{W3C Software License<http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231>}
@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}

"""

__author__  = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = u'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

from rdflib import BNode
from rdflib import Literal as rdflibLiteral
from rdflib.namespace import XSD as ns_xsd

from .RDFS import type
from .RDFS import Literal
from .DatatypeHandling import AltXSDToPYTHON


class _LiteralStructure :
	"""This class serves as a wrapper around rdflib's Literal, by changing the equality function to a strict 
	identity of datatypes and lexical values.
	
	On the other hand, to implement, eg, OWL RL's datatype rules, a should be able to generate 
	an 'a sameAs b' triple, ie, the distinction should be kept. Hence this class that overrides the equality,
	and then can be used as a key in a Python dictionary.
	"""

	# noinspection PyPep8
	def __init__(self, lit) :
		self.lit   = lit
		self.lex   = str(lit)
		self.dt    = lit.datatype
		self.lang  = lit.language
		self.value = lit.value

#	def compare_value(self, other ) :
#		"""Compare to literal structure instances for equality. Here equality means in the sense of datatype values
#		@return: comparison result
#		@rtype: boolean
#		"""
#		try:
#			if self.dt == OWLNS["rational"] and other.dt == OWLNS["rational"] :
#				return self.value == other.value
#			elif self.dt == OWLNS["rational"] and other.dt != OWLNS["rational"] :
#				l = rdflibLiteral(float(self.lit._cmp_value))
#				return l == other.lit
#			elif self.dt != OWLNS["rational"] and other.dt == OWLNS["rational"] :
#				l = rdflibLiteral(float(other.lit._cmp_value))
#				return self.lit == l
#			else :
#				return self.lit == other.lit
#		except: 
#			# There might be conversion problems...
#			return False

	# noinspection PyBroadException
	def compare_value(self, other) :
		"""Compare to literal structure instances for equality. Here equality means in the sense of datatype values
		@return: comparison result
		@rtype: boolean
		"""
		try:
			return self.lit == other.lit
		except: 
			# There might be conversion problems...
			return False

	def __eq__(self, other) :
		if other is None :
			return False
		else :
			return self.lex == other.lex and self.dt == other.dt and self.lang == other.lang

	def __ne__(self, other) :
		return not self.__eq__(other)
		
	def __hash__(self) :
		if self.dt is not None :
			return hash(self.lit) ^ hash(self.dt)
		else :
			return hash(self.lit)
			
	def __repr__(self) :
		retval = ""
		retval += "lexical value: %s; " % self.lex
		retval += "datatype: %s; "      % self.dt
		retval += "language tag: %s; "  % self.lang
		return retval


class LiteralProxies :
	# noinspection PyPep8
	def __init__(self, graph, closure) :
		"""
		@param graph: the graph to be modified
		"""
		self.lit_to_bnode = {}
		self.bnode_to_lit = {}
		self.graph        = graph
		
		to_be_removed = []
		to_be_added   = []
		for t in self.graph :
			(subj, pred, obj) = t
			# This is supposed to be a "proper" graph, so only the obj may be a literal
			if isinstance(obj, rdflibLiteral):
				# Test the validity of the datatype
				if obj.datatype:
					try:
						AltXSDToPYTHON[obj.datatype](str(obj))
					except ValueError:
						closure.add_error("Lexical value of the literal '%s' does not match its datatype (%s)" % (str(obj), obj.datatype))

				# In any case, this should be removed:
				if t not in to_be_removed:
					to_be_removed.append(t)
				# Check if a BNode has already been associated with that literal
				obj_st = _LiteralStructure(obj)
				found = False
				for l in self.lit_to_bnode.keys() :					
					if obj_st.lex == l.lex and obj_st.dt == l.dt and obj_st.lang == l.lang :
						t1 = (subj, pred, self.lit_to_bnode[l])
						to_be_added.append(t1)
						found = True
						break
				if not found:
					# the bnode has to be created
					bn = BNode()
					# store this in the internal administration
					self.lit_to_bnode[obj_st] = bn
					self.bnode_to_lit[bn] = obj_st
					# modify the graph
					to_be_added.append((subj, pred, bn))
					to_be_added.append((bn, type, Literal))
					# Furthermore: a plain literal should be identified with a corresponding xsd:string and vice versa, 
					# cf, RDFS Semantics document
					if obj_st.dt is None and obj_st.lang is None:
						newLit = rdflibLiteral(obj_st.lex, datatype=ns_xsd["string"])
						new_obj_st = _LiteralStructure(newLit)
						new_obj_st.dt = ns_xsd["string"]
						bn2 = BNode()
						self.lit_to_bnode[new_obj_st] = bn2
						self.bnode_to_lit[bn2] = new_obj_st
						to_be_added.append((subj, pred, bn2))
						to_be_added.append((bn2, type, Literal))
					elif obj_st.dt == ns_xsd["string"]:
						newLit = rdflibLiteral(obj_st.lex, datatype=None)
						new_obj_st = _LiteralStructure(newLit)
						# new_obj_st = _LiteralStructure(obj) # Was this the correct one, or was this an old bug?
						new_obj_st.dt = None
						bn2 = BNode()
						self.lit_to_bnode[new_obj_st] = bn2
						self.bnode_to_lit[bn2] = new_obj_st
						to_be_added.append((subj, pred, bn2))
						to_be_added.append((bn2, type, Literal))
		
		# Do the real modifications
		self._massageGraph(to_be_removed, to_be_added)
		
	def restore(self) :
		"""
		This method is to be invoked at the end of the forward chain processing. It restores literals (whenever possible)
		to their original self...
		"""	
		to_be_removed = []
		to_be_added   = []
		for t in self.graph :
			(subj, pred, obj) = t
			# The two cases, namely when the literal appears in subject or object positions, should be treated differently
			if subj in self.bnode_to_lit :
				# well... there may be to cases here: either this is the original tuple stating that
				# this bnode is a literal, or it is the result of an inference. In both cases, the tuple must
				# be removed from the result without any further action
				if t not in to_be_removed:
					to_be_removed.append(t)
			elif obj in self.bnode_to_lit:
				# This is where the exchange should take place: put back the real literal into the graph, removing the proxy one
				if t not in to_be_removed:
					to_be_removed.append(t)
				# This is an additional thing due to the latest change of literal handling in RDF concepts.
				# If a literal is an xsd:string then a plain literal is put in its place for the purpose of serialization...
				lit = self.bnode_to_lit[obj].lit
				if lit.datatype is not None and lit.datatype == ns_xsd["string"]:
					lit = rdflibLiteral(str(lit))
				to_be_added.append((subj, pred, lit))
				
		# Do the real modifications
		self._massageGraph(to_be_removed, to_be_added)
		
	def _massageGraph(self, to_be_removed, to_be_added) :
		"""
		Perform the removal and addition actions on the graph
		@param to_be_removed: list of tuples to be removed
		@param to_be_added : list of tuples to be added
		"""
		for t in to_be_removed:
			self.graph.remove(t)
		for t in to_be_added:
			self.graph.add(t)
		
		
					


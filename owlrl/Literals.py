# -*- coding: utf-8 -*-
#
"""
Separate module to handle literals. 

The issue is that pure literals cannot appear in subject position according to the current rules on RDF. That means that
different types of conclusions cannot properly finish. The present trick is trying to get around the problem as follows:

#. For all literals in the graph a bnode is created. The module does not do a full D entailment but just relies on RDFLib's ability to recognize identical literals
#. All those bnodes get a type Literal
#. All triples with literals are exchanged against a triple with the associated bnode

The inferences are then calculated with the modified Graph. At the end of the process, the above steps are done
backwards: for all triples where a bnode representing a literal appear in object position, a triple is generated;
however, all triples where the bnode appears in a subject position are removed from the final graph.


**Requires**: `RDFLib`_, 4.0.0 and higher.

.. _RDFLib: https://github.com/RDFLib/rdflib

**License**: This software is available for use under the `W3C Software License`_.

.. _W3C Software License: http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231

**Organization**: `World Wide Web Consortium`_

.. _World Wide Web Consortium: http://www.w3.org

**Author**: `Ivan Herman`_

.. _Ivan Herman: http://www.w3.org/People/Ivan/
"""
__author__ = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = 'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

from functools import partial

from rdflib import BNode
from rdflib import Literal as rdflibLiteral
from rdflib.namespace import XSD as ns_xsd

from .RDFS import rdf_type
from .RDFS import Literal
from .DatatypeHandling import AltXSDToPYTHON


identity = lambda v: v


class _LiteralStructure:
    """
    This class serves as a wrapper around rdflib's Literal, by changing the equality function to a strict
    identity of datatypes and lexical values.
    
    On the other hand, to implement, eg, OWL RL's datatype rules, a should be able to generate 
    an 'a sameAs b' triple, ie, the distinction should be kept. Hence this class that overrides the equality,
    and then can be used as a key in a Python dictionary.
    """

    # noinspection PyPep8
    def __init__(self, lit):
        self.lit = lit
        self.lex = str(lit)
        self.dt = lit.datatype
        self.lang = lit.language
        self.value = lit.value

#    def compare_value(self, other ):
#        """Compare to literal structure instances for equality. Here equality means in the sense of datatype values
#        @return: comparison result
#        @rtype: boolean
#        """
#        try:
#            if self.dt == OWLNS["rational"] and other.dt == OWLNS["rational"]:
#                return self.value == other.value
#            elif self.dt == OWLNS["rational"] and other.dt != OWLNS["rational"]:
#                l = rdflibLiteral(float(self.lit._cmp_value))
#                return l == other.lit
#            elif self.dt != OWLNS["rational"] and other.dt == OWLNS["rational"]:
#                l = rdflibLiteral(float(other.lit._cmp_value))
#                return self.lit == l
#            else:
#                return self.lit == other.lit
#        except: 
#            # There might be conversion problems...
#            return False

    # noinspection PyBroadException
    def compare_value(self, other):
        """Compare to literal structure instances for equality. Here equality means in the sense of datatype values
        @return: comparison result
        @rtype: boolean
        """
        try:
            return self.lit == other.lit
        except: 
            # There might be conversion problems...
            return False

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.lex == other.lex and self.dt == other.dt and self.lang == other.lang

    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __hash__(self):
        if self.dt is not None:
            return hash(self.lit) ^ hash(self.dt)
        else:
            return hash(self.lit)
            
    def __repr__(self):
        retval = ""
        retval += "lexical value: %s; " % self.lex
        retval += "datatype: %s; " % self.dt
        retval += "language tag: %s; " % self.lang
        return retval


class LiteralProxies:
    # noinspection PyPep8
    """

    :param graph: The graph to be modified.
    :param closure: ..
    """
    def __init__(self, graph, closure):
        """
        @param graph: the graph to be modified
        """
        self.lit_to_bnode = {}
        self.bnode_to_lit = {}
        self.graph = graph
        
        to_be_added = set()
        _add_bnode = partial(add_bnode, self, to_be_added)

        # This is supposed to be a "proper" graph, so get the triples which
        # object is a literal. All of them will be removed from graph and
        # replaced with the ones stored in `to_be_added` variable.
        to_be_removed = [t for t in self.graph if isinstance(t[2], rdflibLiteral)]
        for t in to_be_removed:
            (subj, pred, obj) = t
            # Test the validity of the datatype
            if obj.datatype:
                converter = AltXSDToPYTHON.get(obj.datatype, identity)
                try:
                    converter(str(obj))
                except ValueError:
                    closure.add_error("Lexical value of the literal '%s' does not match its datatype (%s)" %
                                      (str(obj), obj.datatype))

            # Check if a BNode has already been associated with that literal
            obj_st = _LiteralStructure(obj)
            items = (b for l, b in self.lit_to_bnode.items() if l == obj_st)
            l_bnode = next(items, None)
            if l_bnode:
                to_be_added.add((subj, pred, l_bnode))
            else:
                _add_bnode(subj, pred, obj_st)
                # Furthermore: a plain literal should be identified with a corresponding xsd:string and vice versa, 
                # cf, RDFS Semantics document
                if obj_st.dt is None and obj_st.lang is None:
                    newLit = rdflibLiteral(obj_st.lex, datatype=ns_xsd["string"])
                    new_obj_st = _LiteralStructure(newLit)
                    new_obj_st.dt = ns_xsd["string"]
                    _add_bnode(subj, pred, new_obj_st)
                elif obj_st.dt == ns_xsd["string"]:
                    newLit = rdflibLiteral(obj_st.lex, datatype=None)
                    new_obj_st = _LiteralStructure(newLit)
                    # new_obj_st = _LiteralStructure(obj) # Was this the correct one, or was this an old bug?
                    new_obj_st.dt = None
                    _add_bnode(subj, pred, new_obj_st)
        
        # Do the real modifications
        self._massageGraph(to_be_removed, to_be_added)
        
    def restore(self):
        """
        This method is to be invoked at the end of the forward chain processing. It restores literals (whenever
        possible) to their original self...
        """    
        to_be_removed = set()
        to_be_added = set()
        for t in self.graph:
            (subj, pred, obj) = t
            # The two cases, namely when the literal appears in subject or object positions, should be treated
            # differently
            if subj in self.bnode_to_lit:
                # well... there may be to cases here: either this is the original tuple stating that
                # this bnode is a literal, or it is the result of an inference. In both cases, the tuple must
                # be removed from the result without any further action
                to_be_removed.add(t)
            elif obj in self.bnode_to_lit:
                # This is where the exchange should take place: put back the real literal into the graph, removing the
                # proxy one
                to_be_removed.add(t)
                # This is an additional thing due to the latest change of literal handling in RDF concepts.
                # If a literal is an xsd:string then a plain literal is put in its place for the purpose of
                # serialization...
                lit = self.bnode_to_lit[obj].lit
                if lit.datatype is not None and lit.datatype == ns_xsd["string"]:
                    lit = rdflibLiteral(str(lit))
                to_be_added.add((subj, pred, lit))
                
        # Do the real modifications
        self._massageGraph(to_be_removed, to_be_added)
        
    def _massageGraph(self, to_be_removed, to_be_added):
        """
        Perform the removal and addition actions on the graph
        @param to_be_removed: list of tuples to be removed
        @param to_be_added: list of tuples to be added
        """
        for t in to_be_removed:
            self.graph.remove(t)
        for t in to_be_added:
            self.graph.add(t)


def add_bnode(proxy, to_be_added, subj, pred, obj):
    """
    Create and add BNode for a literal and register the new object within
    the :class:`.LiteralProxies` class data structures.
    """
    bn = BNode()
    # store this in the internal administration
    proxy.lit_to_bnode[obj] = bn
    proxy.bnode_to_lit[bn] = obj
    # modify the graph
    to_be_added.add((subj, pred, bn))
    to_be_added.add((bn, rdf_type, Literal))

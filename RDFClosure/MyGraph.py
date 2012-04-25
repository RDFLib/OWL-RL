# -*- coding: utf-8 -*-
"""
Wrapper around RDFLib's Graph object. The issue is that, in RDFLib 2.X, the turtle and the RDF/XML serialization has some issues (bugs and ugly output). There are also issues with the turtle parser. As a result, the package’s own serializers and turtle parser (which are all minor improvements over the shipped serializers and parser, not a full re-write) should be registered and used. On the  RDFLib 3.X some of these become unnecessary, but, for example, the turtle serializer has to have its own version, too.

This wrapper provides a subclass of RDFLib’s Graph overriding the serialize method to register, if necessary, a different serializer and use that one.

@summary: Shell around RDLib's Graph
@requires: Python version 2.5 or up
@requires: U{RDFLib<http://rdflib.net>}
@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}
@license: This software is available for use under the
U{W3C® SOFTWARE NOTICE AND LICENSE<href="http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231">}

@var _bindings: Default bindings. This is just for the beauty of things: bindings are added to the graph to make the output nicer. If this is not done, RDFlib defines prefixes like "_1:", "_2:" which is, though correct, ugly…
"""

"""
$Id: MyGraph.py,v 1.1 2011/08/04 12:41:57 ivan Exp $ $Date: 2011/08/04 12:41:57 $

"""

__version__ = "3.0"
__author__  = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = u'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

import rdflib
if rdflib.__version__ >= "3.0.0" :
	from rdflib	import Graph
else :
	from rdflib.Graph import ConjunctiveGraph as Graph
	
from rdflib	import Namespace

_xml_serializer_name	= "my-rdfxml-serializer"
_turtle_serializer_name	= "my-turtle-serializer"
_turtle_parser_name     = "my-turtle-parser"

#########################################################################################################
class MyGraph(Graph) :
	"""
	Wrapper around RDFLib's Graph object. The issue is that the serializers and parsers in RDFLib are buggy:-(
	
	In RDFLib 2.X both the Turtle and the RDF/XML serializations have issues (bugs and ugly output), as well
	as the turtle parser. In RDFLib 3.X
	the Turtle serialization and parsers seem to be fine, but the RDF/XML has problems:-(
	
	This wrapper provides a subclass of RDFLib’s Graph overriding the serialize method to register,
	if necessary, a different serializer and use that one.

	@cvar xml_serializer_registered_2: flag to avoid duplicate registration for RDF/XML for rdflib 2.*
	@type xml_serializer_registered_2: boolean
	@cvar xml_serializer_registered_3: flag to avoid duplicate registration for RDF/XML for rdflib 3.*
	@type xml_serializer_registered_3: boolean
	@cvar turtle_serializer_registered_2: flag to avoid duplicate registration for Turtle for rdflib 2.*
	@type turtle_serializer_registered_2: boolean
	@cvar turtle_parser_registered_2: flag to avoid duplicate registration for Turtle for rdflib 2.*
	@type turtle_parser_registered_2: boolean
	"""
	xml_serializer_registered_2		= False
	xml_serializer_registered_3		= False
	turtle_serializer_registered_2	= False
	turtle_serializer_registered_3	= False
	turtle_parser_registered_2		= False
	
	def __init__(self) :
		Graph.__init__(self)

	def _register_XML_serializer_3(self) :
		"""The default XML Serializer of RDFLib 3.X is buggy, mainly when handling lists. An L{own version<serializers.PrettyXMLSerializer_3>} is
		registered in RDFlib and used in the rest of the package. 
		"""
		if not MyGraph.xml_serializer_registered_3 :
			from rdflib.plugin import register
			from rdflib.serializer import Serializer
			register(_xml_serializer_name, Serializer,
					 "RDFClosure.serializers.PrettyXMLSerializer_3", "PrettyXMLSerializer")
			MyGraph.xml_serializer_registered_3 = True
				
	def _register_XML_serializer_2(self) :
		"""The default XML Serializer of RDFLib 2.X is buggy, mainly when handling lists.
		An L{own version<serializers.PrettyXMLSerializer>} is
		registered in RDFlib and used in the rest of the package. This is not used for RDFLib 3.X.
		"""
		if not MyGraph.xml_serializer_registered_2 :
			from rdflib.plugin import register
			from rdflib.syntax import serializer, serializers
			register(_xml_serializer_name, serializers.Serializer,
					 "RDFClosure.serializers.PrettyXMLSerializer", "PrettyXMLSerializer")
			MyGraph.xml_serializer_registered_2 = True

	def _register_Turtle_serializer_2(self) :
		"""The default Turtle Serializers of RDFLib 2.X is buggy and not very nice as far as the output is concerned.
		An L{own version<serializers.TurtleSerializer>} is registered in RDFLib and used in the rest of the package.
		This is not used for RDFLib 3.X.
		"""
		if not MyGraph.turtle_serializer_registered_2 :
			from rdflib.plugin import register
			from rdflib.syntax import serializer, serializers
			register(_turtle_serializer_name, serializers.Serializer,
					 "RDFClosure.serializers.TurtleSerializer", "TurtleSerializer")
			MyGraph.turtle_serialzier_registered_2 = True

	def _register_Turtle_serializer_3(self) :
		"""The default Turtle Serializers of RDFLib 2.X is buggy and not very nice as far as the output is concerned.
		An L{own version<serializers.TurtleSerializer>} is registered in RDFLib and used in the rest of the package.
		This is not used for RDFLib 3.X.
		"""
		if not MyGraph.turtle_serializer_registered_3 :
			from rdflib.plugin import register
			from rdflib.serializer import Serializer
			register(_turtle_serializer_name, Serializer,
					 "RDFClosure.serializers.TurtleSerializer_3", "TurtleSerializer")
			MyGraph.turtle_serialzier_registered_3 = True
			
	def _register_Turtle_parser_2(self) :
		"""The default Turtle parser of RDFLib 2.X is buggy: some constants, like 'true' or 'false', are not handled.
		An L{own version<serializers.TurtleSerializer>} is registered in RDFLib and used in the rest of the package.
		This is not used for RDFLib 3.X.
		"""
		if not MyGraph.turtle_parser_registered_2 :
			from rdflib.plugin import register
			from rdflib.syntax 	import parsers
			register(_turtle_parser_name, parsers.Parser, "RDFClosure.parsers.N3Parser","N3Parser")
			MyGraph.turtle_parser_registered_2 = True
			
	def add(self, (s,p,o)) :
		"""Overriding the Graph's add method to filter out triples with possible None values. It may happen
		in case, for example, a host language is not properly set up for the distiller"""
		if s == None or p == None or o == None :
			return
		else :
			Graph.add(self,(s,p,o))
		
	def serialize(self, format = "xml") :
		"""Overriding the Graph's serialize method to adjust the output format"""
		if rdflib.__version__ >= "3.0.0" :
			# this is the easy case
			if format == "xml" or format == "pretty-xml" :
				self._register_XML_serializer_3()
				format = _xml_serializer_name
			elif format == "n3" or format == "turtle" :
				format = _turtle_serializer_name
				self._register_Turtle_serializer_3()
		else :
			if format == "pretty-xml" :
				self._register_XML_serializer_2()
				format = _xml_serializer_name
			elif format == "n3" or format == "turtle" :
				format = _turtle_serializer_name
				self._register_Turtle_serializer_2()
		return Graph.serialize(self, format=format)

	def parse(self, source=None, format="xml"):
		"""Overriding the Graph's serialize method to adjust the output format"""
		if rdflib.__version__ < "3.0.0" and (format == "n3" or format == "turtle") :
			self._register_Turtle_parser_2()
			format = _turtle_parser_name
		return Graph.parse(self, source=source, format=format)

"""
$Log: MyGraph.py,v $
Revision 1.1  2011/08/04 12:41:57  ivan
*** empty log message ***


"""

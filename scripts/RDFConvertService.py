#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
"""
Possible CGI entry point for the RDFClosure package.


@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}
@license: This software is available for use under the
U{W3C® SOFTWARE NOTICE AND LICENSE<href="http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231">}
@contact: Ivan Herman, ivan@w3.org
"""

"""
$Id: RDFConvertService.py,v 1.3 2009/07/10 08:45:14 ivan Exp $
"""

__version__ = "4.0"

import sys

import cgi
import cgitb; cgitb.enable()
form = cgi.FieldStorage()

if sys.platform == "win32" :
	# this is my local machine
	sys.path.insert(0,"C:\\Documents and Settings\\Ivan Herman\\My Documents\\W3C\\dev\\2004\\PythonLib-IH")
	sys.path.insert(0,"C:\\Documents and Settings\\Ivan Herman\\My Documents\\Lib\\Python")
	sys.path.insert(0,"C:\\Documents and Settings\\Ivan Herman\\My Documents\\Lib\\Python\\rdlib-2.4.2")

from RDFClosure import convert_graph, RDFXML, TURTLE, AUTO

##-----------------------------------------------------------------------------------------------------------------------------------
#
class Options:
	def __init__(self,form) :
		self.iformat 		= AUTO
		self.owlClosure		= "no"
		self.rdfsClosure 	= "no"
		self.owlExtras  	= "no"
		self.axioms 		= "no"
		self.daxioms 		= "no"		
		self.sources 		= []
		self.text 			= None
		self.format 		= TURTLE
		
		
		if "source_1" 		in list(form.keys()) 	: 	self.sources.append(form["source_1"].value)
		if "source_2" 		in list(form.keys()) 	: 	self.sources.append(form["source_2"].value)
		
		if "text" 			in list(form.keys()) 	: 	self.text = form["text"].value
		if "format" 		in list(form.keys())	:	self.format = form["format"].value
		if "iformat" 		in list(form.keys())	:	
			v = form["iformat"].value
			if v == "xml" or v == "turtle" : self.iformat = v	
			
		if "fullClosure" in list(form.keys()) and form["fullClosure"].value == "yes" :
			self.owlClosure  = "yes"
			self.rdfsClosure = "yes"
			self.axioms      = "no"
			self.daxioms     = "no"
			self.owlExtras   = "no"
		else :
			if "owlClosure" 	in list(form.keys())	:	self.owlClosure = form["owlClosure"].value
			if "rdfsClosure"	in list(form.keys())	:	self.rdfsClosure = form["rdfsClosure"].value
			if "owlExtras" 		in list(form.keys()) 	:	self.owlExtras = form["owlExtras"].value
			if "axioms" 		in list(form.keys()) 	:	self.axioms = form["axioms"].value
			if "daxioms" 		in list(form.keys()) 	:	self.daxioms = form["daxioms"].value

		# this one is for backward compatibility...
		if "uri" 			in list(form.keys()) 	: 	self.sources.append(form["uri"].value)		
		if "source" 		in list(form.keys()) 	: 	self.sources.append(form["source"].value)
		
	def to_HTML(self) :
		print('<dl>')
		
		print('<dt>Sources:</dt>')
		print('<dd>')
		if len(self.sources) == 0 :
			print("none")
		elif len(self.sources) == 1 :
			print(cgi.escape(self.sources[0]))
		else :		
			print(cgi.escape(self.sources[0]), ", ", cgi.escape(self.sources[1]))
		print('</dd>')
		
		print('<dt>Input format:</dt>')
		print('<dd>%s</dd>' % self.iformat)
		print('<dt>Output format:</dt><dd>%s</dd>' % self.format)
		print('<dt>OWL 2 RL Processing:</dt><dd>%s</dd>' % self.owlClosure)
		print('<dt>RDFS Processing:</dt><dd>%s</dd>' % self.rdfsClosure)
		print('<dt>Extra OWL Processing:</dt><dd>%s</dd>' % self.owlExtras)
		print('<dt>Axiomatic triples added:</dt><dd>%s</dd>' % self.axioms)
		print('<dt>Datatype Axiomatic triples added:</dt><dd>%s</dd>' % self.daxioms)
		if self.text != None: print('<dt>Turtle code added to the graph:</dt>')
		print('<dl>')
		if self.text != None :
			print(cgi.escape(self.text).replace('\n','<br/>'))

##-----------------------------------------------------------------------------------------------------------------------------------
options = Options(form)

try :
	retval = convert_graph(options)
	if options.format == TURTLE :
		print('Content-Type: text/turtle; charset=utf-8')
	else :
		print('Content-Type: application/rdf+xml; charset=utf-8')
	print()
	print(retval)
except :
	(type,value,traceback) = sys.exc_info()
	print('Content-type: text/html; charset=utf-8')
	print('Status: 400 Invalid Input')
	print()
	print("<html>")
	print("<head>")
	print("<title>Error in RDF Closure processing</title>")
	print("</head><body>")
	print("<h1>Error in RDF Closure processing:</h1>")
	print("<pre>%s</pre>" % value)
	print("<h1>For reference, the input arguments were:</h1>")
	options.to_HTML()
	print("</body>")
	print("</html>")

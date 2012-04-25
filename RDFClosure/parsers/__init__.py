# -*- coding: utf-8 -*-
"""
Parser module with a slightly improved versions of the Turtle parser.

The main issue is that the parser distributed by rdflib does not handle literals properly when they are not in quotes. Ie, for example,::
  <aaa> <bbbb> true .

is not recognized as:: 
  <aaa> <bbbb> "true"^^xsd:boolean .

The errors are:

 - Constants of the form 1234 should be interpreted as xsd integers, which is done correctly by the parser.
 - Constants of the form 1.2345 should be interpreted as xsd:decimal. Unfortunately, the original parser interprets them as xsd:double
 - Constants of the form 'true' or 'false' (whithout the quotes, that is) should be interpreted as xsd:boolean. Instead, they are put as symbols into the default namespace by the original parser.
 - Constants of the form 1.2345E12 should be interpreted as xsd:doubles. Unfortunately, the original parser crashes on those
 
This module provides an alternative parser that takes care of the first three problems.

Obviously, this parser can be used directly, too. Here is a way to do it::
  from rdflib.plugin import register
  from rdflib.syntax import parsers
  register("my_turtle", parsers.Parser, "RDFClosure.parsers.N3Parser","N3Parser")
  ...
  graph.parse(<file>,format="my_turtle")

	
@requires: U{RDFLib<http://rdflib.net>}, 2.2.2. and higher
@license: This software is available for use under the U{W3C Software License<http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231>}
@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}
"""

"""
$Id: __init__.py,v 1.2 2009/08/20 13:40:27 ivan Exp $ $Date: 2009/08/20 13:40:27 $
"""

__author__  = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = u'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

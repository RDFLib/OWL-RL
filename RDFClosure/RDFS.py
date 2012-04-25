"""
RDF(S) terms. Note that the set of terms is I{complete}, ie, it includes I{all} OWL 2 terms, regardless of whether the term is
used in OWL 2 RL or not.

@requires: U{RDFLib<http://rdflib.net>}, 2.2.2. and higher
@license: This software is available for use under the U{W3C Software License<http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231>}
@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}
"""

"""
$Id: RDFS.py,v 1.1 2011/08/04 12:41:58 ivan Exp $ $Date: 2011/08/04 12:41:58 $
"""

import rdflib
if rdflib.__version__ >= "3.0.0" :
	from rdflib				import Namespace
else :
	from rdflib.Namespace	import Namespace
	
RDFNS 		= Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFSNS 		= Namespace("http://www.w3.org/2000/01/rdf-schema#")

# RDF Classes
Seq 		= RDFNS["Seq"]
Bag 		= RDFNS["Bag"]
Alt 		= RDFNS["Alt"]
Statement 	= RDFNS["Statement"]
Property 	= RDFNS["Property"]
XMLLiteral 	= RDFNS["XMLLiteral"]
List 		= RDFNS["List"]

# RDF Properties
subject 	= RDFNS["subject"]
predicate 	= RDFNS["predicate"]
object 		= RDFNS["object"]
type 		= RDFNS["type"]
value 		= RDFNS["value"]
first 		= RDFNS["first"]
rest 		= RDFNS["rest"]
# and _n where n is a non-negative integer

# RDF Resources
nil 		= RDFNS["nil"]

Resource 					= RDFSNS["Resource"]
Class 						= RDFSNS["Class"]
subClassOf 					= RDFSNS["subClassOf"]
subPropertyOf 				= RDFSNS["subPropertyOf"]
comment 					= RDFSNS["comment"]
label 						= RDFSNS["label"]
domain 						= RDFSNS["domain"]
range 						= RDFSNS["range"]
seeAlso 					= RDFSNS["seeAlso"]
isDefinedBy				 	= RDFSNS["isDefinedBy"]
Literal 					= RDFSNS["Literal"]
Container			 		= RDFSNS["Container"]
ContainerMembershipProperty	= RDFSNS["ContainerMembershipProperty"]
member 						= RDFSNS["member"]
Datatype 					= RDFSNS["Datatype"]


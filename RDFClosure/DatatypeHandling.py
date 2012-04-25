#!/d/Bin/Python/python.exe
# -*- coding: utf-8 -*-
#
"""
Most of the XSD datatypes are handled directly by RDFLib. However, in some cases, that is not good enough. There are two
major reasons for this:

 1. Some datatypes are missing from RDFLib and required by OWL 2 RL and/or RDFS
 2. In other cases, though the datatype is present, RDFLib is fairly lax in checking the lexical value of those datatypes. Typical case is boolean.

Some of these defficiencies are handled by this module. All the functions convert the lexical value into a
python datatype (or return the original string if this is not possible) which will be used, eg,
for comparisons (equalities). If the lexical value constraints are not met, exceptions are raised.

@requires: U{RDFLib<http://rdflib.net>}, 2.2.2. and higher
@license: This software is available for use under the U{W3C Software License<http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231>}
@organization: U{World Wide Web Consortium<http://www.w3.org>}
@author: U{Ivan Herman<a href="http://www.w3.org/People/Ivan/">}
"""

"""
$Id: DatatypeHandling.py,v 1.9 2011/08/04 12:41:57 ivan Exp $ $Date: 2011/08/04 12:41:57 $
"""

__author__  = 'Ivan Herman'
__contact__ = 'Ivan Herman, ivan@w3.org'
__license__ = u'W3C® SOFTWARE NOTICE AND LICENSE, http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231'

import rdflib
from RDFClosure.RDFS 	import RDFNS as ns_rdf

if rdflib.__version__ >= "3.0.0" :
	from rdflib.term		import XSDToPython, Literal, _toPythonMapping, _PythonToXSD
	from rdflib.namespace 	import XSD as ns_xsd
else :
	from rdflib.Literal	import XSDToPython, Literal, _toPythonMapping, _PythonToXSD
	from rdflib.Literal import _XSD_NS as ns_xsd

import datetime, time, re

#: The Decimal type is available on python version 2.4 or higher. The flag is set whether the module can be imported or not
Decimal_available = True
try :
	from decimal import Decimal
except :
	Decimal_available = False

class _namelessTZ(datetime.tzinfo):
	"""(Nameless) timezone object. The python datetime object requires timezones as
	a specific object added to the conversion, rather than the explicit hour and minute
	difference used by XSD. This class is used to wrap around the hour/minute values.
	"""
	def __init__(self, hours, minutes):
		"""
		@param hours: hour offset
		@param minutes: minute offset
		"""
		self.__offset = datetime.timedelta(hours = hours, minutes = minutes)
		self.__name = "nameless"

	def utcoffset(self, dt):
		return self.__offset

	def tzname(self, dt):
		return self.__name

	def dst(self, dt):
		return datetime.timedelta(0)

def _returnTimeZone(incoming_v) :
	"""Almost all time/date related methods require the extraction of an optional time zone information.
	@param incoming_v: the time/date string
	@return (v,timezone) tuple; 'v' is the input string with the timezone info cut off, 'timezone' is a L{_namelessTZ} instance or None
	"""
	tzone = None
	if incoming_v[-1] == 'Z' :
		v     = incoming_v[:-1]
		tzone = _namelessTZ(0,0)
	else :
		pattern = ".*(\+|-)([0-9][0-9]):([0-9][0-9])"
		match  	= re.match(pattern,incoming_v)
		if match == None :
			v     = incoming_v
			tzone = None
		else :
			hours   = int(match.groups()[1])
			if match.groups()[0] == '-' : hours = -hours - 1
			minutes = int(match.groups()[2])
			v     = incoming_v[:-6]
			tzone = _namelessTZ(hours,minutes)
	return (v, tzone)


#################################### Booleans ##################################################
def _strToBool(v) :
	"""The built-in conversion to boolean is way too lax. The xsd specification requires that only true, false, 1 or 0 should be used...
	@param v: the literal string defined as boolean
	@return corresponding boolean value
	@raise ValueError: invalid boolean values
	"""
	if v.lower() == "true" or v.lower() == "1" :
		return bool(1)
	elif v.lower() == "false" or v.lower() == "0" :
		return bool(None)
	else :
		raise ValueError("Invalid boolean literal value %s" % v)


#################################### Decimals ##################################################
def _strToDecimal(v) :
	"""The built in datatype handling for RDFLib maps a decimal number to float, but the python version 2.4 and upwards also
	has a Decimal number. Better make use of that to use very high numbers.
	However, there is also a big difference between Python's decimal and XSD's decimal, because the latter does not allow
	for an exponential normal form (why???). This must be filtered out.
	@param v: the literal string defined as decimal
	@return Decimal if the local python version is >= 2.4, float otherwise
	@raise ValueError: invalid decimal value
	"""
	# check whether the lexical form of 'v' is o.k.
	if v.find('E') != -1 or v.find('e') != -1 :
		# this is an invalid lexical form, though would be accepted by Python
		raise ValueError("Invalid decimal literal value %s" %v)
	else :
		if Decimal_available :
			# this may raise further exceptions, which is fine
			return Decimal(v)
		else :
			# running an older version of python
			# this may raise further exceptions, which is fine
			return float(v)

#################################### ANY URIS ##################################################
#: set of characters allowed in a hexadecimal number
_hexc = ['A','B','C','D','E','F','a','b','c','d','e','f']
#: set of numerals
_numb = ['1','2','3','4','5','6','7','8','9','0']
def _strToAnyURI(v) :
	"""Rudimentary test for the AnyURI value. If it is a relative URI, then some tests are done to filter out
	mistakes. I am not sure this is the full implementation of the RFC, though, may have to be checked at some point
	later.
	@param v: the literal string defined as a URI
	@return the incoming value
	@raise ValueError: invalid URI value
	"""
	import urlparse
	if len(v) == 0 : return v
	if urlparse.urlsplit(v)[0] != "" :
		# this means that there is a proper scheme, the URI should be kosher
		return v
	else :
		# this is meant to be a relative URI.
		# If I am correct, that cannot begin with one or more "?" or ":" characters
		# all others are o.k.
		# if it begins with a % then it should be followed by two hexa charaters,
		# otherwise it is also a bug
		if v[0] == '%' :
			if len(v) >= 3 and (v[1] in _hexc or v[1] in _numb) and (v[2] in _hexc or v[2] in _numb) :
				return v
			else :
				raise ValueError("Invalid IRI %s" % v)
		elif v[0] == '?' or v[0] == ':' :
			raise ValueError("Invalid IRI %s" % v)
		else :
			return v

#################################### Base64Binary ##################################################
def _strToBase64Binary(v) :
	"""Rudimentary test for the base64Binary value. The problem is that the built-in b64 module functions ignore the
	fact that only a certain family of characters are allowed to appear in the lexical value, so this is checked first.
	@param v: the literal string defined as a base64encoded string
	@return the decoded (binary) content
	@raise ValueError: invalid base 64 binary value
	"""
	import base64
	if v.replace('=','x').replace('+','y').replace('/','z').isalnum() :
		try :
			return base64.standard_b64decode(v)
		except :
			raise ValueError("Invalid Base64Binary %s" % v)
	else :
		raise ValueError("Invalid Base64Binary %s" % v)

#################################### Numerical types ##################################################
#: limits for unsigned bytes
_limits_unsignedByte		= [-1, 256]

#: limits for bytes
_limits_byte				= [-129, 128]

#: limits for unsigned int
_limits_unsignedInt			= [-1, 4294967296]

#: limits for int
_limits_int					= [-2147483649, 2147483648]

#: limits for unsigned short
_limits_unsignedShort		= [-1, 65536]

#: limits for short
_limits_short				= [-32769, 32768]

#: limits for unsigned long
_limits_unsignedLong		= [-1, 18446744073709551616]

#: limits for long
_limits_long				= [-9223372036854775809, 9223372036854775808]

#: limits for positive integer
_limits_positiveInteger		= [0, None]

#: limits for non positive integer
_limits_nonPositiveInteger	= [None, 1]

#: limits for non negative ingteger
_limits_nonNegativeInteger	= [-1, None]

#: limits for negative ingteger
_limits_negativeInteger		= [None, 0]

def _strToBoundNumeral(v, interval, conversion) :
	"""Test (and convert) a generic numerical type, with a check against a lower and upper limit.
	@param v: the literal string to be converted
	@param interval: lower and upper bounds (non inclusive). If the value is None, no comparison should be done
	@param conversion: conversion function, ie, int, long, etc
	@raise ValueError: invalid value
	"""
	try :
		i = conversion(v)
		if (interval[0] == None or interval[0] < i) and (interval[1] == None or i < interval[1]) :
			return i
	except :
		pass
	raise ValueError("Invalid numerical value %s" % v)

#################################### Double and float ##################################################
def _strToDouble(v) :
	"""Test and convert a double value into a Decimal or float. Raises an exception if the number is outside the permitted
	range, ie, 1.0E+310 and 1.0E-330. To be on the safe side (python does not have double!) Decimals are used
	if possible. Upper and lower values, as required by xsd, are checked.

	@param v: the literal string defined as a double
	@return Decimal if the local python version is >= 2.4, float otherwise
	@raise ValueError: invalid value
	"""
	if Decimal_available :
		try :
			value = Decimal(v)
			avalue = abs(value)
			upper = Decimal("1.0E+310")
			lower = Decimal("1.0E-330")
			if lower < avalue and avalue < upper :
				# bingo
				return value
			else :
				raise ValueError("Invalid double %s" % v)
		except :
			# there was a problem in creating a decimal...
			raise ValueError("Invalid double %s" % v)
	else :
		# not much we can do, just convert to float. This will not be o.k., but will work on older python
		# installations...
		return float(v)

def _strToFloat(v) :
	"""Test and convert a float value into Decimal or (python) float. Raises an exception if the number is outside the
	permitted range, ie, 1.0E+40 and 1.0E-50.

	@param v: the literal string defined as a float
	@return Decimal if the local python version is >= 2.4, float otherwise
	@raise ValueError: invalid value
	"""
	if Decimal_available :
		try :
			value = Decimal(v)
			avalue = abs(value)
			upper = Decimal("1.0E+40")
			lower = Decimal("1.0E-50")
			if lower < avalue and avalue < upper :
				# bingo
				return value
			else :
				raise ValueError("Invalid float %s" % v)
		except :
			# there was a problem in creating a decimal...
			raise ValueError("Invalid float %s" % v)
	else :
		# it seems that the float range handled by python is larger than what is described in the spec
		# the stuff below may go wrong at the edges but nevertheless gives some check
		value = float(v)
		avalue = abs(value)
		if 1.0E-50 < avalue and avalue < 1.0E+40 :
			return value
		else:
			raise ValueError("Invalid float %s" % v)

#################################### hexa ##################################################
def _strToHexBinary(v) :
	"""Test (and convert) hexa integer values. The number of characters should be even.
	@param v: the literal string defined as a hexa number
	@return long value
	@raise ValueError: invalid value
	"""
	# first of all, the number of characters must be even according to the xsd spec:
	length = len(v)
	if (length/2)*2 != length :
		raise ValueError("Invalid hex binary number %s" % v)
	return long(v,16)

#################################### Datetime, datetimestamp, etc ################################

def _strToDateTimeAndStamp(incoming_v, timezone_required = False) :
	"""Test (and convert) datetime and datetimestamp values.
	@param incoming_v: the literal string defined as the date and time
	@param timezone_required: whether the timezone is required (ie, for datetimestamp) or not
	@return datetime
	@rtype: datetime.datetime
	@raise ValueError: invalid datetime or datetimestamp
	"""

	# First, handle the timezone portion, if there is any
	(v, tzone) = _returnTimeZone(incoming_v)

	# Check on the timezone. For timedatestamp object it is required
	if timezone_required and tzone == None :
		raise ValueError("Invalid datetime %s" % incoming_v)

	# The microseconds should be handled here...
	final_v     = v
	miliseconds = 0
	milpattern  = "(.*)(\.)([0-9]*)"
	match = re.match(milpattern, v)
	if match != None :
		# we have a milisecond portion...
		try :
			final_v = match.groups()[0]
			miliseconds = int(match.groups()[2])
		except :
			raise ValueError("Invalid datetime %s" % incoming_v)
	#
	# By now, the pattern should be clear
	# This may raise an exception...
	try :
		tstr = time.strptime(final_v,"%Y-%m-%dT%H:%M:%S")
		if tzone != None :
			return datetime.datetime(tstr.tm_year, tstr.tm_mon, tstr.tm_mday, tstr.tm_hour, tstr.tm_min, tstr.tm_sec, miliseconds, tzone)
		else :
			return datetime.datetime(tstr.tm_year, tstr.tm_mon, tstr.tm_mday, tstr.tm_hour, tstr.tm_min, tstr.tm_sec, miliseconds)
	except :
		raise ValueError("Invalid datetime %s" % incoming_v)

def _strToTime(incoming_v) :
	"""Test (and convert) time values.
	@param incoming_v: the literal string defined as time value
	@return time
	@rtype datetime.time
	@raise ValueError: invalid datetime or datetimestamp
	"""

	# First, handle the timezone portion, if there is any
	(v, tzone) = _returnTimeZone(incoming_v)

	# The microseconds should be handled here...
	final_v     = v
	miliseconds = 0
	milpattern  = "(.*)(\.)([0-9]*)"
	match = re.match(milpattern, v)
	if match != None :
		# we have a milisecond portion...
		try :
			final_v = match.groups()[0]
			miliseconds = int(match.groups()[2])
		except :
			raise ValueError("Invalid datetime %s" % incoming_v)
	#
	# By now, the pattern should be clear
	# This may raise an exception...
	try :
		tstr = time.strptime(final_v,"%H:%M:%S")
		if tzone != None :
			return datetime.time(tstr.tm_hour, tstr.tm_min, tstr.tm_sec, miliseconds, tzone)
		else :
			return datetime.time(tstr.tm_hour, tstr.tm_min, tstr.tm_sec, miliseconds)
	except :
		raise ValueError("Invalid time %s" % incoming_v)

def _strToDate(incoming_v) :
	"""Test (and convert) date values.
	@param incoming_v: the literal string defined as date (in iso format)
	@return date
	@return datetime.date
	@raise ValueError: invalid datetime or datetimestamp
	"""

	# First, handle the timezone portion, if there is any
	(final_v, tzone) = _returnTimeZone(incoming_v)

	# This may raise an exception...
	try :
		tstr = time.strptime(final_v,"%Y-%m-%d")
		return datetime.date(tstr.tm_year, tstr.tm_mon, tstr.tm_mday)
	except :
		raise ValueError("Invalid date %s" % incoming_v)

#################################### The 'g' series for dates ############################
# The 'g' datatatypes (eg, gYear) cannot be directly represented as a python datatype
# the series of methods below simply check whether the incoming string is o.k., but the
# returned value is the same as the original
def _strTogYearMonth(v) :
	"""Test gYearMonth value
	@param v: the literal string
	@return v
	@raise ValueError: invalid value
	"""
	try :
		time.strptime(v+"-01","%Y-%m-%d")
		return v
	except :
		raise ValueError("Invalid gYearMonth %s" % v)

def _strTogYear(v) :
	"""Test gYearMonth value
	@param v: the literal string
	@return v
	@raise ValueError: invalid value
	"""
	try :
		time.strptime(v+"-01-01","%Y-%m-%d")
		return v
	except :
		raise ValueError("Invalid gYear %s" % v)

def _strTogMonthDay(v) :
	"""Test gYearMonth value
	@param v: the literal string
	@return v
	@raise ValueError: invalid value
	"""
	try :
		time.strptime("2008-" + v,"%Y-%m-%d")
		return v
	except :
		raise ValueError("Invalid gMonthDay %s" % v)

def _strTogDay(v) :
	"""Test gYearMonth value
	@param v: the literal string
	@return v
	@raise ValueError: invalid value
	"""
	try :
		time.strptime("2001-01-" + v,"%Y-%m-%d")
		return v
	except :
		raise ValueError("Invalid gDay %s" % v)

def _strTogMonth(v) :
	"""Test gYearMonth value
	@param v: the literal string
	@return v
	@raise ValueError: invalid value
	"""
	try :
		time.strptime("2001-" + v + "-01","%Y-%m-%d")
		return v
	except :
		raise ValueError("Invalid gMonth %s" % v)

#################################### XML Literal #########################################
def _strToXMLLiteral(v) :
	"""Test (and convert) XML Literal values.
	@param v: the literal string defined as an xml literal
	@return the canonical version of the same xml text
	@raise ValueError: incorrect xml string
	"""
	import xml.dom.minidom
	try :
		dom = xml.dom.minidom.parseString(v)
		return dom.toxml()
	except :
		raise ValueError("Invalid XML Literal %s" % v)

#################################### language, NMTOKEN, NAME, etc #########################
#: regular expression for a 'language' datatype
_re_language = "[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*"

#: regexp for NMTOKEN. It must be used with a re.U flag (the '(?U' regexp form did not work. It may depend on the locale...)
_re_NMTOKEN 	= "[\w:_.\-]+"

#: characters not permitted at a starting position for Name (otherwise Name is like NMTOKEN
_re_Name_ex		= ['.','-'] + _numb

#: regexp for NCName. It must be used with a re.U flag (the '(?U' regexp form did not work. It may depend on the locale...)
_re_NCName 		= "[\w_.\-]+"

#: characters not permitted at a starting position for NCName
_re_NCName_ex	= ['.','-'] + _numb

def _strToVal_Regexp(v, regexp, flag = 0, excludeStart = []) :
	"""Test (and convert) a generic string type, with a check against a regular expression.
	@param v: the literal string to be converted
	@param regexp: the regular expression to check against
	@param flag: flags to be used in the regular expression
	@param excludeStart: array of characters disallowed in the first position
	@return original string
	@raise ValueError: invalid value
	"""
	match = re.match(regexp, v, flag)
	if match == None or match.end() != len(v) :
		raise ValueError("Invalid literal %s" % v)
	else :
		if len(excludeStart) > 0 and v[0] in excludeStart :
			raise ValueError("Invalid literal %s" % v)
		return v

#: Disallowed characters in a token or a normalized string, as a regexp
_re_token = "[^\n\t\r]+"

def _strToToken(v) :
	"""Test (and convert) a string to a token.
	@param v: the literal string to be converted
	@return original string
	@raise ValueError: invalid value
	"""
	if len(v) == 0 : return v
	# filter out the case when there are new lines and similar (if there is a problem, an exception is raised)
	_strToVal_Regexp(v, _re_token)
	v1 = ' '.join(v.strip().split())
	# normalize the string, and see if the result is the same:
	if len(v1) == len(v) :
		# no characters lost, ie, no unnecessary spaces
		return v
	else :
		raise ValueError("Invalid literal %s" % v)

#################################### plain literal ########################################
def _strToPlainLiteral(v) :
	"""Test (and convert) a plain literal
	@param v: the literal to be converted
	@return a new RDFLib Literal with language tag
	@raise ValueError: invalid value
	"""
	reg = "(.*)@([^@]*)"
	# a plain literal must match this regexp!
	match = re.match(reg,v)
	if match == None :
		raise ValueError("Invalid plain literal %s" % v)
	else :
		lit  = match.groups()[0]
		if len(match.groups()) == 1 or match.groups()[1] == "" :
			# no language tag
			lang = None
			return Literal(lit)
		else :
			lang = match.groups()[1]
			# check if this is a correct language tag. Note that can raise an exception!
			try :
				lang = _strToVal_Regexp(lang, _re_language)
				return Literal(lit,lang=lang.lower())
			except :
				raise ValueError("Invalid plain literal %s" % v)

#####################################################################################
#: Replacement of RDFLib's conversion function. Each entry assigns a function to an XSD datatype, attempting to convert a string to a Python datatype (or raise an exception if some problem is found)
AltXSDToPYTHON = {
	ns_xsd["language"]				: lambda v: _strToVal_Regexp(v, _re_language),
	ns_xsd["NMTOKEN"]				: lambda v: _strToVal_Regexp(v, _re_NMTOKEN, re.U),
	ns_xsd["Name"]					: lambda v: _strToVal_Regexp(v, _re_NMTOKEN, re.U, _re_Name_ex),
	ns_xsd["NCName"]				: lambda v: _strToVal_Regexp(v, _re_NCName, re.U, _re_NCName_ex),
	ns_xsd["token"]					: _strToToken,
	ns_rdf["PlainLiteral"]			: _strToPlainLiteral,
	ns_xsd["boolean"]				: _strToBool,
	ns_xsd["decimal"]				: _strToDecimal,
	ns_xsd["anyURI"]				: _strToAnyURI,
	ns_xsd["base64Binary"]			: _strToBase64Binary,
	ns_xsd["double"]				: _strToDouble,
	ns_xsd["float"]					: _strToFloat,
	ns_xsd["byte"]					: lambda v: _strToBoundNumeral(v, _limits_byte, int),
	ns_xsd["int"]					: lambda v: _strToBoundNumeral(v, _limits_int, long),
	ns_xsd["long"]					: lambda v: _strToBoundNumeral(v, _limits_long, long),
	ns_xsd["positiveInteger"]		: lambda v: _strToBoundNumeral(v, _limits_positiveInteger, long),
	ns_xsd["nonPositiveInteger"]	: lambda v: _strToBoundNumeral(v, _limits_nonPositiveInteger, long),
	ns_xsd["negativeInteger"]		: lambda v: _strToBoundNumeral(v, _limits_negativeInteger, long),
	ns_xsd["nonNegativeInteger"]	: lambda v: _strToBoundNumeral(v, _limits_nonNegativeInteger, long),
	ns_xsd["short"]					: lambda v: _strToBoundNumeral(v, _limits_short, int),
	ns_xsd["unsignedByte"]			: lambda v: _strToBoundNumeral(v, _limits_unsignedByte, int),
	ns_xsd["unsignedShort"]			: lambda v: _strToBoundNumeral(v, _limits_unsignedShort, int),
	ns_xsd["unsignedInt"]			: lambda v: _strToBoundNumeral(v, _limits_unsignedInt, long),
	ns_xsd["unsignedLong"]			: lambda v: _strToBoundNumeral(v, _limits_unsignedLong, long),
	ns_xsd["hexBinary"]				: _strToHexBinary,
	ns_xsd["dateTime"]				: lambda v: _strToDateTimeAndStamp(v, False),
	ns_xsd["dateTimeStamp"]			: lambda v: _strToDateTimeAndStamp(v, True),
	ns_rdf["XMLLiteral"]			: _strToXMLLiteral,
	ns_xsd["integer"]				: long,
	ns_xsd["string"]				: lambda v: v,
	ns_xsd["normalizedString"]		: lambda v: _strToVal_Regexp(v, _re_token),

	# These are RDFS specific...
	ns_xsd["time"]					: _strToTime,
	ns_xsd["date"]					: _strToDate,
	ns_xsd["gYearMonth"]			: _strTogYearMonth,
	ns_xsd["gYear"]					: _strTogYear,
	ns_xsd["gMonthDay"]				: _strTogMonthDay,
	ns_xsd["gDay"]					: _strTogDay,
	ns_xsd["gMonth"]				: _strTogMonth,
}

def use_Alt_lexical_conversions() :
	"""Registering the datatypes item for RDFLib, ie, bind the dictionary values. The 'bind' method of RDFLib adds
	extra datatypes to the registered ones in RDFLib, though the table used here (ie, L{AltXSDToPYTHON}) actually overrides
	all of the default conversion routines. The method also add a Decimal entry to the PythonToXSD array of RDFLib.
	"""
	_toPythonMapping.update(AltXSDToPYTHON)
	if Decimal_available :
		# at some point in type, this structure has changed in rdflib...
		import types
		if isinstance(_PythonToXSD,types.DictType) :
			_PythonToXSD[Decimal] = (None,ns_xsd[u'decimal'])
		else :
			_PythonToXSD.append((Decimal,(None,ns_xsd[u'decimal'])))

def use_RDFLib_lexical_conversions() :
	"""Restore the original (ie, RDFLib) set of lexical conversion routines.
	"""
	_toPythonMapping.update(XSDToPython)

#######################################################################################
# This module can pretty much tested individually...
if __name__ == '__main__' :
	import sys
	string   = sys.argv[1]
	datatype = ns_xsd["gMonth"]
	result = AltXSDToPYTHON[datatype](string)
	print type(result)
	print result







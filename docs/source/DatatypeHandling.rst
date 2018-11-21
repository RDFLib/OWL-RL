DatatypeHandling
================

.. automodule:: RDFClosure.DatatypeHandling
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:


AltXSDToPYTHON Table
--------------------

.. code-block:: python

    AltXSDToPYTHON = {
        ns_xsd["language"]: lambda v: _strToVal_Regexp(v, _re_language),
        ns_xsd["NMTOKEN"]: lambda v: _strToVal_Regexp(v, _re_NMTOKEN, re.U),
        ns_xsd["Name"]: lambda v: _strToVal_Regexp(v, _re_NMTOKEN, re.U, _re_Name_ex),
        ns_xsd["NCName"]: lambda v: _strToVal_Regexp(v, _re_NCName, re.U, _re_NCName_ex),
        ns_xsd["token"]: _strToToken,
        ns_rdf["PlainLiteral"]: _strToPlainLiteral,
        ns_xsd["boolean"]: _strToBool,
        ns_xsd["decimal"]: _strToDecimal,
        ns_xsd["anyURI"]: _strToAnyURI,
        ns_xsd["base64Binary"]: _strToBase64Binary,
        ns_xsd["double"]: _strToDouble,
        ns_xsd["float"]: _strToFloat,
        ns_xsd["byte"]: lambda v: _strToBoundNumeral(v, _limits_byte, int),
        ns_xsd["int"]: lambda v: _strToBoundNumeral(v, _limits_int, int),
        ns_xsd["long"]: lambda v: _strToBoundNumeral(v, _limits_long, int),
        ns_xsd["positiveInteger"]: lambda v: _strToBoundNumeral(v, _limits_positiveInteger, int),
        ns_xsd["nonPositiveInteger"]: lambda v: _strToBoundNumeral(v, _limits_nonPositiveInteger, int),
        ns_xsd["negativeInteger"]: lambda v: _strToBoundNumeral(v, _limits_negativeInteger, int),
        ns_xsd["nonNegativeInteger"]: lambda v: _strToBoundNumeral(v, _limits_nonNegativeInteger, int),
        ns_xsd["short"]: lambda v: _strToBoundNumeral(v, _limits_short, int),
        ns_xsd["unsignedByte"]: lambda v: _strToBoundNumeral(v, _limits_unsignedByte, int),
        ns_xsd["unsignedShort"]: lambda v: _strToBoundNumeral(v, _limits_unsignedShort, int),
        ns_xsd["unsignedInt"]: lambda v: _strToBoundNumeral(v, _limits_unsignedInt, int),
        ns_xsd["unsignedLong"]: lambda v: _strToBoundNumeral(v, _limits_unsignedLong, int),
        ns_xsd["hexBinary"]: _strToHexBinary,
        ns_xsd["dateTime"]: lambda v: _strToDateTimeAndStamp(v, False),
        ns_xsd["dateTimeStamp"]: lambda v: _strToDateTimeAndStamp(v, True),
        ns_rdf["XMLLiteral"]: _strToXMLLiteral,
        ns_xsd["integer"]: int,
        ns_xsd["string"]: lambda v: v,
        ns_rdf["HTML"]: lambda v: v,
        ns_xsd["normalizedString"]: lambda v: _strToVal_Regexp(v, _re_token),

        # These are RDFS specific...
        ns_xsd["time"]: _strToTime,
        ns_xsd["date"]: _strToDate,
        ns_xsd["gYearMonth"]: _strTogYearMonth,
        ns_xsd["gYear"]: _strTogYear,
        ns_xsd["gMonthDay"]: _strTogMonthDay,
        ns_xsd["gDay"]: _strTogDay,
        ns_xsd["gMonth"]: _strTogMonth,
    }
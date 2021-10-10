DatatypeHandling
================

.. automodule:: owlrl.DatatypeHandling
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:


AltXSDToPYTHON Table
--------------------

.. note:: The code below is not extracted automatically from the source code.

    If there are any errors, please make a pull request or an issue: https://github.com/RDFLib/OWL-RL

.. code-block:: python

    AltXSDToPYTHON = {
        XSD.language: lambda v: _strToVal_Regexp(v, _re_language),
        XSD.NMTOKEN: lambda v: _strToVal_Regexp(v, _re_NMTOKEN, re.U),
        XSD.Name: lambda v: _strToVal_Regexp(v, _re_NMTOKEN, re.U, _re_Name_ex),
        XSD.NCName: lambda v: _strToVal_Regexp(v, _re_NCName, re.U, _re_NCName_ex),
        XSD.token: _strToToken,
        RDF.plainLiteral: _strToPlainLiteral,
        XSD.boolean: _strToBool,
        XSD.decimal: _strToDecimal,
        XSD.anyURI: _strToAnyURI,
        XSD.base64Binary: _strToBase64Binary,
        XSD.double: _strToDouble,
        XSD.float: _strToFloat,
        XSD.byte: lambda v: _strToBoundNumeral(v, _limits_byte, int),
        XSD.int: lambda v: _strToBoundNumeral(v, _limits_int, int),
        XSD.long: lambda v: _strToBoundNumeral(v, _limits_long, int),
        XSD.positiveInteger: lambda v: _strToBoundNumeral(v, _limits_positiveInteger, int),
        XSD.nonPositiveInteger: lambda v: _strToBoundNumeral(v, _limits_nonPositiveInteger, int),
        XSD.negativeInteger: lambda v: _strToBoundNumeral(v, _limits_negativeInteger, int),
        XSD.nonNegativeInteger: lambda v: _strToBoundNumeral(v, _limits_nonNegativeInteger, int),
        XSD.short: lambda v: _strToBoundNumeral(v, _limits_short, int),
        XSD.unsignedByte: lambda v: _strToBoundNumeral(v, _limits_unsignedByte, int),
        XSD.unsignedShort: lambda v: _strToBoundNumeral(v, _limits_unsignedShort, int),
        XSD.unsignedInt: lambda v: _strToBoundNumeral(v, _limits_unsignedInt, int),
        XSD.unsignedLong: lambda v: _strToBoundNumeral(v, _limits_unsignedLong, int),
        XSD.hexBinary: _strToHexBinary,
        XSD.dateTime: lambda v: _strToDateTimeAndStamp(v, False),
        XSD.dateTimeStamp: lambda v: _strToDateTimeAndStamp(v, True),
        RDF.XMLLiteral: _strToXMLLiteral,
        XSD.integer: int,
        XSD.string: lambda v: v,
        RDF.HTML: lambda v: v,
        XSD.normalizedString: lambda v: _strToVal_Regexp(v, _re_token),

        # These are RDFS specific...
        XSD.time: _strToTime,
        XSD.date: _strToDate,
        XSD.gYearMonth: _strTogYearMonth,
        XSD.gYear: _strTogYear,
        XSD.gMonthDay: _strTogMonthDay,
        XSD.gDay: _strTogDay,
        XSD.gMonth: _strTogMonth,
    }

.. seealso:: View the source code :ref:`DatatypeHandling`.
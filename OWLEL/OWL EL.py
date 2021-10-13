import sys
import io
if sys.version_info < (3, 4, ):
    raise RuntimeError("This version of owl-el cannot be used in python < 3.4")
# noinspection PyPackageRequirements,PyPackageRequirements,PyPackageRequirements
import rdflib

from rdflib import Literal as rdflibLiteral
# noinspection PyPep8Naming
from rdflib import Graph

from . import DatatypeHandling, Closure
from .OWLELExtras import OWLEL_Extension, OWLEL_Extension_Trimming
from .OWLEL import OWLEL_Semantics
from .RDFSClosure import RDFS_Semantics
from .CombinedClosure import RDFS_OWLEL_Semantics
from .OWL import imports

################################################################################################################
RDFXML = "xml"
TURTLE = "turtle"
JSON   = "json"
AUTO   = "auto"
RDFA   = "rdfa"

NONE = "none"
RDF  = "rdf"
RDFS = "rdfs"
OWL  = "owl"
FULL = "full"

try:
    from rdflib_jsonld.parser import JsonLDParser
    from rdflib_jsonld.serializer import JsonLDSerializer
    from rdflib.plugin import register, Serializer, Parser
    register('json-ld', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')
    register('json-ld', Serializer, 'rdflib_jsonld.serializer', 'JsonLDSerializer')
    json_ld_available = True
except:
    json_ld_available = False


################################################################################################################

# noinspection PyShadowingBuiltins
def __parse_input(iformat, inp, graph):
    """Parse the input into the graph, possibly checking the suffix for the format.
    @param iformat: input format; can be one of L{AUTO}, L{TURTLE}, or L{RDFXML}. L{AUTO} means that the suffix of the
    file name or URI will decide: '.ttl' means Turtle, RDF/XML otherwise.
    @param inp: input file; anything that RDFLib accepts in that position (URI, file name, file object). If '-',
    standard input is used.
    @param graph: the RDFLib Graph instance to parse into.
    """
    if iformat == AUTO:
        if inp == "-":
            format = "turtle"
        else:
            if inp.endswith('.ttl') or inp.endswith('.n3'):
                format = "turtle"
            elif json_ld_available and (inp.endswith('.json') or inp.endswith('.jsonld')):
                format = "json-ld"
            elif inp.endswith('.html'):
                format = "rdfa1.1"
            else:
                format = "xml"
    elif iformat == TURTLE:
        format = "n3"
    elif iformat == RDFA:
        format = "rdfa1.1"
    elif iformat == RDFXML:
        format = "xml"
    elif iformat == JSON:
        if json_ld_available:
            format = "json-ld"
        else:
            raise Exception("JSON-LD parser is not available")
    else:
        raise Exception("Unknown input syntax")

    if inp == "-":
        # standard input is used
        import sys
        source = sys.stdin
    else:
        source = inp
    graph.parse(source, format=format)


def interpret_owl_imports(iformat, graph):
    """
    Interpret the owl import statements. Essentially, recursively merge with all the objects in the owl import
    statement, and remove the corresponding triples from the graph.
    This method can be used by an application prior to expansion. It is *not* done by the the :class:`.DeductiveClosure`
    class.
    :param iformat: Input format; can be one of :code:`AUTO`, :code:`TURTLE`, or :code:`RDFXML`. :code:`AUTO` means that
    the suffix of the file name or URI will decide: '.ttl' means Turtle, RDF/XML otherwise.
    :type iformat: str
    :param graph: The RDFLib Graph instance to parse into.
    :type graph: :class:`RDFLib.Graph`
    """
    while True:
        # 1. collect the import statements:
        all_imports = [t for t in graph.triples((None, imports, None))]
        if len(all_imports) == 0:
            # no import statement whatsoever, we can go on...
            return
        # 2. remove all the import statements from the graph
        for t in all_imports:
            graph.remove(t)
        # 3. get all the imported vocabularies and import them
        for (s, p, uri) in all_imports:
            # this is not 100% kosher. The expected object for an import statement is a URI. However,
            # on local usage, a string would also make sense, so I do that one, too
            if isinstance(uri, rdflibLiteral):
                __parse_input(iformat, str(uri), graph)
            else:
                __parse_input(iformat, uri, graph)
            # 4. start all over again to see if import statements have been imported


def return_closure_class(owl_closure, rdfs_closure, owl_extras, trimming=False):
   
    if owl_closure:
        if owl_extras:
            if trimming:
                return OWLEL_Extension_Trimming
            else:
                return OWLEL_Extension
        else:
            if rdfs_closure:
                return RDFS_OWLEL_Semantics
            else:
                return OWLEL_Semantics
    elif rdfs_closure:
        return RDFS_Semantics
    else:
        return None


# noinspection PyCallingNonCallable
class DeductiveClosure:
   
    # This is the original set of param definitions in the class definition
    #
    # @ivar rdfs_closure: Whether the RDFS closure should also be executed. Default: False.
    # @type rdfs_closure: boolean
    # @ivar axiomatic_triples: Whether relevant axiomatic triples are added before chaining, except for datatype axiomatic
    # triples. Default: False.
    # @type axiomatic_triples: boolean
    # @ivar datatype_axioms: Whether further datatype axiomatic triples are added to the output. Default: false.
    # @type datatype_axioms: boolean
    # @ivar closure_class: the class instance used to expand the graph
    # @type closure_class: L{Closure.Core}
    # @cvar improved_datatype_generic: Whether the improved set of lexical-to-Python conversions should be used for
    # datatype handling I{in general}, ie, not only for a particular instance and not only for inference purposes.
    # Default: False.
    # @type improved_datatype_generic: boolean

    improved_datatype_generic = False

    def __init__(self, closure_class, improved_datatypes=True, rdfs_closure=False, axiomatic_triples=False,
                 datatype_axioms=False):
        # This is the original set of param definitions in the __init__
        #
        # @param closure_class: a closure class reference.
        # @type closure_class: subclass of L{Closure.Core}
        # @param rdfs_closure: whether RDFS rules are executed or not
        # @type rdfs_closure: boolean
        # @param axiomatic_triples: Whether relevant axiomatic triples are added before chaining, except for datatype
        # axiomatic triples. Default: False.
        # @type axiomatic_triples: boolean
        # @param datatype_axioms: Whether further datatype axiomatic triples are added to the output. Default: false.
        # @type datatype_axioms: boolean
        # @param improved_datatypes: Whether the improved set of lexical-to-Python conversions should be used for
        # datatype handling. See the introduction for more details. Default: True.
        # @type improved_datatypes: boolean

        if closure_class is None:
            self.closure_class = None
        else:
            if not isinstance(closure_class, type):
                raise ValueError("The closure type argument must be a class reference")
            else:
                self.closure_class = closure_class
        self.axiomatic_triples = axiomatic_triples
        self.datatype_axioms = datatype_axioms
        self.rdfs_closure = rdfs_closure
        self.improved_datatypes = improved_datatypes

    def expand(self, graph):
        """
        Expand the graph using forward chaining, and with the relevant closure type.
        :param graph: The RDF graph.
        :type graph: :class:`rdflib.Graph`
        """
        if (not DeductiveClosure.improved_datatype_generic) and self.improved_datatypes:
            DatatypeHandling.use_Alt_lexical_conversions()

        if self.closure_class is not None:
            self.closure_class(graph, self.axiomatic_triples, self.datatype_axioms, self.rdfs_closure).closure()

        if (not DeductiveClosure.improved_datatype_generic) and self.improved_datatypes:
            DatatypeHandling.use_RDFLib_lexical_conversions()

    @staticmethod
    def use_improved_datatypes_conversions():
        """
        Switch the system to use the improved datatype conversion routines.
        """
        DeductiveClosure.improved_datatype_generic = True
        DatatypeHandling.use_Alt_lexical_conversions()

    @staticmethod
    def use_rdflib_datatypes_conversions():
        """
        Switch the system to use the generic (RDFLib) datatype conversion routines
        """
        DeductiveClosure.improved_datatype_generic = False
        DatatypeHandling.use_RDFLib_lexical_conversions()

###############################################################################################################


# noinspection PyPep8Naming,PyBroadException,PyBroadException,PyBroadException
def convert_graph(options, closureClass=None):
   

 

    def __check_yes_or_true(opt):
        return opt is True or opt == "yes" or opt == "Yes" or opt == "True" or opt == "true"

    import warnings

    warnings.filterwarnings("ignore")
    if len(options.sources) == 0 and (options.text is None or len(options.text.strip()) == 0):
        raise Exception("No graph specified either via a URI or text")

    graph = Graph()

    # Just to be sure that this attribute does not create issues with older versions of the service...
    # the try statement should be removed, eventually...
    iformat = AUTO
    try:
        iformat = options.iformat
    except:
        # exception can be raised if that attribute is not used at all, true for older versions
        pass

    # similar measure with the possible usage of the 'source' options
    try:
        if options.source is not None:
            options.sources.append(options.source)
    except:
        # exception can be raised if that attribute is not used at all, true for newer versions
        pass

    # Get the sources first. Note that a possible error is filtered out, namely to process the same file twice. This is
    # done by turning the input arguments into a set...
    for inp in set(options.sources):
        __parse_input(iformat, inp, graph)

    # add the possible extra text (ie, the text input on the HTML page)
    if options.text is not None:
        graph.parse(io.StringIO(options.text), format="n3")

    # Get all the options right
    # noinspection PyPep8Naming
    owlClosure = __check_yes_or_true(options.owlClosure)
    # noinspection PyPep8Naming
    rdfsClosure = __check_yes_or_true(options.rdfsClosure)
    # noinspection PyPep8Naming
    owlExtras = __check_yes_or_true(options.owlExtras)
    try:
        trimming = __check_yes_or_true(options.trimming)
    except:
        trimming = False
    axioms = __check_yes_or_true(options.axioms)
    daxioms = __check_yes_or_true(options.daxioms)

    if owlClosure:
        interpret_owl_imports(iformat, graph)

    # adds to the 'beauty' of the output
    graph.bind("owl", "http://www.w3.org/2002/07/owl#")
    graph.bind("xsd", "http://www.w3.org/2001/XMLSchema#")

    # @@@@ some smarter choice should be used later to decide what the closure class is!!! That should
    # also control the import management. Eg, if the superclass includes OWL...
    if closureClass is not None:
        closure_class = closureClass
    else:
        closure_class = return_closure_class(owlClosure, rdfsClosure, owlExtras, trimming)

    DeductiveClosure(closure_class, improved_datatypes=True, rdfs_closure=rdfsClosure, axiomatic_triples=axioms,
                     datatype_axioms=daxioms).expand(graph)

    if options.format == TURTLE:
        return graph.serialize(format="turtle")
    elif options.format == JSON:
        if json_ld_available:
            return graph.serialize(format="json-ld")
        else:
            raise Exception("JSON-LD serializer is not available")
    else:
        return graph.serialize(format="pretty-xml")
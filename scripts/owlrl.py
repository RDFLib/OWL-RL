#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from optparse import OptionParser
from owlrl import convert_graph, RDFXML, TURTLE, JSON, AUTO, RDFA


def main():
    parser = OptionParser(usage="%prog [options] fname1 fname2 ...")
    parser.disable_interspersed_args()
    
    # The 'text' field is not used in the command line, but the CGI environment uses it. This means that there
    # is no option to change that, but is added to the final option structure
    parser.set_defaults(format=TURTLE, owlClosure="no", rdfsClosure="no", owlExtras="no", axioms="no", daxioms="no",
                        iformat=AUTO, trimming="no", maximal="no", text=None)
    
    parser.add_option("-f", "--file", type="string", dest="source",
                      help="input file; should be a .rdf or .ttl file, for RDF/XML or Turtle, respectively. If "
                            "missing, or if the value is '-' then standard input is used. Usage of this options is not "
                            "really necessary, the fname in the command lines refer to files by themselves")
    
    parser.add_option("--owlrl", action="store", dest="owlClosure", choices=["yes", "no"],
                      help="execute OWL RL closure; argument must be yes|no [default: %default]")
    
    parser.add_option("-w", action="store_const", dest="owlClosure", const="yes",
                      help="OWL-RL is executed; shorthand for --owlrl=yes")
    
    parser.add_option("--rdfs", action="store", dest="rdfsClosure", choices=["yes", "no"],
                      help="execute RDFS closure; argument must be yes|no [default: %default]")

    parser.add_option("-r", action="store_const", dest="rdfsClosure", const="yes",
                      help="RDFS is executed; shorthand for --rdfs=yes")

    parser.add_option("--extras", action="store", dest="owlExtras", choices=["yes", "no"],
                      help="additional owl features added; argument must be yes|no [default: %default]")

    parser.add_option("-e", action="store_const", dest="owlExtras", const="yes",
                      help="additional owl features added; shorthand for --extras=yes [default: %default]")

    parser.add_option("--axioms", action="store", dest="axioms", choices=["yes", "no"],
                      help="axiomatic triples; argument must be yes|no [default: %default]")
    
    parser.add_option("-a", action="store_const", dest="axioms", const="yes",
                      help="add axiomatic triples; shorthand for --axioms=yes [default: %default]")

    parser.add_option("--daxioms", action="store", dest="daxioms", choices=["yes", "no"],
                      help="datatype axiomatic triples; argument must be true|false [default: %default]")
    
    parser.add_option("-d", action="store_const", dest="daxioms", const="yes",
                      help="add axiomatic triples; shorthand for --daxioms=yes [default: %default]")

    parser.add_option("--trimming", action="store", dest="trimming", choices=["yes", "no"],
                      help="trim the output of OWL 2 RL and extension; 'yes' is ineffective unless --extras=yes  "
                      "[default: %default]")

    parser.add_option("-m", "--maximal", action="store_const", dest="maximal", const="yes",
                      help="maximal possibilities switched on: RDFS, OWL with extensions, and with trimming")

    parser.add_option("-t", action="store_const", dest="trimming", const="yes",
                      help="trim the output of OWL 2 RL and extension; shorthand for --trimming=yes "
                           "[default: %default]")
    
    parser.add_option("-o", "-s", "--serialization", "--syntax", action="store", dest="format",
                      choices=[TURTLE, JSON, RDFXML],
                      help="output format; argument must be turtle|json|xml [default: %default]")
    
    parser.add_option("-i", "--input_syntax", action="store", dest="iformat",
                      choices=[AUTO, TURTLE, JSON, RDFA, RDFXML],
                      help="format of input; argument must be auto|turtle|xml|rdfa|json [default: %default]; auto "
                            "means that file suffix defines the format. This flag is valid for all input files.")

    (options, args) = parser.parse_args()
    if options.source is None:
        options.sources = []
    else:
        options.sources = [options.source]
        
    if len(args) > 0:
        options.sources += args
        
    if len(options.sources) == 0:
        # the default mechanism, ie, to use standard input
        options.sources = ["-"]

    if options.maximal == "yes":
        options.trimming = "yes"
        options.owlClosure = "yes"
        options.owlExtras = "yes"
            
    print(convert_graph(options))


# The standard startup idiom...
if __name__ == '__main__':
    main()

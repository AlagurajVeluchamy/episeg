from argumentparse import *
from complexes import *


def categorise():
    """ Parse the subcommand along with its arguments. """
    descr = '''
    Find complexes from ChIP-seq mapped files.
    '''
    import argparse
    parser = argparse.ArgumentParser(description=descr, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers( title='Subcommands')
    #parser.add_argument("square", type=int, help="display the square of a given number")
    clusterdataoptions(subparsers)
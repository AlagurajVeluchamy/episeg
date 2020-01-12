from readfiles import *
from complexes import *

def readdirectories(subparsers):
    """ Read bed/bam files from a directory. """
    help_str = "Read bed/bam files from a directory."
    parser_t = subparsers.add_parser('readdirectories', help=help_str)
    parser_t.add_argument('-d', '--directory_bedfiles', required=False, type=str, dest='dir_bed', action='store', help=help_str)
    parser_t.add_argument('-b', '--directory_bamfiles', required=False, type=str, dest='dir_bam', action='store', help=help_str)
    parser_t.set_defaults(func=readallbed)
def arg_parsing():
    """ Parse the subcommand along with its arguments. """
    descr = '''
    Find complexes from ChIP-seq mapped files.
    '''
    import argparse
    parser = argparse.ArgumentParser(description=descr, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers( title='Subcommands')
    #parser.add_argument("square", type=int, help="display the square of a given number")
    readdirectories(subparsers)
    # tffm_apply_arg_parsing(subparsers)
    # pssm_train_arg_parsing(subparsers)
    # pssm_apply_arg_parsing(subparsers)
    # binary_train_arg_parsing(subparsers)
    # binary_apply_arg_parsing(subparsers)
    argu = parser.parse_args()
    return argu
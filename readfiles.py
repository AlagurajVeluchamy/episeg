import os
from argumentparse import *
from complexes import *
import glob
import pysam
from pybedtools import BedTool
from subprocess import call
import numpy


def readallbed(argu):
    """ Read bed/bam files from a directory. """
    #print argu.dir_bam
    print argu.dir_bed
    file = " "
    if argu.dir_bam is None:
        filecount = 0
        for file in glob.glob(os.path.join(argu.dir_bed,'*narrowPeak1')):
            print file
            filecount += 1
            filesmod = glob.glob(os.path.join(argu.dir_bed,'*HistPeak1'))
            filesmod.append(file)
            makemergedpeaks(argu, file, filesmod, filecount)
    return file
    # if argu.dir_bed is None:
    #     for file in glob.glob(os.path.join(argu.dir_bam, '*.bam')):
    #         samfile = pysam.AlignmentFile(file, "rb")

def makemergedpeaks(argu, file, filesmod, filecount):
    ## windowsize get as argument
    windowsize = "200"
    #print filesmod
    ### type yes or no
    generatemergedpeaks = "no"
    if (generatemergedpeaks == "yes"):
        firstfile = BedTool(filesmod[0])
        mergedcontent = firstfile.cat(*filesmod[1:])
        mergedcontentfile = os.path.join(argu.dir_bed, 'mergedpeaks.bed')
        mergedcontent.saveas(mergedcontentfile)
    if (generatemergedpeaks == "no"):
        mergedcontentfile = file

    # for making windows
    mergedpeakswindowsfile = os.path.join(argu.dir_bed, 'mergedpeaks_windows.bed')
    mergedpeakswindows = open(mergedpeakswindowsfile,"w")
    call(['bedtools', 'makewindows', '-b', mergedcontentfile, '-w', windowsize], stdout = mergedpeakswindows)
    sortmergedpeakswindowsfile = os.path.join(argu.dir_bed, 'sortmergedpeaks_windows.bed')
    sortmergedpeakswindows = open(sortmergedpeakswindowsfile, "w")
    call(['sort', '-k1,1', '-k2,2n', mergedpeakswindowsfile], stdout=sortmergedpeakswindows)
    ###column = "5"
    column = "7"
    ifnooverlapnull = "0"
    for fileinthree in filesmod:
        #print fileinthree
        fileinthreeoverlap = open(fileinthree+ "_" +str(filecount), "w")
        call(['bedtools', 'map', '-c', column, '-o', 'mean', '-a',  sortmergedpeakswindowsfile, '-b', fileinthree, '-null', ifnooverlapnull], stdout = fileinthreeoverlap)

    #makearrays(argu.dir_bed)
        # for line in readfile:
        #     a=10
            #print (line)
            #print (line[4])


        #for file in files:

        # parser_t.add_argument('-T', '--tffmfile', required=True, dest='tffm_file',
        #                       action='store', type=str, help='TFFM XML file.')
        #
        # parser_t.add_argument('-t', '--tffm_kind', required=False,
        #                       dest='tffm_kind', action='store', type=str,
        #                       choices=['first_order', 'detailed'],0986776666666555
        #                       default='first_order',
        #                       help='TFFM kind ("first_order" or "detailed").')
        # help_str = 'Input fasta file containing the foreground sequences.'
        # parser_t.add_argument('-i', '--fg_fasta', required=True, type=str,
        #                       dest='fg_fasta', action='store', help=help_str)
        # help_str = 'Input bed file w/ positions of foreground sequences.'
        # parser_t.add_argument('-I', '--fg_bed', required=True, type=str,
        #                       dest='fg_bed', action='store', help=help_str)
        # help_str = 'Input fasta containing the background sequences.'
        # parser_t.add_argument('-b', '--bg_fasta', required=True, type=str,
        #                       dest='bg_fasta', action='store', help=help_str)
        # help_str = 'Input bed file w/ positions of background sequences.'
        # parser_t.add_argument('-B', '--bg_bed', required=True, type=str,
        #                       dest='bg_bed', action='store', help=help_str)
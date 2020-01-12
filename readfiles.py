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

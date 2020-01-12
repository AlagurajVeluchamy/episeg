#!/usr/bin/python
from argumentparse import *
from makearrays import *
from readfiles import *

# def readallbed(argu):
#     print argu


##############################################################################
#                               MAIN
##############################################################################
if __name__ == "__main__":
    arguments = arg_parsing()
    file = arguments.func(arguments)
    #argum = "/Users/velucha/delete"
    #datanparray = makearrays(argum)
    datanparray = makearrays(arguments.dir_bed)
    ###ndatanparray = filtercriteria(arguments.dir_bed, datanparray, file)
    print file